from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from io import BytesIO
from models import Bill

@login_required
def generate_pdf(request, id):
    bill = Bill.objects.get(id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % bill.number

    # Create a buffer
    buffer = BytesIO()
    template = get_template('generate_pdf.html')
    html  = template.render(Context(bill))
    pisaStatus = pisa.CreatePDF(html, dest=buffer)
    pdf = buffer.getvalue()
    buffer.close()

    # Create the HttpResponse object with the appropriate PDF headers.
    response.write(pdf)
    return response

