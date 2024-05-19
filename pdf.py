from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.utils import ImageReader

def make_pdf_ticket(ticket_bool, how_many, prename, surname):
  if ticket_bool == 1:
    ticket_style = 'Ticket'
  else:
    ticket_style = 'Party-Ticket'
  
  name = prename + ' ' + surname
  
  h, w = A5
  w = 1.5*w
  c = canvas.Canvas("ticket.pdf", pagesize = landscape((h, w)))
  img = ImageReader("background.jpg")
  qr_code = ImageReader("my_qr_code.png")
  
  img_w, img_h = img.getSize()
  qr_w, qr_h = qr_code.getSize()
  c.drawImage(img, 0, 0, width = 0.5*img_w, height = h)
  
  
  c.setFont('Helvetica', 62)
  c.drawString(200, h - 70, 'Pharmaball')
  
  c.setFont('Helvetica-Bold', 48)
  c.drawString(0.5*img_w+ 20, h - 120, ticket_style)
  
  c.setFont('Helvetica', 32)
  c.drawString(0.5*img_w+ 20, h- 250, name)
  
  c.setFont('Helvetica', 22)
  c.drawString(0.5*img_w+ 20, h - 380, '01.06.2024 - Samstag')
  c.drawString(0.5*img_w+ 20, h - 404, 'Westend - Westbahnhof 13')
  
  c.line(590, 0.1*h, 590, 0.9*h)
  
  c.drawImage(qr_code, 640, 0.4*h, width = 0.7*qr_w, height = 0.7*qr_h)
  
  c.drawString(640, h - 300, 'Platz für Sponsoren')

  c.showPage()
  c.save()