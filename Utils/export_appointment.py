from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO
from Models.lab_analysis import LabAnalysisDetails
from Models.diagnosis import DiagnosisDetails
from Models.prescription import PrescriptionDetails

def generate_appointment_pdf(patient_info,  prescription_info, diagnosis_info, lab_info):
  # Generate filename
  timestamp = datetime.now().strftime("%Y-%m-%d")
  filename = f"appointment-report-{patient_info['first_name']}_{patient_info['last_name']}-{timestamp}.pdf"

  buffer = BytesIO()
  
  # Create PDF document
  doc = SimpleDocTemplate(
    buffer,
    pagesize=letter,
    leftMargin=40,
    rightMargin=40,
    topMargin=40,
    bottomMargin=40
  )
  
  # Prepare styles
  styles = getSampleStyleSheet()
  
  # Custom styles
  styles['Title'].fontSize = 14
  styles['Title'].leading = 15
  styles['Title'].spaceAfter = 1
  
  styles.add(ParagraphStyle(
    name='Header',
    fontSize=12,
    leading=15,
    spaceAfter=10,
    textColor=colors.darkblue
  ))
  
  styles.add(ParagraphStyle(
    name='WrappedText',
    parent=styles['Normal'],
    fontSize=10,
    leading=12,
    spaceBefore=6,
    spaceAfter=6,
    wordWrap='LTR'
  ))
  
  # Build document content
  elements = []
  
  # Clinic header
  elements.append(Paragraph("Terra Natural Herbs", styles['Title']))
  elements.append(Paragraph("P.O.BOX 222, Arusha, Arusha", styles['Title']))
  elements.append(Paragraph("Phone: (123) 456-7890 | www.terranaturalherbs.co.tz", styles['Title']))
  elements.append(Spacer(1, 30))

  # Patient information
  elements.append(Paragraph("PATIENT INFORMATION", styles['Header']))
  
  patient_data = [
    ["Patient Name:", f"{patient_info['first_name']} {patient_info['last_name']}"],
    ["Patient ID:", patient_info['patient_id']],
    ["Age:", str(patient_info['age'])],
    ["Gender:", patient_info['gender'].capitalize()],
    ["Phone:", patient_info['phone_number_1']]
  ]
  
  patient_table = Table(patient_data, colWidths=[200, 330])
  patient_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
  ]))
  
  elements.append(patient_table)
  elements.append(Spacer(1, 30))

  # Lab Analysis information
  elements.append(Paragraph("LAB ANALYSIS INFORMATION", styles['Header']))

  lab_analysis_data = []
  for lab_detail in lab_info:
    analyses = LabAnalysisDetails.query.filter_by(lab_analysis_id=lab_detail.id).all()
    for analysis in analyses:
      lab_analysis_data.append([
        Paragraph("Lab Test", styles['WrappedText']),
        Paragraph(analysis.test, styles['WrappedText'])
      ])
      lab_analysis_data.append([
        Paragraph("Test Results", styles['WrappedText']),
        Paragraph(analysis.result, styles['WrappedText'])
      ])

  lab_analysis_table = Table(lab_analysis_data, colWidths=[200, 330])
  lab_analysis_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('WORDWRAP', (0, 0), (-1, -1), True),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey)
  ]))
  
  elements.append(lab_analysis_table)
  elements.append(Spacer(1, 30))

  # Diagnosis information
  elements.append(Paragraph("DIAGNOSIS INFORMATION", styles['Header']))

  diagnosis_data = []
  diagnoses = DiagnosisDetails.query.filter_by(diagnosis_id=diagnosis_info.id).all()
  for diagnosis in diagnoses:
    diagnosis_data.append([
      Paragraph("Diagnosed with", styles['WrappedText']),
      Paragraph(diagnosis.diagnosed_disease.name, styles['WrappedText'])
    ])
  diagnosis_data.append([
    Paragraph("Doctor's note", styles['WrappedText']),
    Paragraph(diagnosis_info.note, styles['WrappedText'])
  ])

  diagnosis_table = Table(diagnosis_data, colWidths=[200, 330])
  diagnosis_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('WORDWRAP', (0, 0), (-1, -1), True),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey)
  ]))
  
  elements.append(diagnosis_table)
  elements.append(Spacer(1, 30))

  # Prescription information
  elements.append(Paragraph("PRESCRIPTION INFORMATION", styles['Header']))

  prescription_data = []
  prescriptions = PrescriptionDetails.query.filter_by(prescription_id=prescription_info.id).all()
  for prescription in prescriptions:
    prescription_data.append([
      Paragraph("Prescribed with", styles['WrappedText']),
      Paragraph(prescription.prescribed_medicine.name, styles['WrappedText'])
    ])
  prescription_data.append([
    Paragraph("Doctor's note", styles['WrappedText']),
    Paragraph(prescription_info.note, styles['WrappedText'])
  ])

  prescription_table = Table(prescription_data, colWidths=[200, 330])
  prescription_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('WORDWRAP', (0, 0), (-1, -1), True),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey)
  ]))
  
  elements.append(prescription_table)
  elements.append(Spacer(1, 30))
  
  # Footer
  elements.append(Spacer(1, 10))
  elements.append(Paragraph("For any questions, please contact our billing department.", styles['Title']))
  
  # Generate PDF
  doc.build(elements)

  buffer.seek(0)
  return send_file(
    buffer,
    as_attachment=False,
    mimetype='application/pdf',
    download_name=filename
  )
