# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
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
    pdf.setFillColorRGB(0.4,0.4,0.4)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawRightString(width, height-lh, 'Facture');
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawRightString(width, height-2*lh, u'Numéro : %s' % bill.number)
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(width, height-3*lh, u'Date facturation : %s' % bill.billing_date.strftime('%d/%m/%Y'))

    pdf.showPage()
    pdf.save()
    # get pdf from buffer and return it to response
    genpdf = buffer.getvalue()
    buffer.close()
    response.write(genpdf)
    return response
