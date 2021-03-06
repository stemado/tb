
import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render

from tb.core.forms import ChangePasswordForm, ProfileForm, EditProfileForm, SignUpStep1, SignUpStep2, SignUpStep3, SignUpStep4, GenerateRandomUserForm
from tb.medications.models import Medication, MedicationTime, MedicationCompletion, MedicationTable
from tb.feeds.models import Feed
from tb.feeds.views import FEEDS_NUM_PAGES, feeds
from tb.authentication.models import Notification, Profile, Clinic
from PIL import Image
from django_filters.views import FilterView
from tb.medications.filters import MedicationFilter
from tb.core.filters import PatientFilter
from django_tables2.export.views import ExportMixin
from tb.core.resources import MedicationResource, PatientResource

from django.http import HttpResponse
from tablib import Dataset
from import_export import resources
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from tb.core.tasks import create_random_user_accounts


###############################################
########### CELERY TASK VIEWS TESTS ###########
###############################################

#@@@ THIS IS USED FOR CREATING USERS TESTS @@@#
#CELERY TEST VIEW 1
class UsersListView(ListView):
    template_name = 'core/users_list.html'
    model = User


#CELERY TEST VIEW 2
class GenerateRandomUserView(FormView):
    template_name = 'core/generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random medication times! Wait a moment and refresh this page.')
        return redirect('users_list')

#@@@ THIS IS USED FOR CREATING MEDICATION TIME TESTS @@@#
# class UsersListView(ListView):
#     template_name = 'core/medications_list.html'
#     model = MedicationTime


#############################################################
################# END CELERY TASK VIEWS ######################
#############################################################

def home(request):
    return render(request, 'core/home.html')

def app(request):
    if request.user.is_authenticated():
        user = request.user
        if user.profile.registration_complete == True:
            user = request.user
            page_user = get_object_or_404(User, username=user.username)
            all_feeds = Feed.get_feeds().filter(user=page_user)
            paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
            feeds = paginator.page(1)
            from_feed = -1
            if feeds:
                from_feed = feeds[0].id
            return render(request, 'core/profile.html', {
            'page_user': page_user,
            'feeds': feeds,
            'from_feed': from_feed,
            'page': 1
            })
        else:
            return redirect('registration')

    else:
        return render(request, 'core/cover.html')

@login_required
def patients(request):
    user = request.user
    page_user = get_object_or_404(User, username=user.username)
    patient_list = Profile.objects.filter()
    patient_filter = PatientFilter(request.GET, queryset=patient_list)
    return render(request, 'core/patients.html',
         {'page_user': page_user, 'filter': patient_filter
         })


@login_required
def network(request):
    users_list = User.objects.filter(is_active=True).order_by('username')
    paginator = Paginator(users_list, 100)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'core/network.html', {'users': users})


@login_required
def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    all_feeds = Feed.get_feeds().filter(user=page_user)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id
    return render(request, 'core/profile.html', {
        'page_user': page_user,
        'feeds': feeds,
        'from_feed': from_feed,
        'page': 1
        })

@login_required
def dashboard(request):
    user = request.user
    page_user = get_object_or_404(User, id=user.id)
    overdue = MedicationTime.get_overdue_medications()
    active = MedicationTime.get_active_medications()
    patients = Profile.objects.filter(user_type='1')
    medication = Medication.objects.all()
    missed = MedicationCompletion.get_monthly_missed()
    delivered = MedicationCompletion.get_monthly_delivered()
    print(overdue)
    return render(request, 'core/dashboard.html', {'missed': missed, 'delivered': delivered, 'overdue': overdue, 'active': active, 'medication': medication, 'patients': patients, 'page_user': page_user })


# @login_required
# def clinicReport(request):
#     user = request.user
#     page_user = get_object_or_404(User, username=user.username)
#     meds = Medication.objects.all().order_by('medicationName')
#     table = MedicationTable(meds)
#     table.paginate(page=request.GET.get('page', 1), per_page=10)
#     return render(request, 'core/clinic_report.html',
#          {'page_user': page_user, 
#          'meds': meds, 'table': table
#          })

@login_required
def clinicReport(request):
    user = request.user
    page_user = get_object_or_404(User, username=user.username)
    medication_list = Medication.objects.select_related().all()
    medication_filter = MedicationFilter(request.GET, queryset=medication_list)
    return render(request, 'core/clinic_report.html',
         {'page_user': page_user, 'filter': medication_filter
         })
    
@login_required
def exportClinicReport(request):
    user = request.user
    page_user = get_object_or_404(User, username=user.username)
    medication_list = Medication.objects.all()
    medication_filter = MedicationFilter(request.GET, queryset=medication_list)
    return render(request, 'core/clinic_report.html',
         {'page_user': page_user, 'filter': medication_filter
         })

@login_required
def importPatients(request):
    user = request.user
    page_user = get_object_or_404(User, username=user.username)
    if request.method == 'POST':
        patient_resource = PatientResource()
        dataset = Dataset()
        new_patients = request.FILES['myfile']

        imported_data = dataset.load(new_patients.read())
        result = patient_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            patient_resource.import_data(dataset, dry_run=False)
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your data was imported successfully!')
        else:
            messages.add_message(request,
                                 messages.WARNING,
                                 'Uh-oh! Your data was unable to be imported!')

    return render(request, 'core/import.html', {'page_user': page_user})

@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.address1 = form.cleaned_data.get('address1')
            user.profile.address2 = form.cleaned_data.get('address2')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.providence = form.cleaned_data.get('providence')
            user.profile.zipcode = form.cleaned_data.get('zipcode')
            user.profile.phonenumber = form.cleaned_data.get('phonenumber')
            user.profile.mobilenumber = form.cleaned_data.get('mobilenumber')
            user.profile.user_type = form.cleaned_data.get('user_type')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        form = ProfileForm(instance=user, initial={
            'address1': user.profile.address1,
            'address2': user.profile.address2,
            'city': user.profile.city,
            'providence': user.profile.providence,
            'zipcode': user.profile.zipcode,
            'phonenumber': user.profile.phonenumber,
            'mobilenumber': user.profile.mobilenumber,
            'user_type': user.profile.user_type,

            })
    return render(request, 'core/settings.html', {'form': form})

####### TO DO ##################################
# Clinic View Form View and Edit Coming Soon to a theatre near you!
# 1. Need to create view ONLY for viewing clinics (since could be more than one)
# 2. Need to create URL for viewing clinics
# 3. Need to create URL for viewing specific clinic
################################################
# @login_required
# def clinic(request, id):
#     user = request.user
#     clinic = get_object_or_404(Clinic, id=id)
#     if request.method == 'POST':
#         form = SignUpStep3(request.POST, instance=clinic)
#         if form.is_valid():
#             clinic = form.save()
#             clinic.province = form.cleaned_data.get('province')
#             clinic.city = form.cleaned_data.get('city')
#             clinic.street = form.cleaned_data.get('street')
#             clinic.suburb = form.cleaned_data.get('suburb')
#             clinic.user = form.cleaned_data.get('user')
#             clinic.save()
#             messages.add_message(request,
#                                  messages.SUCCESS,
#                                  'Your clinic was successfully updated.')
#             return redirect('clinic')


#     else:
#         form = SignUpStep3(instance=clinic, initial={
#             'name': clinic.name,
#             'province': clinic.province,
#             'city': province.city,
#             'street': province.street,
#             'suburb': province.suburb,

#             })
#     return render(request, 'core/settings.html', {'form': form})

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.address1 = form.cleaned_data.get('address1')
            user.profile.address2 = form.cleaned_data.get('address2')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.providence = form.cleaned_data.get('providence')
            user.profile.zipcode = form.cleaned_data.get('zipcode')
            user.profile.phonenumber = form.cleaned_data.get('phonenumber')
            user.profile.mobilenumber = form.cleaned_data.get('mobilenumber')
            user.profile.user_type = form.cleaned_data.get('user_type')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        form = EditProfileForm(instance=user, initial={
            'address1': user.profile.address1,
            'address2': user.profile.address2,
            'city': user.profile.city,
            'providence': user.profile.providence,
            'zipcode': user.profile.zipcode,
            'phonenumber': user.profile.phonenumber,
            'mobilenumber': user.profile.mobilenumber,
            'user_type': user.profile.user_type,

            })
    return render(request, 'core/edit_profile.html', {'form': form})


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception:
        pass

    return render(request, 'core/picture.html',
                  {'uploaded_picture': uploaded_picture})


@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect('password')

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'core/password.html', {'form': form})


@login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/settings/picture/?upload_picture=uploaded')

    except Exception as e:
        print(e)
        return redirect('/settings/picture/')


@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
            request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' +\
            request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except Exception:
        pass

    return redirect('/settings/picture/')


#Export Medication Records
@login_required
def medicationExport(request):
    medication_resource = MedicationResource()
    dataset = medication_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="medications.csv"'
    return response

#On this view, change the Admin(0) to show all patients. Then make the last first_name
#of the patient a link that will then allow them to "login" as the Patient and view the patient's information
@login_required
def medication(request):
    user = request.user
    page_user = get_object_or_404(User, id=user.id)
    user_type = int(page_user.profile.user_type)
    if user_type == 0:
        medications = Medication.get_medications()
        active_count = MedicationTime.get_active_medications()
        overdue_count = MedicationTime.get_overdue_medications()  
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
        return render(request, 'core/medication.html', {'meds': meds, 'page_user': page_user, 'active_count': active_count, 'overdue_count': overdue_count, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

    else:
        medications = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active').values('id')
        medcount = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active')
        active_count = MedicationTime.get_active_medications().filter(timeMedication_id__in=medcount)
        overdue_count = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=medcount)     
        active_medications = MedicationTime.get_active_medications().filter(timeMedication_id__in=medications)
        overdue_medications = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=medications)
        paginator = Paginator(medications, 10)
        page = request.GET.get('page')
        try:
            meds = paginator.page(page)
        except PageNotAnInteger:
            meds = paginator.page(1)
        except EmptyPage:
            meds = paginator.page(paginator.num_pages)

        return render(request, 'core/medication.html', {'meds': meds, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications, 'active_count': active_count, 'overdue_count': overdue_count})

###############################################################
## Loads Patient Medication after clicking                   ##
## User's Login As button when accessing as an Administrator ##
###############################################################

@login_required
def patient_medication(request, id):
    user = request.user
    page_user = get_object_or_404(User, id=id)
    user_type = page_user.profile.user_type
    medications = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active').values('id')
    medcount = Medication.objects.filter(user=page_user, medicationDiscontinuedStatus='Active')
    active_count = MedicationTime.get_active_medications().filter(timeMedication_id__in=medications)
    overdue_count = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=medications)
    active_medications = MedicationTime.get_active_medications().filter(timeMedication_id__in=medications)
    overdue_medications = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=medications)
    paginator = Paginator(medcount, 10)
    page = request.GET.get('page')
    try:
        meds = paginator.page(page)
    except PageNotAnInteger:
        meds = paginator.page(1)
    except EmptyPage:
        meds = paginator.page(paginator.num_pages)

    return render(request, 'core/patient_medication.html', {'meds': meds, 'page_user': page_user, 'active_count': active_count, 'overdue_count': overdue_count, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})


@login_required
def medication_overdue(request, id):
    user = request.user
    page_user = get_object_or_404(User, pk=id)
    user_type = int(page_user.profile.user_type)
    if user_type == 0:
        medications = Medication.get_medications()
        active_count = MedicationTime.get_active_medications()
        overdue_count = MedicationTime.get_overdue_medications()
        active_medications = MedicationTime.get_active_medications()
        overdue_medications = MedicationTime.get_overdue_medications()
        paginator = Paginator(overdue_medications, 10)
        page = request.GET.get('page')
        try:
            meds = paginator.page(page)
        except PageNotAnInteger:
            meds = paginator.page(1)
        except EmptyPage:
            meds = paginator.page(paginator.num_pages)
        return render(request, 'core/medication_overdue.html', {'meds': meds, 'active_count': active_count, 'overdue_count': overdue_count, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

    else:
        medications = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active').values('id')
        print(medications)
        medcount = Medication.get_medications().filter(user=page_user, medicationDiscontinuedStatus='Active')
        active_count = MedicationTime.get_active_medications().filter(timeMedication_id__in=medcount)
        overdue_count = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=medcount)
        active_medications = MedicationTime.get_active_medications().filter(timeMedication_id__in=medications)
        overdue_medications = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=medications)
        paginator = Paginator(overdue_medications, 10)
        page = request.GET.get('page')
        try:
            meds = paginator.page(page)
        except PageNotAnInteger:
            meds = paginator.page(1)
        except EmptyPage:
            meds = paginator.page(paginator.num_pages)

        return render(request, 'core/medication_overdue.html', {'meds': meds, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications, 'active_count': active_count, 'overdue_count': overdue_count})


@login_required
def medication_active(request, id):
    user = request.user
    page_user = get_object_or_404(User, id=id)
    user_type = int(page_user.profile.user_type)
    if user_type == 0:
        medications = Medication.get_medications()
        active_count = MedicationTime.get_active_medications()
        overdue_count = MedicationTime.get_overdue_medications()
        active_medications = MedicationTime.get_active_medications()
        overdue_medications = MedicationTime.get_overdue_medications()
        paginator = Paginator(active_medications, 10)
        page = request.GET.get('page')
        try:
            meds = paginator.page(page)
        except PageNotAnInteger:
            meds = paginator.page(1)
        except EmptyPage:
            meds = paginator.page(paginator.num_pages)
        return render(request, 'core/medication_active.html', {'meds': meds, 'active_count': active_count, 'overdue_count': overdue_count, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

    else:
        medications = Medication.get_medications().filter(user=user, medicationDiscontinuedStatus='Active').values('id')
        medcount = Medication.get_medications().filter(user=user, medicationDiscontinuedStatus='Active')
        active_count = MedicationTime.get_active_medications().filter(timeMedication__id__in=medcount)
        overdue_count = MedicationTime.get_overdue_medications().filter(timeMedication__id__in=medcount)
        active_medications = MedicationTime.get_active_medications().filter(timeMedication__id__in=medications)
        overdue_medications = MedicationTime.get_overdue_medications().filter(timeMedication__id__in=medications)
        paginator = Paginator(active_medications, 10)
        page = request.GET.get('page')
        try:
            meds = paginator.page(page)
        except PageNotAnInteger:
            meds = paginator.page(1)
        except EmptyPage:
            meds = paginator.page(paginator.num_pages)

        return render(request, 'core/medication_active.html', {'meds': meds, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications, 'active_count': active_count, 'overdue_count': overdue_count})

@login_required
def create_medication(request):
    user = request.user
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
        form = MedicationForm(initial={'patient': user})
    return render(request, 'settings/create.html', {'form': form})


@login_required
def registration(request):
    user = request.user
    if request.method == 'POST':
        form = SignUpStep1(request.POST)
        if form.is_valid():
            user.profile.city = form.cleaned_data.get('city')
            user.profile.providence = form.cleaned_data.get('providence')
            user.profile.zipcode = form.cleaned_data.get('zipcode')
            user.profile.address1 = form.cleaned_data.get('address1')
            user.profile.address2 = form.cleaned_data.get('address2')
            user.profile.phonenumber = form.cleaned_data.get('phonenumber')
            user.profile.mobilenumber = form.cleaned_data.get('mobilenumber')
            user.profile.user_type = form.cleaned_data.get('user_type')
            user.profile.pinnumber = form.cleaned_data.get('pinnumber')
            user.save()
            return redirect('registration_tc')
    else:
        form = SignUpStep1(instance=user, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'city': user.profile.city,
            'providence': user.profile.providence,
            'zipcode': user.profile.zipcode,
            'address1': user.profile.address1,
            'address2:': user.profile.address2,
            'phonenumber': user.profile.phonenumber,
            'mobilenumber': user.profile.mobilenumber,
            'pinnumber': user.profile.pinnumber,
            'user_type': user.profile.user_type,
            })
    return render(request, 'core/sign_up_one.html', {'form': form})

@login_required
def registration_page_2(request):
    user = request.user
    if request.method == 'POST':
        form = SignUpStep2(request.POST, instance = user)
        if form.is_valid():

            user.profile.tandc = form.cleaned_data.get('tandc')
            user.save()
            return redirect('registration_pharmacy')
    else:
        form = SignUpStep2(instance=user, initial={
            'tandc': user.profile.tandc,
            })
    return render(request, 'core/sign_up_two.html', {'form': form})


@login_required
def registration_page_3(request):
    user = request.user
    if request.method == 'POST':
        form = SignUpStep3(request.POST)
        if form.is_valid():
            clinic = form.save()
            clinic.province = form.cleaned_data.get('province')
            clinic.city = form.cleaned_data.get('city')
            clinic.street = form.cleaned_data.get('street')
            clinic.suburb = form.cleaned_data.get('suburb')
            clinic.user = form.cleaned_data.get('user')
            clinic.save()
            return redirect('registration_notification')
    else:
        form = SignUpStep3(initial={
            'user': user,
            })

    return render(request, 'core/sign_up_three.html', {'form': form, 'user': user})

# @login_required
# def registration_page_3(request):
#     user = request.user
#     if request.method == 'POST':
#         form = SignUpStep3(request.POST, instance = user)
#         if form.is_valid():

#             user.profile.pharmacy = form.cleaned_data.get('pharmacy')
#             user.save()
#             return redirect('registration_notification')
#     else:
#         form = SignUpStep3(instance=user, initial={
#             'pharmacy': user.profile.pharmacy,
#             })
#     return render(request, 'core/sign_up_three.html', {'form': form})



@login_required
def registration_page_4(request):
    user = request.user
    if request.method == 'POST':
        form = SignUpStep4(request.POST, instance = user)
        if form.is_valid():

            user.profile.smsnotify = form.cleaned_data.get('smsnotify')
            user.profile.emailnotify = form.cleaned_data.get('emailnotify')
            user.profile.registration_complete = True
            user.save()

            welcome_post = 'Congratulations! Your registration is complete!'.format(user.username,
                                                                user.username)
            feed = Feed(user=user, post=welcome_post)
            feed.save()

            return redirect('/app')
    else:
        form = SignUpStep4(instance=user, initial={
            'smsnotify': user.profile.smsnotify,
            'emailnotify': user.profile.emailnotify,
            })
    return render(request, 'core/sign_up_four.html', {'form': form})


########################################################
################ RABBITMQ TASKS ########################
########################################################

#@@@ THIS IS USED FOR CREATING USERS TESTS @@@#
# Will be preface for Medication Time Creations
# And for Medication AcceptRefuse Creations
# For scaling purposes


#CELERY TEST VIEW 1
class UsersListView(ListView):
    template_name = 'core/users_list.html'
    model = User


#CELERY TEST VIEW 2
class GenerateRandomUserView(FormView):
    template_name = 'core/generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random medication times! Wait a moment and refresh this page.')
        return redirect('users_list')

#@@@ THIS IS USED FOR CREATING MEDICATION TIME TESTS @@@#
# class UsersListView(ListView):
#     template_name = 'core/medications_list.html'
#     model = MedicationTime


#############################################################
################# END RABBITMQ TASKS ########################
#############################################################


