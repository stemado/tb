
import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render

from tb.core.forms import ChangePasswordForm, ProfileForm, EditProfileForm, SignUpStep1
from tb.medications.models import Medication, MedicationTime, MedicationCompletion
from tb.feeds.models import Feed
from tb.feeds.views import FEEDS_NUM_PAGES, feeds
from tb.authentication.models import Notification
from PIL import Image



def home(request):
    if request.user.is_authenticated():
        user =request.user
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
        return render(request, 'core/cover.html')


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
def clinicReport(request):
    user = request.user
    page_user = get_object_or_404(User, username=user.username)
    medications = Medication.objects.all()
    paginator = Paginator(medications, 10)
    page = request.GET.get('page')
    try:
        meds = paginator.page(page)
    except PageNotAnInteger:
        meds = paginator.page(1)
    except EmptyPage:
        meds = paginator.page(paginator.num_pages)
    return render(request, 'core/clinic_report.html',
         {'page_user': page_user, 
         'meds': meds
         })



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



@login_required
def medication(request):
    user = request.user
    page_user = get_object_or_404(User, username=user.username)
    user_type = int(page_user.profile.user_type)
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
        return render(request, 'core/medication.html', {'meds': meds, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

    else:
        medications = Medication.get_medications().filter(user=user)
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

        return render(request, 'core/medication.html', {'meds': meds, 'page_user': page_user, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

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
        form = MedicationForm(initial={'user': user})
    return render(request, 'settings/create.html', {'form': form})

@login_required
def registration(request):
    user = request.user
    if request.method == 'POST':
        form = SignUpStep1(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.providence = form.cleaned_data.get('providence')
            user.profile.zipcode = form.cleaned_data.get('zipcode')
            user.profile.address1 = form.cleaned_data.get('address1')
            user.profile.address2 = form.cleaned_data.get('address2')
            user.profile.phonenumber = form.cleaned_data.get('phonenumber')
            user.profile.mobilenumber = form.cleaned_data.get('mobilenumber')
            user.profile.pharmacy = form.cleaned_data.get('pharmacy')
            user.profile.smsnotify = form.cleaned_data.get('pinnumber')
            user.profile.smsnotify = form.cleaned_data.get('smsnotify')
            user.profile.smsnotify = form.cleaned_data.get('emailnotify')
            user.save()
            return redirect('/')
    else:
        form = SignUpStep1(instance=user)
    return render(request, 'core/first_sign_up.html', {'form': form})
