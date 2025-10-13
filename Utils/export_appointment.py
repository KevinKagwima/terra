from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO

def generate_appointment_pdf(patient_info,  prescription_info, diagnosis_info, lab_info):
  # Generate filename
  timestamp = datetime.now().strftime("%Y-%m-%d")
  filename = f"payment-receipt-{patient_info['first_name']}_{patient_info['last_name']}-{timestamp}.pdf"

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
    name='NormalBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold'
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

  # Appointment information
  elements.append(Paragraph("APPOINTMENT INFORMATION", styles['Header']))

  appointment_data = [
    ["Lab Analysis", f"{lab_info["lab_details"]}"],
    ["Diagnosed with", f"{diagnosis_info["diagnosis_details"]}"],
    ["Diagnosis Note", f"{diagnosis_info["note"]}"],
    ["Prescribed Medication", f"{prescription_info["prescription_details"]}"],
    ["Doctor's Note", f"{prescription_info["note"]}"]
  ]

  prescription_table = Table(appointment_data, colWidths=[200, 330])
  prescription_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('WORDWRAP', (0, 0), (-1, -1), True)
  ]))
  
  elements.append(prescription_table)
  elements.append(Spacer(1, 30))
  
  # Footer
  elements.append(Paragraph("Thank you for your payment!", styles['Normal']))
  elements.append(Spacer(1, 10))
  elements.append(Paragraph("Please keep this receipt for your records.", styles['Normal']))
  elements.append(Paragraph("For any questions, please contact our billing department.", styles['Normal']))
  
  # Generate PDF
  doc.build(elements)

  buffer.seek(0)
  return send_file(
    buffer,
    as_attachment=False,
    mimetype='application/pdf',
    download_name=filename
  )
