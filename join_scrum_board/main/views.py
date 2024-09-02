from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json
from main.models import UserAccount
from add_task.models import TaskItem, SubtaskItem, AssignedContactItem
from contacts.models import ContactItem
from rest_framework.views import APIView, Response
from add_task.serializers import TaskItemSerializer, SubtaskItemSerializer, AssignedContactItemSerializer
from contacts.serializers import ContactItemSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

class IsLoggedInView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, format=None):
        if request.user.is_authenticated:
            print(request.user.is_authenticated)
            return JsonResponse({"status": 1})
        else:
            return JsonResponse({"status": 2})
  

class LoginView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        email = request.POST['email']
        upass = request.POST['password']
        user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))

        get_user_obj = User.objects.filter(username=email).exists()
        if get_user_obj:
            token, created = Token.objects.get_or_create(user=user)
            get_user=User.objects.filter(username=email)
            check_pass = check_password(upass,get_user[0].password)
            if not check_pass:
                print(f"Password dose not exist with username = {get_user[0].username}")
                return JsonResponse({
                    #"id": request.id,
                    "status": 1
                })
            else:
                login(request, user)
                #user_serialized = serializers.serialize('json', [user])
                #json_user_serialized = user_serialized[1:-1]
                userForColor = User.objects.get(username=request.POST.get('email'))
                userColor = userForColor.useraccount.color
                return JsonResponse({
                    "id": user.pk,
                    "username": user.username,
                    "firstname": user.first_name,
                    "lastname": user.last_name,
                    "email": user.email,
                    "userColor": userColor,
                    "token": token.key
                })
                #return JsonResponse(user_serialized[1:-1], safe=False)
        else:
            print('Username dose not exist')
            return JsonResponse({
                #"id": request.id,
                "status": 2
            })

class SignUpView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        newUserData = json.loads(request.body)
        get_user_obj = User.objects.filter(username=newUserData['email']).exists()
        if get_user_obj:
            return JsonResponse({
                "status": 1
            })
        else:          
            new_user = User.objects.create_user(
                username=newUserData['email'],
                password=newUserData['password'],
                email=newUserData['email'],
                first_name=newUserData['first_name'],
                last_name=newUserData['last_name']
            )
            
            UserAccount.objects.create(
                user=new_user,
                color=newUserData['color'],
                phone=newUserData['phone']
            )
            
            ContactItem.objects.create(
                active_user=new_user,
                first_name=newUserData['first_name'],
                last_name=newUserData['last_name'],
                email=newUserData['email'],
                phone=newUserData['phone'],
                color=newUserData['color'],
            )
            #userForColor = User.objects.get(username=request.POST.get('email'))
            #userColor = userForColor.useraccount.color   
            return Response({ "status": "OK - New user and contact created"})

#@method_decorator(login_required(login_url="http://127.0.0.1:5500/login.html"), name="get")
class TasksView(APIView): 
    authenticaiton_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    #@login_required(login_url="http://127.0.0.1:5500/login.html")
    def get(self, request, format=None):
        #tasks = TaskItem.objects.filter(created_by=request.user)
        #tasks = TaskItem.objects.filter(created_by=1)
        tasks = TaskItem.objects.all()
        serializer = TaskItemSerializer(tasks, many=True)
        print(Response(serializer.data))
        return Response(serializer.data)

class SubtasksView(APIView): 
    authenticaiton_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    #@login_required(login_url="http://127.0.0.1:5500/login.html")
    def get(self, request, format=None):
        #subtasks = SubtaskItem.objects.filter(created_by=1)
        subtasks = SubtaskItem.objects.all()
        serializer = SubtaskItemSerializer(subtasks, many=True)
        print(Response(serializer.data))
        return Response(serializer.data)

class AssignedContactView(APIView): 
    authenticaiton_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    #@login_required(login_url="http://127.0.0.1:5500/login.html")
    def get(self, request, format=None):
        assignedContacts = AssignedContactItem.objects.all()
        serializer = AssignedContactItemSerializer(assignedContacts, many=True)
        print(Response(serializer.data))
        return Response(serializer.data)

class ContactsView(APIView): 
    authenticaiton_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    #@login_required(login_url="http://127.0.0.1:5500/login.html")
    def get(self, request, format=None):
        contacts = ContactItem.objects.all()
        serializer = ContactItemSerializer(contacts, many=True)
        print(Response(serializer.data))
        return Response(serializer.data)

class LogoutView(APIView):
    def logout_view(request):
        #if request.method == 'POST':
        #if "logout" in request.body:
        logout(request)
        #Redirect to a success page.
        #return Response({ "status": "OK - User logged out"})
