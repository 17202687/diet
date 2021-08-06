from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

class UserView(APIView):
    def get(self, request):
        return Response("ok", status=200) #test response

# Create your views here.
