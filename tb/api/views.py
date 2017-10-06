from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from tb.medications.models import Medication, MedicationTime
# Create your views here.
from tb.api.serializers import MedicationSerializer, MedicationTimeSerializer
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from tb.decorators import ajax_required
from django.http import HttpResponse
import json

@api_view(['GET', 'POST'],)
def MedicationList(request, format=None):
    if "id" in request.GET:
        id = request.GET["id"]
        medications = Medication.objects.filter(user=id)
        serializer = MedicationSerializer(medications, many=True)
        return Response(serializer.data, template_name='api_medications.html')

@api_view(['GET', 'POST'],)
def MedicationTimeList(request, format=None):
    if "id" in request.GET:
        id = request.GET["id"]
        medicationTime = MedicationTime.objects.filter(timeMedication_id__user=id)
        serializer = MedicationTimeSerializer(medicationTime, many=True)
        return Response(serializer.data, template_name='api_medications.html')



