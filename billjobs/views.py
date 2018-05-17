# -*- coding: utf-8 -*-
from django.forms import ModelForm, ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, Paragraph
import requests
from io import BytesIO
from .settings import BILLJOBS_DEBUG_PDF, BILLJOBS_BILL_LOGO_PATH, \
        BILLJOBS_BILL_LOGO_WIDTH, BILLJOBS_BILL_LOGO_HEIGHT, \
        BILLJOBS_BILL_PAYMENT_INFO, BILLJOBS_FORCE_SUPERUSER, \
        BILLJOBS_FORCE_USER_GROUP, BILLJOBS_SLACK_TOKEN, \
        BILLJOBS_SLACK_CHANNEL
from .models import Bill, UserProfile, BillLine
from textwrap import wrap
from django.utils import timezone
from django.db.models import Sum
from django.utils.html import format_html
import calendar


class UserSignupForm(ModelForm):
    ''' Form for signup '''
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        if data == "":
            raise ValidationError(_("This field is required."))
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data == "":
            raise ValidationError(_("This field is required."))
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data == "":
            raise ValidationError(_("This field is required."))
        return data


class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ['billing_address']

    def clean_billing_address(self):
        data = self.cleaned_data['billing_address']
        if data == "":
            raise ValidationError(_('This field is required.'))
        return data


def force_user_properties(user):
    ''' Force user properties to be set when we register them '''
    user.is_staff = True
    if BILLJOBS_FORCE_SUPERUSER is True:
        user.is_superuser = True
    if BILLJOBS_FORCE_USER_GROUP is not None:
        group = Group.objects.get(name=BILLJOBS_FORCE_USER_GROUP)
        user.groups.add(group.id)
    user.save()


def send_slack_invitation(user):
    ''' Send an invitation to the newly created user '''
    url = 'https://slack.com/api/users.admin.invite'
    payload = {'token': BILLJOBS_SLACK_TOKEN, 'email': user.email}
    # send request
    response = requests.post(url, data=payload)
    # get json response
    json_response = response.json()
    # response['ok'] is a bool
    notify_subscription(user, json_response['ok'])


def notify_subscription(user, invitation):
    ''' Send to a specific channel information about last signup '''
    if invitation is True:
        invitation_status = 'L\'envoi de l\'invitation slack a réussi'
    elif invitation is False:
        invitation_status = (
                "L\'envoi de l\'invitation slack a échoué\nSoit il sait pas "
                "écrire son email (ça commence bien), soit slack a un "
                "problème (c\'est possible)"
                )

    url = 'https://slack.com/api/chat.postMessage'
    payload = {
            'username': 'signup-bot',
            'token': BILLJOBS_SLACK_TOKEN,
            'channel': BILLJOBS_SLACK_CHANNEL,
            'text': (
                ':new:\nL\'utilisateur {0} ({1} {2}) est inscrit\n'
                'L\'adresse email est {3}\n{4}'.format(
                    user.username,
                    user.first_name,
                    user.last_name,
                    user.email,
                    invitation_status
                    )
                )
            }
    # this failed silently, we do not manage errors
    requests.post(url, data=payload)


def signup(request):
    ''' Signup view for new user '''
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        user_form = UserSignupForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            force_user_properties(user)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            if BILLJOBS_SLACK_TOKEN is not False:
                send_slack_invitation(user)
            return redirect('billjobs_signup_success')
    else:
        user_form = UserSignupForm()
        profile_form = UserProfileForm()
    return render(
            request,
            'billjobs/signup.html',
            {'user_form': user_form, 'profile_form': profile_form}
            )


def signup_success(request):
    return render(request, 'billjobs/signup_success.html')


@login_required
def generate_pdf(request, bill_id):
    bill = Bill.objects.get(id=bill_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = '{} "{}"'.format(
            'attachment; filename=', bill.number)

    # Create a buffer
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    # define new 0,0 bottom left with cm as margin
    pdf.translate(cm, cm)
    # define document width and height with cm as margin
    width, height = A4
    width = width - 2*cm
    height = height - 2*cm

    # if debug draw lines for document limit
    if BILLJOBS_DEBUG_PDF is True:
        pdf.setStrokeColorRGB(1, 0, 0)
        pdf.line(0, 0, width, 0)
        pdf.line(0, 0, 0, height)
        pdf.line(0, height, width, height)
        pdf.line(width, height, width, 0)

    # Put logo on top of pdf original image size is 570px/250px
    pdf.drawImage(
            BILLJOBS_BILL_LOGO_PATH,
            0,
            height-BILLJOBS_BILL_LOGO_HEIGHT,
            width=BILLJOBS_BILL_LOGO_WIDTH,
            height=BILLJOBS_BILL_LOGO_HEIGHT
            )
    # billing information
    lh = 15  # define a line height
    pdf.setFillColorRGB(0.3, 0.3, 0.3)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawRightString(width, height-lh, 'Facture')
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawRightString(width, height-2*lh, u'Numéro : %s' % bill.number)
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(
            width,
            height-3*lh,
            u'Date facturation : {}'.format(
                bill.billing_date.strftime('%d/%m/%Y'))
            )

    # define new height
    nh = height - 90

    # seller
    pdf.setFillColorRGB(0.95, 0.95, 0.95)
    pdf.setStrokeColorRGB(1, 1, 1)
    # rect(x,y,width,height)
    pdf.rect(0, nh-8*lh, width/2-40, 6.4*lh, fill=1)
    # reset fill for text color
    pdf.setFillColorRGB(0.3, 0.3, 0.3)
    pdf.drawString(10, nh-lh, 'Émetteur')
    issuer = Paragraph(bill.issuer_address, getSampleStyleSheet()['Normal'])
    issuer.wrapOn(pdf, width*0.25, 6*lh)
    issuer.drawOn(pdf, 20, nh-6*lh)

    # customer
    pdf.drawString(width/2, nh-lh, 'Adressé à')
    customer = pdf.beginText()
    customer.setTextOrigin(width/2+20, nh-3*lh)
    # create text with \n and remove \r
    text = '{} {}\n{}'.format(
            bill.user.first_name,
            bill.user.last_name,
            bill.billing_address.replace('\r', '')
            )
    # get each line
    for line in text.split('\n'):
        customer.textOut(line)
        customer.moveCursor(0, lh)
    pdf.drawText(customer)
    pdf.setStrokeColorRGB(0, 0, 0)
    # rect(x,y,width,height)
    pdf.rect(width/2, nh-8*lh, width/2, 6.4*lh, fill=0)

    # define new height
    nh = nh - 10*lh

    data = [['Désignation', 'Prix unit. HT', 'Quantité', 'Total HT']]

    for line in bill.billline_set.all():
        description = '{} - {}\n{}'.format(
                line.service.reference,
                line.service.name,
                '\n'.join(wrap(line.service.description, 62)))

        if line.note:
            description = '{}\n{}'.format(
                    description,
                    '\n'.join(wrap(line.note, 62)))

        line = (description, line.service.price, line.quantity, line.total)
        data.append(line)

    data.append((
        'TVA non applicable art-293B du CGI',
        '',
        'Total HT',
        '{} €'.format(bill.amount)
        ))
    data.append(('', '', 'TVA 0%', '0'))
    data.append(('', '', 'Total TTC', '{} €.'.format(bill.amount)))

    # widths in percent of pdf width
    colWidths = (width*0.55, width*0.15, width*0.15, width*0.15)
    style = [
            ('GRID', (0, 0), (-1, 0), 1, colors.black),
            ('GRID', (-2, -3), (-1, -1), 1, colors.black),
            ('BOX', (0, 1), (0, -4), 1, colors.black),
            ('BOX', (1, 1), (1, -4), 1, colors.black),
            ('BOX', (2, 1), (2, -4), 1, colors.black),
            ('BOX', (-1, 1), (-1, -4), 1, colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, -3), (0, -3), 'Helvetica-Bold'),
            ]
    table = Table(data, colWidths=colWidths, style=style)
    # create table and get width and height
    t_width, t_height = table.wrap(0, 0)
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



# set variables
current_year = timezone.now().year
previous_year = current_year - 1
current_month = timezone.now().month
previous_month = current_month - 1

calendar.month_name[current_month]

def month_name(month):
    output = _(calendar.month_name[month])
    return output



# if current_month == 5:
#     current_month_name = 'Mai'
# if previous_month == 4:
#     previous_month_name = 'Avril'

if current_month == 1:
    current_month_name = 'Janvier'
    previous_month_name = 'Décembre'
elif current_month == 2:
    current_month_name = 'Février'
    previous_month_name = 'Janvier'
elif current_month == 3:
    current_month_name = 'Mars'
    previous_month_name = 'Février'
elif current_month == 4:
    current_month_name = 'Avril'
    previous_month_name = 'Mars'
elif current_month == 5:
    current_month_name = 'Mai'
    previous_month_name = 'Avril'
elif current_month == 6:
    current_month_name = 'Juin'
    previous_month_name = 'Mai'
elif current_month == 7:
    current_month_name = 'Juillet'
    previous_month_name = 'Juin'
elif current_month == 8:
    current_month_name = 'Août'
    previous_month_name = 'Juillet'
elif current_month == 9:
    current_month_name = 'Septembre'
    previous_month_name = 'Août'
elif current_month == 10:
    current_month_name = 'Octobre'
    previous_month_name = 'September'
elif current_month == 11:
    current_month_name = 'Novembre'
    previous_month_name = 'October'
elif current_month == 12:
    month_name = 'December'
    previous_month_name = 'November'


# Refactored version
def get_annual_revenue(request, year):
    if year == current_year: # Le chiffre d'affaire annuel est une estimation
        annual_revenue = (Bill.objects.filter(billing_date__year=year, billing_date__month__lte=previous_month).aggregate(Sum('amount'))['amount__sum']) / previous_month * 12
        if annual_revenue == None:
            annual_revenue = "-"
    else:
        annual_revenue =  Bill.objects.filter(billing_date__year=year).aggregate(Sum('amount'))['amount__sum']
        if annual_revenue == None:
            annual_revenue = "-"
    return annual_revenue

# Refactored version
def get_monthly_revenue(request, month, year):
    monthly_revenue =  Bill.objects.filter(billing_date__month=month, billing_date__year=year).aggregate(Sum('amount'))['amount__sum']
    if monthly_revenue == None:
        monthly_revenue = "-"
    if month == current_month and year == current_year:
        return format_html('<strong style="color: purple">{}</strong>', monthly_revenue)
    else:
        return monthly_revenue


def get_current_month_revenue(request):
    current_month_revenue = Bill.objects.filter(billing_date__month=current_month, billing_date__year=current_year).aggregate(Sum('amount'))['amount__sum']
    return current_month_revenue

def get_previous_month_revenue(request):
    previous_month_revenue = Bill.objects.filter(billing_date__month=previous_month, billing_date__year=current_year).aggregate(Sum('amount'))['amount__sum']
    return previous_month_revenue


def get_annual_subscriptions(request, subscription, year):
    annual_subscriptions = BillLine.objects.filter(service__is_available=True,
    service__pk=subscription, bill__billing_date__year=year).count()
    return annual_subscriptions

def get_monthly_subscriptions(request, subscription, month, year):
    monthly_subscriptions = BillLine.objects.filter(service__is_available=True,
    service__pk=subscription, bill__billing_date__month=month, bill__billing_date__year=year).count()
    return monthly_subscriptions

def statistics(request):
    return render(request, 'billjobs/statistics.html',
    {'current_month_name': month_name(current_month),
    'current_year': current_year,
    'current_month_revenue': get_monthly_revenue(request, current_month, current_year),
    'previous_month_name': month_name(previous_month), 'previous_year': previous_year,
    'previous_month_revenue': get_monthly_revenue(request, previous_month, current_year),
    'current_year_revenue': get_annual_revenue(request, current_year),
    'previous_year_revenue': get_annual_revenue(request, previous_year),
    'current_january_revenue': get_monthly_revenue(request, 1, current_year),
    'previous_january_revenue': get_monthly_revenue(request, 1, previous_year),
    'current_february_revenue': get_monthly_revenue(request, 2, current_year),
    'previous_february_revenue': get_monthly_revenue(request, 2, previous_year),
    'current_march_revenue': get_monthly_revenue(request, 3, current_year),
    'previous_march_revenue': get_monthly_revenue(request, 3, previous_year),
    'current_april_revenue': get_monthly_revenue(request, 4, current_year),
    'previous_april_revenue': get_monthly_revenue(request, 4, previous_year),
    'current_may_revenue': get_monthly_revenue(request, 5, current_year),
    'previous_may_revenue': get_monthly_revenue(request, 5, previous_year),
    'current_june_revenue': get_monthly_revenue(request, 6, current_year),
    'previous_june_revenue': get_monthly_revenue(request, 6, previous_year),
    'current_july_revenue': get_monthly_revenue(request, 7, current_year),
    'previous_july_revenue': get_monthly_revenue(request, 7, previous_year),
    'current_august_revenue': get_monthly_revenue(request, 8, current_year),
    'previous_august_revenue': get_monthly_revenue(request, 8, previous_year),
    'current_september_revenue': get_monthly_revenue(request, 9, current_year),
    'previous_september_revenue': get_monthly_revenue(request, 9, previous_year),
    'current_october_revenue': get_monthly_revenue(request, 10, current_year),
    'previous_october_revenue': get_monthly_revenue(request, 10, previous_year),
    'current_november_revenue': get_monthly_revenue(request, 11, current_year),
    'previous_november_revenue': get_monthly_revenue(request, 11, previous_year),
    'current_december_revenue': get_monthly_revenue(request, 12, current_year),
    'previous_december_revenue': get_monthly_revenue(request, 12, previous_year),
    'current_january_subscriptions_1': get_monthly_subscriptions(request, 1, 1, current_year),
    'current_february_subscriptions_1': get_monthly_subscriptions(request, 1, 2, current_year),
    'current_march_subscriptions_1': get_monthly_subscriptions(request, 1, 3, current_year),
    'current_april_subscriptions_1': get_monthly_subscriptions(request, 1, 4, current_year),
    'current_may_subscriptions_1': get_monthly_subscriptions(request, 1, 5, current_year),
    'current_june_subscriptions_1': get_monthly_subscriptions(request, 1, 6, current_year),
    'current_july_subscriptions_1': get_monthly_subscriptions(request, 1, 7, current_year),
    'current_august_subscriptions_1': get_monthly_subscriptions(request, 1, 8, current_year),
    'current_september_subscriptions_1': get_monthly_subscriptions(request, 1, 9, current_year),
    'current_october_subscriptions_1': get_monthly_subscriptions(request, 1, 10, current_year),
    'current_november_subscriptions_1': get_monthly_subscriptions(request, 1, 11, current_year),
    'current_december_subscriptions_1': get_monthly_subscriptions(request, 1, 12, current_year),
    'current_year_subscriptions_1': get_annual_subscriptions(request, 1, current_year),
    'current_january_subscriptions_2': get_monthly_subscriptions(request, 2, 1, current_year),
    'current_february_subscriptions_2': get_monthly_subscriptions(request, 2, 2, current_year),
    'current_march_subscriptions_2': get_monthly_subscriptions(request, 2, 3, current_year),
    'current_april_subscriptions_2': get_monthly_subscriptions(request, 2, 4, current_year),
    'current_may_subscriptions_2': get_monthly_subscriptions(request, 2, 5, current_year),
    'current_june_subscriptions_2': get_monthly_subscriptions(request, 2, 6, current_year),
    'current_july_subscriptions_2': get_monthly_subscriptions(request, 2, 7, current_year),
    'current_august_subscriptions_2': get_monthly_subscriptions(request, 2, 8, current_year),
    'current_september_subscriptions_2': get_monthly_subscriptions(request, 2, 9, current_year),
    'current_october_subscriptions_2': get_monthly_subscriptions(request, 2, 10, current_year),
    'current_november_subscriptions_2': get_monthly_subscriptions(request, 2, 11, current_year),
    'current_december_subscriptions_2': get_monthly_subscriptions(request, 2, 12, current_year),
    'current_year_subscriptions_2': get_annual_subscriptions(request, 2, current_year),
    'current_january_subscriptions_3': get_monthly_subscriptions(request, 3, 1, current_year),
    'current_february_subscriptions_3': get_monthly_subscriptions(request, 3, 2, current_year),
    'current_march_subscriptions_3': get_monthly_subscriptions(request, 3, 3, current_year),
    'current_april_subscriptions_3': get_monthly_subscriptions(request, 3, 4, current_year),
    'current_may_subscriptions_3': get_monthly_subscriptions(request, 3, 5, current_year),
    'current_june_subscriptions_3': get_monthly_subscriptions(request, 3, 6, current_year),
    'current_july_subscriptions_3': get_monthly_subscriptions(request, 3, 7, current_year),
    'current_august_subscriptions_3': get_monthly_subscriptions(request, 3, 8, current_year),
    'current_september_subscriptions_3': get_monthly_subscriptions(request, 3, 9, current_year),
    'current_october_subscriptions_3': get_monthly_subscriptions(request, 3, 10, current_year),
    'current_november_subscriptions_3': get_monthly_subscriptions(request, 3, 11, current_year),
    'current_december_subscriptions_3': get_monthly_subscriptions(request, 3, 12, current_year),
    'current_year_subscriptions_3': get_annual_subscriptions(request, 3, current_year),

    'previous_january_subscriptions_1': get_monthly_subscriptions(request, 1, 1, previous_year),
    'previous_february_subscriptions_1': get_monthly_subscriptions(request, 1, 2, previous_year),
    'previous_march_subscriptions_1': get_monthly_subscriptions(request, 1, 3, previous_year),
    'previous_april_subscriptions_1': get_monthly_subscriptions(request, 1, 4, previous_year),
    'previous_may_subscriptions_1': get_monthly_subscriptions(request, 1, 5, previous_year),
    'previous_june_subscriptions_1': get_monthly_subscriptions(request, 1, 6, previous_year),
    'previous_july_subscriptions_1': get_monthly_subscriptions(request, 1, 7, previous_year),
    'previous_august_subscriptions_1': get_monthly_subscriptions(request, 1, 8, previous_year),
    'previous_september_subscriptions_1': get_monthly_subscriptions(request, 1, 9, previous_year),
    'previous_october_subscriptions_1': get_monthly_subscriptions(request, 1, 10, previous_year),
    'previous_november_subscriptions_1': get_monthly_subscriptions(request, 1, 11, previous_year),
    'previous_december_subscriptions_1': get_monthly_subscriptions(request, 1, 12, previous_year),
    'previous_year_subscriptions_1': get_annual_subscriptions(request, 1, previous_year),
    'previous_january_subscriptions_2': get_monthly_subscriptions(request, 2, 1, previous_year),
    'previous_february_subscriptions_2': get_monthly_subscriptions(request, 2, 2, previous_year),
    'previous_march_subscriptions_2': get_monthly_subscriptions(request, 2, 3, previous_year),
    'previous_april_subscriptions_2': get_monthly_subscriptions(request, 2, 4, previous_year),
    'previous_may_subscriptions_2': get_monthly_subscriptions(request, 2, 5, previous_year),
    'previous_june_subscriptions_2': get_monthly_subscriptions(request, 2, 6, previous_year),
    'previous_july_subscriptions_2': get_monthly_subscriptions(request, 2, 7, previous_year),
    'previous_august_subscriptions_2': get_monthly_subscriptions(request, 2, 8, previous_year),
    'previous_september_subscriptions_2': get_monthly_subscriptions(request, 2, 9, previous_year),
    'previous_october_subscriptions_2': get_monthly_subscriptions(request, 2, 10, previous_year),
    'previous_november_subscriptions_2': get_monthly_subscriptions(request, 2, 11, previous_year),
    'previous_december_subscriptions_2': get_monthly_subscriptions(request, 2, 12, previous_year),
    'previous_year_subscriptions_2': get_annual_subscriptions(request, 2, previous_year),
    'previous_january_subscriptions_3': get_monthly_subscriptions(request, 3, 1, previous_year),
    'previous_february_subscriptions_3': get_monthly_subscriptions(request, 3, 2, previous_year),
    'previous_march_subscriptions_3': get_monthly_subscriptions(request, 3, 3, previous_year),
    'previous_april_subscriptions_3': get_monthly_subscriptions(request, 3, 4, previous_year),
    'previous_may_subscriptions_3': get_monthly_subscriptions(request, 3, 5, previous_year),
    'previous_june_subscriptions_3': get_monthly_subscriptions(request, 3, 6, previous_year),
    'previous_july_subscriptions_3': get_monthly_subscriptions(request, 3, 7, previous_year),
    'previous_august_subscriptions_3': get_monthly_subscriptions(request, 3, 8, previous_year),
    'previous_september_subscriptions_3': get_monthly_subscriptions(request, 3, 9, previous_year),
    'previous_october_subscriptions_3': get_monthly_subscriptions(request, 3, 10, previous_year),
    'previous_november_subscriptions_3': get_monthly_subscriptions(request, 3, 11, previous_year),
    'previous_december_subscriptions_3': get_monthly_subscriptions(request, 3, 12, previous_year),
    'previous_year_subscriptions_3': get_annual_subscriptions(request, 3, previous_year),


    } )
