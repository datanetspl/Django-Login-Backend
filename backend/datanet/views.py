from hashlib import sha512
from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Users

import secrets

# Create your views here.

class UsersView(APIView):
    serializer_class = UserSerializer

    def get_queyset(self):
        users = Users.objects.all()
        return users
    
    def get(self, request, *args, **kwargs):
        try:
            username = request.query_params["username"]
            if(username != None):
                user = Users.objects.get(username=username)
                serializer = UserSerializer(user)
        except:
            users = self.get_queyset()
            serializer = UserSerializer(users,many=True)

        return Response(serializer.data)

class UserLoginView(APIView):
    serializer_class = UserSerializer

    def get_queyset(self):
        users = Users.objects.all()
        return users
    
    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        password = request.data["password"]

        if(not Users.objects.filter(email=email).exists()):
            return Response('Email or Password Incorrect',status=status.HTTP_404_NOT_FOUND)


        user = Users.objects.get(email=email)
        serializer = UserSerializer(user)

        salt = serializer.data['salt']

        hashed = sha512((password+salt).encode('utf-8')).hexdigest()
        if(hashed == serializer.data['password']):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Email or Password Incorrect',status=status.HTTP_404_NOT_FOUND)




class UserRegisterView(APIView):
    serializer_class = UserSerializer

    def get_queyset(self):
        users = Users.objects.all()
        return users
    
    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]
        email = request.data["email"]

        if(Users.objects.filter(email=email).exists()):
            return Response('User exists',status=status.HTTP_409_CONFLICT)

        salt = secrets.token_hex(8)
        hashed = sha512((password+salt).encode('utf-8')).hexdigest()

        new_user = Users(username=username,password=hashed,email=email,salt=salt)
        new_user.save()

        return Response('', status=status.HTTP_200_OK)