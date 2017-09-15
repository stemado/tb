from django.shortcuts import render

from tb.medications.models import Medication
# Create your views here.
from tb.api.serializers import MedicationSerializer
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'],)
def MedicationList(request, format=None):
    if "id" in request.GET:
        id = request.GET["id"]
        medications = Medication.objects.filter(user=id)
        serializer = MedicationSerializer(medications, many=True)
        return Response(serializer.data, template_name='api_medications.html')
