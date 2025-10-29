# generador_de_archivos.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os

def generar(estudiante, salida_dir="certificados"):
    try:
        if not os.path.exists(salida_dir):
            os.makedirs(salida_dir)

        nombre_pdf = f"certificado_{estudiante.get('carnet','sin_carnet').replace(' ','_')}.pdf"
        ruta = os.path.join(salida_dir, nombre_pdf)

        doc = SimpleDocTemplate(ruta, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle("Titulo", parent=styles["Title"], fontSize=14, alignment=1)
        estilo_normal = ParagraphStyle("Normal", parent=styles["Normal"], fontSize=10, leading=12)

        story = []

        story.append(Paragraph("<b>UNIVERSIDAD / INSTITUCIÓN</b>", estilo_titulo))
        story.append(Paragraph("<b>INFORME DE CALIFICACIONES</b>", estilo_titulo))
        story.append(Spacer(1,8))

        info = (f"<b>Nombre y apellido:</b> {estudiante.get('nombre','')} {estudiante.get('apellido','')}<br/>"
                f"<b>Carnet:</b> {estudiante.get('carnet','')}  &nbsp;&nbsp; <b>Cédula:</b> {estudiante.get('cedula','')}<br/>"
                f"<b>Carrera:</b> {estudiante.get('carrera','')}  &nbsp;&nbsp; <b>Año:</b> {estudiante.get('anio','')} &nbsp;&nbsp; <b>Ciclo:</b> {estudiante.get('ciclo','')}<br/>"
                f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}")
        story.append(Paragraph(info, estilo_normal))
        story.append(Spacer(1,12))


        data = [["Materia", "C1 P1", "C1 P2", "C2 P1", "C2 P2", "Promedio", "Estado"]]
        materias = estudiante.get("materias", [])
        total = 0.0
        cont = 0
        for mat in materias:
            nombre = mat.get("materia","")
            notas = mat.get("notas", {})
            v1 = notas.get("C1P1","")
            v2 = notas.get("C1P2","")
            v3 = notas.get("C2P1","")
            v4 = notas.get("C2P2","")
            prom = mat.get("promedio", "")
            estado = mat.get("estado", "")
            data.append([nombre, str(v1), str(v2), str(v3), str(v4), f"{prom:.2f}" if isinstance(prom,float) else prom, estado])
            if isinstance(prom, (int,float)):
                total += prom
                cont += 1

        indice = round(total/cont,2) if cont>0 else 0.0


        story.append(Spacer(1,12))


        indice = round(total/cont,2) if cont>0 else 0.0


        estilo_indice = ParagraphStyle("Indice", parent=styles["Normal"], fontSize=11, alignment=2)  # 2 = derecha
        story.append(Paragraph(f"<b>Índice:</b> {indice:.2f}", estilo_indice))


        tabla = Table(data, colWidths=[140,50,50,50,50,70,70])
        tabla.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0), colors.lightgrey),
            ("GRID",(0,0),(-1,-1),0.5,colors.black),
            ("ALIGN",(1,1),(-1,-1),"CENTER"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,-1),9),
        ]))
        story.append(tabla)
        story.append(Spacer(1,12))

        nota = "<i>Nota: Cada ciclo tiene 2 parciales. Promedio calculado sobre los 4 parciales (si están disponibles).</i>"
        story.append(Paragraph(nota, estilo_normal))
        story.append(Spacer(1,18))
        story.append(Paragraph("<b>Firma del/a univeritario:</b> ______________________", estilo_normal))

        doc.build(story)
        print(f"✅ PDF generado: {ruta}")
    except Exception as e:
        print(f"⚠️ Error generando PDF: {e}")

