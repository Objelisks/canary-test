from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def authorize(request):
  auth_response = requests.post("https://github.com/login/oauth/access_token", data={
    "client_id": "Ov23libLqCiLNJBdAmxC",
    "client_secret": "b6ee238160886f3f238ef307e5113eed40bb3cbe",
    "code": request.query_params["code"],
  }, headers={"Accept": "application/json"})
  return Response(data={"access_token": auth_response.json()["access_token"]})