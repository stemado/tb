
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from tb.medications.models import MedicationTime
from tb.activities.models import Notification
from tb.decorators import ajax_required


@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.all()
    unread = Notification.objects.filter(is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()

    return render(request, 'activities/notifications.html',
                  {'notifications': notifications})


@login_required
@ajax_required
def last_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(is_read=False)[:5]
    for notification in notifications:
        notification.is_read = True
        notification.save()

    return render(request,
                  'activities/last_notifications.html',
                  {'notifications': notifications})


@login_required
@ajax_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user,
                                                is_read=False)[:5]
    return HttpResponse(len(notifications))

@login_required
@ajax_required
def check_notifications_medication(request):
    user = request.user
    overdue = MedicationTime.get_overdue_medications()[:5]
    return HttpResponse(len(overdue))