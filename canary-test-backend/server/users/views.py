from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User
import requests

# Create your views here.

@api_view(['GET'])
@permission_classes((AllowAny, ))
def index(request):
  user_list = User.objects.all()
  output = ", ".join(["%s %s" % (u.client_id, u.selected_repo_id) for u in user_list])
  return HttpResponse(output)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def login(request):
  print(request.query_params["client_id"])
  user, created = User.objects.get_or_create(client_id=request.query_params["client_id"])
  return Response(data={"client_id": user.client_id, "selected_repo_id": user.selected_repo_id})

@api_view(['POST'])
@permission_classes((AllowAny, ))
def select_repo(request):
  user = get_object_or_404(User, client_id=request.query_params["client_id"])
  user.selected_repo_id = request.query_params["repo_id"]
  user.save()
  return HttpResponse(status=200)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def authorize(request):
  auth_response = requests.post("https://github.com/login/oauth/access_token", data={
    "client_id": "Ov23libLqCiLNJBdAmxC",
    "client_secret": "b6ee238160886f3f238ef307e5113eed40bb3cbe",
    "code": request.query_params["code"],
  }, headers={"Accept": "application/json"})
  return Response(data={"access_token": auth_response.json()["access_token"]})

# Create your views here.
@api_view(['POST'])
@permission_classes((AllowAny, ))
def webhook(request):
  print('webhook call', request.data)
  return Response(status=200)