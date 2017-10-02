from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import hashlib

import markdown
from tb.medications.forms import MedicationForm, StatusForm, EditStatusForm, MedicationStatusForm, StatusFormSet
from tb.medications.models import Medication, MedicationCompletion, MedicationTime, MedicationCompletionChangeHistory
from tb.authentication.models import Profile
from tb.decorators import ajax_required
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetView
import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus.tables import Table
cm = 2.54
from io import BytesIO
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Q
from datetime import datetime
from reportlab.lib.pagesizes import A4, cm 
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER 
from reportlab.lib import colors
from django.contrib.auth.models import User
import string
from django.utils.dateparse import parse_date
from tb.core.tasks import accept_or_refuse_medication
from django.contrib import messages





def _medications(request, medications):
	return render(request, 'medications/all_medications.html', {
		'medications': medications
		})


def _overdue_medications(request, medications):
    return render(request, 'medications/overdue_medications.html', {
        'medications': medications
        })

def _active_medications(request, medications):
    return render(request, 'medications/active_medications.html', {
        'medications': medications
        })

@login_required
def medications(request):
    user = request.user
    user_type = int(user.profile.user_type)
    if user_type == 0:
        medications = Medication.get_medications()
        active_medications = MedicationTime.get_active_medications()
        overdue_medications = MedicationTime.get_overdue_medications()
        paginator = Paginator(medications, 10)
        page = request.GET.get('page')
        try:
            meds = paginator.page(page)
        except PageNotAnInteger:
            meds = paginator.page(1)
        except EmptyPage:
            meds = paginator.page(paginator.num_pages)
        return render(request, 'medications/all_medications.html', {'meds': meds, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})
    else:
        return render('/')

@login_required
def overdue_medications(request):
    medications = Medication.get_medications()
    overdue = MedicationTime.get_overdue_medications()
    active_medications = MedicationTime.get_active_medications()
    return render(request, 'medications/overdue_medications.html', {'medications': medications,
        'active_medications': active_medications, 'overdue': overdue})

# @login_required
# def medication_overdue(request, id):
#     user = request.user
#     page_user = get_object_or_404(User, id=id)
#     user_type = page_user.profile.user_type
#     if user_type == 0:
#         medications = Medication.get_medications()
#         active_medications = MedicationTime.get_active_medications()
#         overdue_medications = MedicationTime.get_overdue_medications()
#         paginator = Paginator(overdue_medications, 10)
#         page = request.GET.get('page')
#         try:
#             meds = paginator.page(page)
#         except PageNotAnInteger:
#             meds = paginator.page(1)
#         except EmptyPage:
#             meds = paginator.page(paginator.num_pages)
#         return render(request, 'core/medication_overdue.html', {'meds': meds, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

#     else:
#         medications = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active').values('id')
#         medcount = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active')
#         active_count = MedicationTime.get_active_medications().filter(timeMedication__id=medcount)
#         overdue_count = MedicationTime.get_overdue_medications().filter(timeMedication__id=medcount)
#         active_medications = MedicationTime.get_active_medications().filter(timeMedication__id=medications)
#         overdue_medications = MedicationTime.get_overdue_medications().filter(timeMedication__id=medications)
#         paginator = Paginator(overdue_medications, 10)
#         page = request.GET.get('page')
#         try:
#             meds = paginator.page(page)
#         except PageNotAnInteger:
#             meds = paginator.page(1)
#         except EmptyPage:
#             meds = paginator.page(paginator.num_pages)

#         return render(request, 'core/medication_overdue.html', {'meds': meds, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications, 'active_count': active_count, 'overdue_count': overdue_count})




@login_required
def active_medications(request):
    medications = Medication.get_medications()
    active = MedicationTime.get_active_medications()
    overdue_medications = MedicationTime.get_overdue_medications()
    return render(request, 'medications/active_medications.html', {'medications': medications,
        'active': active, 'overdue_medications': overdue_medications})

@login_required
def monthly_missed_medications(request):
    user = request.user
    page_user = get_object_or_404(User, id=user.id)
    missed = MedicationCompletion.get_monthly_missed()
    return render(request, 'medications/missed_by_current_month.html', {'missed': missed, 'page_user': page_user })



@login_required
def medication(request, id):
    medication = get_object_or_404(Medication, pk=id)
    time = MedicationTime.objects.filter(timeMedication=id)
    a = MedicationTime.objects.filter(timeMedication=id).values_list('id', flat=True)
    # Use this when ready for production
    # completion = MedicationCompletion.objects.filter(Q(completionMedication__in=a) & ~Q(completionStatus=None)).order_by('completionDate', 'completionDue')
    completion = MedicationCompletion.objects.filter(completionMedication__in=a).order_by('-completionDate', '-completionTime')
    paginator = Paginator(completion, 10)
    page = request.GET.get('page')
    try:
        meds = paginator.page(page)
    except PageNotAnInteger:
        meds = paginator.page(1)
    except EmptyPage:
        meds = paginator.page(paginator.num_pages)
    return render(request, 'medications/medication.html', {'medication': medication, 'time': time, 'meds': meds})

#On this view, change the Admin(0) to show all patients. Then make the last first_name
#of the patient a link that will then allow them to "login" as the Patient and view the patient's information
# @login_required
# def medication(request):
#     user = request.user
#     page_user = get_object_or_404(User, id=user.id)
#     user_type = int(page_user.profile.user_type)
#     if user_type == 0:
#         medications = Medication.get_medications()
#         active_count = MedicationTime.get_active_medications()
#         overdue_count = MedicationTime.get_overdue_medications()  
#         active_medications = MedicationTime.get_active_medications()
#         overdue_medications = MedicationTime.get_overdue_medications()
#         paginator = Paginator(medications, 10)
#         page = request.GET.get('page')
#         try:
#             meds = paginator.page(page)
#         except PageNotAnInteger:
#             meds = paginator.page(1)
#         except EmptyPage:
#             meds = paginator.page(paginator.num_pages)
#         return render(request, 'core/medication.html', {'meds': meds, 'page_user': page_user, 'active_count': active_count, 'overdue_count': overdue_count, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

#     else:
#         medications = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active').values('id')
#         medcount = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active')
#         active_count = MedicationTime.get_active_medications().filter(timeMedication__id=medcount)
#         overdue_count = MedicationTime.get_overdue_medications().filter(timeMedication__id=medcount)     
#         active_medications = MedicationTime.get_active_medications().filter(timeMedication__id=medications)
#         overdue_medications = MedicationTime.get_overdue_medications().filter(timeMedication__id=medications)
#         paginator = Paginator(medications, 10)
#         page = request.GET.get('page')
#         try:
#             meds = paginator.page(page)
#         except PageNotAnInteger:
#             meds = paginator.page(1)
#         except EmptyPage:
#             meds = paginator.page(paginator.num_pages)

#         return render(request, 'core/medication.html', {'meds': meds, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications, 'active_count': active_count, 'overdue_count': overdue_count})



###############################################################
## Loads Patient Medication after clicking                   ##
## User's Login As button when accessing as an Administrator ##
###############################################################

# @login_required
# def patient_medication(request, id):
#     user = request.user
#     page_user = get_object_or_404(User, id=id)
#     user_type = page_user.profile.user_type
#     medications = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active').values('id')
#     medcount = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active')
#     active_count = MedicationTime.get_active_medications().filter(timeMedication__id=medications)
#     overdue_count = MedicationTime.get_overdue_medications().filter(timeMedication__id=medications)
#     active_medications = MedicationTime.get_active_medications().filter(timeMedication__id=medications)
#     overdue_medications = MedicationTime.get_overdue_medications().filter(timeMedication__id=medications)
#     paginator = Paginator(medcount, 10)
#     page = request.GET.get('page')
#     try:
#         meds = paginator.page(page)
#     except PageNotAnInteger:
#         meds = paginator.page(1)
#     except EmptyPage:
#         meds = paginator.page(paginator.num_pages)

#     return render(request, 'core/patient_medication.html', {'meds': meds, 'page_user': page_user, 'active_count': active_count, 'overdue_count': overdue_count, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})




#Need to add conditional logic to separate who the user is.
#If it is the Admin (request.user.profile.user_type == 0) creating the medication, then we want them to choose who the patient is in the patient field
#If it is the Patient creating the medication, we want the do not want the patient field populated since the patient_user is the user and the patient.
@login_required
def createMedication(request, id):
    user = get_object_or_404(User, pk=id)

    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save()
            medication.medicationName = form.cleaned_data.get('medicationName')
            medication.medicationDosage = form.cleaned_data.get('medicationDosage')
            medication.medicationFrequency = form.cleaned_data.get('medicationFrequency')
            medication.medicationDistribution = form.cleaned_data.get('medicationDistribution')
            medication.medicationQuantity = form.cleaned_data.get('medicationQuantity')
            medication.medicationType = form.cleaned_data.get('medicationType')
            medication.medicationStatus = form.cleaned_data.get('medicationStatus')
            medication.medicationComment = form.cleaned_data.get('medicationComment')
            medication.medicationSlug = form.cleaned_data.get('medicationSlug')
            medication.medicationTimeSchedule = form.cleaned_data.get('medicationTimeSchedule')
            medication.save()
            return redirect('medication')
    else:
        if request.user.profile.user_type == 0:
            form = MedicationForm(initial={'user': user})
        else:
            form = MedicationForm(instance=user, initial={'user': user, 'patient': user.id})
    return render(request, 'medications/create.html', {'form': form})



#This model allows us to edit the Medication.
@login_required
def editMedication(request, id):
    if id:
        medication = get_object_or_404(Medication, pk=id)
    else:
        medication = None

    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            return redirect('/medications/')
    else: 
        form = MedicationForm(instance=medication, initial={'medication': medication})
    return render(request, 'medications/edit.html', {'form': form})

@login_required
def acceptRefuse(request, medication, rx):
    user = request.user
    r = Medication.objects.filter(id=rx).values('user_id')
    getMedTime = MedicationTime.objects.get(id=medication)
    medtime = getMedTime.timeDue
    resident = User.objects.get(id=r)
    date = datetime.now().date()
    rx = rx
    medication = medication
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            status = form.save()
            status.save()

            return redirect('medication')
    else:
        form = StatusForm(initial={'completionMedication': medication, 'completionRx': rx, 'completionDue': medtime, 'completionDate': date, 'is_notified': False  })
    return render(request, 'medications/medication_status.html/', {'form': form, 'user': user, 'rx': rx, 'medication': medication})

@login_required
def editAcceptRefuse(request, id):
    user = request.user
    time = datetime.now()
    if id:
        completion = get_object_or_404(MedicationCompletion, id=id)
        print(completion)
    else:
        completion = None

    if request.method == 'POST':
        form = EditStatusForm(request.POST, instance=completion)
        if form.is_valid():
            completion.completionMissed = 'False'
            completion.completionEdited = True
            completion.completionEditedUser = user.id
            completion.completionEditedDate = time
            form.save()

            #Record update in MedicationCompletionChangesHistory
            MedicationCompletionChangeHistory.objects.create(user=user, medicationRx=completion.completionRx, medicationTime=completion.completionMedication) 


            return redirect('monthlyMissed')
    else: 
        form = EditStatusForm(instance=completion, initial={'completion': completion})
    return render(request, 'medications/edit_missed.html/', {'form': form, 'id': id})
    

@login_required
def deleteMedication(request, id):
    article = get_object_or_404(Medication, pk=id).delete()

    return redirect ('/medications/')


@login_required
def mar(request, mar_id):
    if 'to' and 'from' in request.GET:
        stringTo = request.GET.get('to')
        stringFrom = request.GET.get('from')
        stringDateTo = str.replace(stringTo, '/', '-')
        stringDateFrom = str.replace(stringFrom, '/', '-')
        querystringTo = datetime.strptime(stringDateTo, "%Y-%m-%d").date()
        querystringFrom = datetime.strptime(stringDateFrom, "%Y-%m-%d").date()
        med = Medication.objects.filter(user=mar_id)
        medicationID = Medication.objects.filter(user=mar_id).values('id')
        medication = MedicationCompletion.objects.select_related('completionRx').filter(completionRx_id__in=medicationID, completionDate__range=[querystringTo, querystringFrom])
        paginator = Paginator(med, 5)
        page = request.GET.get('page')
        try:
            meds = paginator.page(page)
        except PageNotAnInteger:
            meds = paginator.page(1)
        except EmptyPage:
            meds = paginator.page(paginator.num_pages)
        return render(request, 'medications/mar.html', {'medication': medication, 'meds': meds, 'querystringTo': querystringTo, 'querystringFrom': querystringFrom})
    else: 
        return redirect('/medication/')



class EditMedicationUpdate(UpdateWithInlinesView):
    model = Medication
    inlines = [StatusFormSet, ]
    fields = ['medicationStatus']

    def post(self, request):
        return redirect ("testMedication")


def csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="testpdf.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C',  ' "Testing"', "Here's a quote"])

    return response

def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    elements = []

    doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)

    data=[(1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31),(3,4,5,6),(5,6,7,8),(7,8,9,10)]
    table = Table(data, colWidths=18, rowHeights=20)
    elements.append(table)
    doc.build(elements) 

    return response

