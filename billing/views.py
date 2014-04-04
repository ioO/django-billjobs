from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from models import Bill

@login_required
def generate_pdf(request, id):
    bill = Bill.objects.get(id=id)
    # Create the HttpResponse object with the appropriate PDF headers.
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % bill.number

    return render(request, 'generate_pdf.html', {'bill': bill})
