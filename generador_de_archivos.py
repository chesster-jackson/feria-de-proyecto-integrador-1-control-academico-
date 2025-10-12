# modulo_certificados.py
"""
Módulo para generar certificados PDF de notas.
Dependencia: reportlab
"""

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generar_certificado_pdf(estudiante, salida_pdf):
    """
    Genera un certificado de notas en formato PDF para un estudiante.

    Parámetros:
        estudiante (dict): Información del estudiante, debe contener:
            - nombre, apellido, carnet, cedula, carrera
            - anio, ciclo, semestre, materia
            - notas (lista de floats)
            - promedio (float)
        salida_pdf (str): Ruta o nombre del archivo PDF de salida.
    """
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(salida_pdf, pagesize=A4)
    story = []

    # Encabezado
    story.append(Paragraph("<b>INSTITUTO NACIONAL DE EDUCACIÓN TÉCNICA</b>", styles["Title"]))
    story.append(Paragraph("Certificado de Notas", styles["Heading2"]))
    story.append(Spacer(1, 12))

    # Información del estudiante
    info = f"""
    <b>Nombre:</b> {estudiante['nombre']} {estudiante['apellido']}<br/>
    <b>Carnet:</b> {estudiante['carnet']}<br/>
    <b>Cédula:</b> {estudiante['cedula']}<br/>
    <b>Carrera:</b> {estudiante['carrera']}<br/>
    <b>Año:</b> {estudiante['anio']} | <b>Ciclo:</b> {estudiante['ciclo']} | <b>Semestre:</b> {estudiante['semestre']}<br/>
    <b>Materia:</b> {estudiante['materia']}<br/>
    <b>Fecha de emisión:</b> {datetime.now().strftime('%d/%m/%Y')}
    """
    story.append(Paragraph(info, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Tabla de notas
    data = [["Parcial", "Nota"]] + [[f"Parcial {i+1}", f"{n:.2f}"] for i, n in enumerate(estudiante["notas"])]
    data.append(["Promedio Final", f"{estudiante['promedio']:.2f}"])
    estado = "Aprobado ✅" if estudiante["promedio"] >= 60 else "Reprobado ❌"
    data.append(["Estado", estado])

    tabla = Table(data, colWidths=[200, 150])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))
    story.append(tabla)
    story.append(Spacer(1, 20))

    # Firma
    story.append(Paragraph("<b>Firma del Director:</b> ____________________", styles["Normal"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Sello Institucional</b>", styles["Italic"]))

    # Generar PDF
    doc.build(story)
    print(f"✅ Certificado generado: {salida_pdf}")
