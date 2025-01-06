from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
import time
import calendar;
from main.models import PwResetTimestamp
from add_task.models import TaskItem, SubtaskItem, AssignedContactItem, CategoryItem
from contacts.models import ContactItem
from rest_framework.views import APIView, Response
from add_task.serializers import TaskItemSerializer, SubtaskItemSerializer, AssignedContactItemSerializer, CategoryItemSerializer
from main.serializers import PwResetTimestampSerializer
from contacts.serializers import ContactItemSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from main.helpers import *

class TokenCheckView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, format=None):
        tokenData = json.loads(request.body)
        token = tokenData['token']
        existingToken = Token.objects.filter(key=token).exists()
        if(existingToken):
            return JsonResponse({"status": 1})
        else:
            return JsonResponse({"status": 2})   
    
class LoginView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, format=None):
        email = request.POST['email']
        upass = request.POST['password']
        user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
        get_user_obj = User.objects.filter(username=email).exists()

        if get_user_obj:
            get_user=User.objects.filter(username=email)
            if user:
                return returnUserData(upass, get_user, request, user)
            else:
                print(f"Password dose not exist with username = {get_user[0].username}")
                return JsonResponse({"status": 1})   
        else:
            print('Username dose not exist')
            return JsonResponse({"status": 2 })

class GuestLoginView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, format=None):
        newUserData = json.loads(request.body)       
        email = newUserData['email']
        upass = newUserData['password']
        get_user_obj = User.objects.filter(username=email).exists()

        if not get_user_obj:
            createObjectsForGuestUser(newUserData, upass)
    
        user = authenticate(username=email, password=upass)
        get_user=User.objects.filter(username=email)
        
        return returnGuestUserData(upass, get_user, request, user, newUserData)

class SignUpView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, format=None):
        newUserData = json.loads(request.body)
        get_user_obj = User.objects.filter(username=newUserData['email']).exists()
        if get_user_obj:
            return JsonResponse({
                "status": 1
            })
        else:          
            createObjectsForNewUser(newUserData)
            return Response({ "status": "OK - New user and contact created"})

class DataView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def get(self, request, format=None):
        tasks = TaskItem.objects.all()
        task_serializer = TaskItemSerializer(tasks, many=True)
        subtasks = SubtaskItem.objects.all()
        subtasks_serializer = SubtaskItemSerializer(subtasks, many=True)
        assignedContacts = AssignedContactItem.objects.all()
        assignedContacts_serializer = AssignedContactItemSerializer(assignedContacts, many=True)
        contacts = ContactItem.objects.all()
        contacts_serializer = ContactItemSerializer(contacts, many=True)
        categories = CategoryItem.objects.all()
        categories_serializer = CategoryItemSerializer(categories, many=True)       
        return Response(
            {
                'tasks': task_serializer.data,
                'subtasks': subtasks_serializer.data,
                'assignedContacts': assignedContacts_serializer.data,
                'contacts': contacts_serializer.data,
                'categories': categories_serializer.data
            })       

class CategoriesView(APIView): 
    authenticaiton_classes = [TokenAuthentication]
    def get(self, request, format=None):
        categories = CategoryItem.objects.all()
        serializer = CategoryItemSerializer(categories, many=True)
        return Response(serializer.data)  

class SetCategoriesView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        categories = json.loads(request.body)      

        for category in categories: 
            CategoryItem.objects.create(
                categoryName = category['categoryName'],
                color = category['color'],
                categoryType = category['categoryType']
            )
        return Response({ "status": "OK - Categories saved in database"})

class GetTimestampView(APIView): 
    def get(self, request, user_id):
        user= User.objects.get(pk=user_id)      
        if PwResetTimestamp.objects.filter(user=user):
            user_timestamp = PwResetTimestamp.objects.filter(user=user)
            print(user_timestamp)
            serializer = PwResetTimestampSerializer(user_timestamp[0])
            return Response(serializer.data)
        else:
            print("No timestamp entry")
            return Response("OK")  

class SetTimestampView(APIView):
    #authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.filter(pk=data['user_id'])      
       
        if PwResetTimestamp.objects.filter(user=user[0]):
            PwResetTimestamp.objects.filter(user=user[0]).update(
                timestamp=data['timestamp'],
            )    
            return Response({ "status": "OK - Timestamp loaded"})
        else:
            PwResetTimestamp.objects.create(
                user=user[0],
                timestamp=data['timestamp'],
            )    
            return Response({ "status": "OK - Timestamp loaded"})

class PasswordResetView(APIView):
    def post(self, request):
        email = request.POST['email']
        get_user_obj = User.objects.filter(username=email).exists()
        if get_user_obj:
            return sendEmail(email, request)
        else:
            return Response({ "status": 1})

class SetNewPasswordView(APIView):
    def post(self, request):
        newPassword = request.POST['newPw']
        uid = request.POST['uid']
        pass
        get_user_obj = User.objects.filter(pk=uid)
        if get_user_obj:
            user = User.objects.get(pk=uid)
            get_user_obj[0].set_password(newPassword)
            get_user_obj[0].save()          
            return JsonResponse({"status": 1})
        else:
            print('User dose not exist')
            return JsonResponse({"status": 2})



