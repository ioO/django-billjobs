# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from core import settings
from xhtml2pdf import pisa
from io import BytesIO
from models import Bill
import os

# Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
def link_callback(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.
    """
    for d in settings.STATICFILES_DIRS:
        path = os.path.join(d, uri.replace(settings.STATIC_URL, ""))

    return path

@login_required
def generate_pdf(request, id):
    bill = Bill.objects.get(id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % bill.number

    # Create a buffer
    buffer = BytesIO()
    template = get_template('generate_pdf.html')
    html  = template.render(Context({"bill": bill}))
    pisaStatus = pisa.CreatePDF(html, dest=buffer, link_callback=link_callback)
    pdf = buffer.getvalue()
    buffer.close()

    # Create the HttpResponse object with the appropriate PDF headers.
    response.write(pdf)
    return response

