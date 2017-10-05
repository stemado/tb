
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render

from tb.decorators import ajax_required
from tb.messenger.models import Message

#New Pharmacy Model Would Go Here