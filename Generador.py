from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os

def generar_PDF(estudiante, nombre_pdf, registrar_accion=None):
    try:
        salida_dir = "certificados"
        if not os.path.exists(salida_dir):
            os.makedirs(salida_dir)
        ruta = os.path.join(salida_dir, nombre_pdf)
        doc = SimpleDocTemplate(ruta, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle("Titulo", parent=styles["Title"], fontSize=14, alignment=1)
        estilo_normal = ParagraphStyle("Normal", parent=styles["Normal"], fontSize=10, leading=12)
        story = []
        story.append(Paragraph("<b>UNIVERSIDAD / INSTITUCIÓN</b>", estilo_titulo))
        story.append(Paragraph("<b>INFORME DE CALIFICACIONES</b>", estilo_titulo))
        story.append(Spacer(1, 8))
        info = (f"<b>Nombre:</b> {estudiante.get('nombre','')} {estudiante.get('apellido','')}<br/>"
                f"<b>Carnet:</b> {estudiante.get('carnet','')} &nbsp;&nbsp; <b>Cédula:</b> {estudiante.get('cedula','')}<br/>"
                f"<b>Carrera:</b> {estudiante.get('carrera','')} &nbsp;&nbsp; <b>Año:</b> {estudiante.get('anio','')}<br/>"
                f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}")
        story.append(Paragraph(info, estilo_normal))
        story.append(Spacer(1, 12))

        materias = estudiante.get("materias", [])
        incluir_c2 = any("C2P1" in m.get("notas", {}) or "C2P2" in m.get("notas", {}) for m in materias)

        if incluir_c2:
            data = [["Materia", "C1 P1", "C1 P2", "C2 P1", "C2 P2", "Promedio", "Estado"]]
        else:
            data = [["Materia", "C1 P1", "C1 P2", "Promedio", "Estado"]]

        total = 0.0
        cont = 0
        for mat in materias:
            notas = mat.get("notas", {})
            prom = mat.get("promedio", "")
            estado = mat.get("estado", "")
            if incluir_c2:
                fila = [
                    mat.get("materia", ""),
                    str(notas.get("C1P1", "")),
                    str(notas.get("C1P2", "")),
                    str(notas.get("C2P1", "")),
                    str(notas.get("C2P2", "")),
                    f"{prom:.2f}" if isinstance(prom, float) else prom,
                    estado
                ]
            else:
                fila = [
                    mat.get("materia", ""),
                    str(notas.get("C1P1", "")),
                    str(notas.get("C1P2", "")),
                    f"{prom:.2f}" if isinstance(prom, float) else prom,
                    estado
                ]
            data.append(fila)
            if isinstance(prom, (int, float)):
                total += prom
                cont += 1

        indice = round(total / cont, 2) if cont > 0 else 0.0
        story.append(Spacer(1, 12))
        estilo_indice = ParagraphStyle("Indice", parent=styles["Normal"], fontSize=11, alignment=2)
        story.append(Paragraph(f"<b>Índice:</b> {indice:.2f}", estilo_indice))

        tabla = Table(data, colWidths=[140, 50, 50, 50, 50, 70, 70] if incluir_c2 else [160, 60, 60, 70, 70])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))
        story.append(tabla)
        story.append(Spacer(1, 18))
        story.append(Paragraph("<b>Firma del/a universitario:</b> ______________________", estilo_normal))
        doc.build(story)
        print(f"✅ PDF generado: {ruta}")
        if registrar_accion:
            registrar_accion(f"Se generó certificado PDF para {estudiante['nombre']} {estudiante['apellido']} ({estudiante['carnet']})")
        return estudiante.get("carnet")
    except Exception as e:
        print(f" Error generando PDF: {e}")
        return None

