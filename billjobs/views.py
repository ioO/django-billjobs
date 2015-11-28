# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, Paragraph
from io import BytesIO
from .settings import BILLJOBS_DEBUG_PDF, BILLJOBS_BILL_LOGO_PATH, \
        BILLJOBS_BILL_LOGO_WIDTH, BILLJOBS_BILL_LOGO_HEIGHT, \
        BILLJOBS_BILL_ISSUER, BILLJOBS_BILL_PAYMENT_INFO
from .models import Bill

@login_required
def generate_pdf(request, bill_id):
    bill = Bill.objects.get(id=bill_id)
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
    if BILLJOBS_DEBUG_PDF is True:
        pdf.setStrokeColorRGB(1,0,0)
        pdf.line(0,0,width,0)
        pdf.line(0,0,0,height)
        pdf.line(0,height,width,height)
        pdf.line(width,height,width,0)

    # Put logo on top of pdf original image size is 570px/250px
    pdf.drawImage(BILLJOBS_BILL_LOGO_PATH, 0, height-BILLJOBS_BILL_LOGO_HEIGHT, 
            width=BILLJOBS_BILL_LOGO_WIDTH, height=BILLJOBS_BILL_LOGO_HEIGHT)
    # billing information
    lh = 15 #define a line height
    pdf.setFillColorRGB(0.3,0.3,0.3)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawRightString(width, height-lh, 'Facture');
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawRightString(width, height-2*lh, u'Numéro : %s' % bill.number)
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(width, height-3*lh, u'Date facturation : %s' % bill.billing_date.strftime('%d/%m/%Y'))

    # define new height
    nh = height - 90

    # seller
    pdf.setFillColorRGB(0.95,0.95,0.95)
    pdf.setStrokeColorRGB(1,1,1)
    # rect(x,y,width,height)
    pdf.rect(0, nh-8*lh, width/2-40, 6.4*lh, fill=1)
    # reset fill for text color
    pdf.setFillColorRGB(0.3,0.3,0.3)
    pdf.drawString(10, nh-lh, 'Émetteur')
    issuer = Paragraph(BILLJOBS_BILL_ISSUER, getSampleStyleSheet()['Normal'])
    issuer.wrapOn(pdf, width*0.25, 6*lh)
    issuer.drawOn(pdf, 20, nh-6*lh)

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

    data = [['Désignation', 'Prix unit. HT', 'Quantité', 'Total HT']]

    for line in bill.billline_set.all():
        description = '%s - %s\n%s' % (line.service.reference, line.service.name, line.service.description)
        line = (description, line.service.price, line.quantity, line.total)
        data.append(line)

    data.append(('TVA non applicable art-293B du CGI', '', 'Total HT', '%s €' % bill.amount))
    data.append(('', '', 'TVA 0%', '0'))
    data.append(('', '', 'Total TTC', '%s €' % bill.amount))

    # widths in percent of pdf width
    colWidths = (width*0.55, width*0.15, width*0.15, width*0.15)
    style = [('GRID', (0,0), (-1,0),1, colors.black),
            ('GRID', (-2,-3), (-1,-1), 1, colors.black),
            ('BOX', (0,1), (0,-4), 1, colors.black),
            ('BOX', (1,1), (1,-4), 1, colors.black),
            ('BOX', (2,1), (2,-4), 1, colors.black),
            ('BOX', (-1,1), (-1,-4), 1, colors.black),
            ('ALIGN',(0,0),(0,-1),'LEFT'),
            ('ALIGN',(1,0),(-1,-1),'CENTER'),
            ('ALIGN',(-1,0),(-1,-1),'RIGHT'),
            ('FONTNAME', (0,-3), (0,-3), 'Helvetica-Bold'),
            ]
    table = Table(data, colWidths=colWidths, style=style)
    # create table and get width and height
    t_width, t_height = table.wrap(0,0)
    table.drawOn(pdf, 0, nh-t_height)

    p = Paragraph(BILLJOBS_BILL_PAYMENT_INFO, getSampleStyleSheet()['Normal'])
    p.wrapOn(pdf, width*0.6, 100)
    p.drawOn(pdf, 0, 3*lh)

    pdf.line(0, 2*lh, width, 2*lh)
    pdf.setFontSize(8)
    pdf.drawCentredString(width/2.0, lh, 'Association Loi 1901')

    pdf.showPage()
    pdf.save()
    # get pdf from buffer and return it to response
    genpdf = buffer.getvalue()
    buffer.close()
    response.write(genpdf)
    return response
