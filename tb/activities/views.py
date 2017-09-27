
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
    # notifications = Notification.objects.filter(is_read=False)[:5]
    notifications = Notification.objects.all()
    return HttpResponse(len(notifications))

#This is not the answer to getting the overdue medications to display in the Notifications
#What needs to happen is that we need a trigger of checking if the below does return != 0
#If True, then create a notification with the necessary data:
# 1. notification_type, 2. is_read=False 3. feed_id (Can be blank) 
# 4. from_user_id (Need one called TB), 5. to_user_id (any that are super admins), 6. medication_id = MedicationTime id
# next step is to see if we can take the AJAX Call and add a condition to post to the table IF the reslut is != 0.

#NEW CHALLENGE IS THAT EVERY TIME THIS IS CALLED, IT RECREATES THE NOTIFICATIONS EVERY 30 SECONDS.
#THIS IS NOT A NOTIFICATION, SO WE CANNOT SET TO "NOT_READ" TO STOP IT.


@login_required
@ajax_required
def check_notifications_medication(request):
    user = request.user
    overdue = MedicationTime.get_overdue_medications().filter(is_notified=False).values_list('id', flat=True)
    for od in overdue:

        notification = Notification(notification_type='O', is_read=False, from_user_id=2, to_user_id=1, medication_id=od)
        notification.save()
        notify = MedicationTime.objects.get(id=od)
        notify.is_notified = True
        notify.save()


    print(overdue)
    return HttpResponse(len(overdue))