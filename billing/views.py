# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table
from core import settings
from io import BytesIO
from models import Bill

@login_required
def generate_pdf(request, id):
    bill = Bill.objects.get(id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % bill.number

    # Create a buffer
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    # define new 0,0 bottom left with cm as margin
    pdf.translate(cm,cm)
    # define document width and height with cm as margin
    width, height = A4
    width = width - 2*cm
    height = height - 2*cm

    # if debug draw lines for document limit
    if settings.DEBUG is True:
        pdf.setStrokeColorRGB(1,0,0)
        pdf.line(0,0,width,0)
        pdf.line(0,0,0,height)
        pdf.line(0,height,width,height)
        pdf.line(width,height,width,0)

    # Put logo on top of pdf original image size is 570px/250px
    pdf.drawImage(settings.STATICFILES_DIRS[0]+'/logo-coworking.jpg', 0, height-75, width=138, height=75)
    # billing information
    lh = 15 #define a line height
    pdf.setFillColorRGB(0.3,0.3,0.3)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawRightString(width, height-lh, 'Facture');
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawRightString(width, height-2*lh, u'Numéro : %s' % bill.number)
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(width, height-3*lh, u'Date facturation : %s' % bill.billing_date.strftime('%d/%m/%Y'))

    # define new heght
    nh = height - 90

    # seller
    pdf.setFillColorRGB(0.95,0.95,0.95)
    # rect(x,y,width,height)
    pdf.rect(0, nh-8*lh, width/2-40, 6.4*lh, fill=1)
    # reset fill for text color
    pdf.setFillColorRGB(0.3,0.3,0.3)
    pdf.drawString(10, nh-lh, 'Emetteur')
    pdf.drawString(20, nh-3*lh, 'Cowork\'in Montpellier')
    pdf.drawString(20, nh-4*lh, '19 rue de l\'école de droit')
    pdf.drawString(20, nh-5*lh, '34000 Montpellier')

    # customer
    pdf.drawString(width/2, nh-lh, 'Adressé à')
    customer = pdf.beginText()
    customer.setTextOrigin(width/2+20, nh-3*lh)
    # create text with \n and remove \r
    text = '%s %s\n%s' % (bill.user.first_name, bill.user.last_name, 
                bill.user.userprofile.billing_address.replace('\r',''))
    # get each line
    for line in text.split('\n'):
        customer.textOut(line)
        customer.moveCursor(0,lh)
    pdf.drawText(customer)
    pdf.setStrokeColorRGB(0,0,0)
    # rect(x,y,width,height)
    pdf.rect(width/2, nh-8*lh, width/2, 6.4*lh, fill=0)

    # define new heght
    nh = nh - 10*lh

    data = [['Désignation', 'Prix HT', 'Quantité', 'Total HT']]

    for line in bill.billline_set.all():
        description = '%s - %s' % (line.service.reference, line.service.name)
        line = (description, line.service.price, line.quantity, line.total)
        data.append(line)
            
    table = Table(data)
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 0, nh)

    pdf.showPage()
    pdf.save()
    # get pdf from buffer and return it to response
    genpdf = buffer.getvalue()
    buffer.close()
    response.write(genpdf)
    return response
