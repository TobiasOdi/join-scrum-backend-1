from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from rest_framework.views import APIView, Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from user_auth_app.models import PwResetTimestamp
from user_auth_app.serializers import PwResetTimestampSerializer
from user_auth_app.api.helpers import *

class TokenCheckView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request, format=None):
        """ Checks if the token already exists.
        Args:
            request (json): Token data
        Returns a jason with the status 1 (token exists) or 2 (token does not exist).
        """
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
        """ Logs the user into his account or return a json with the status 1(Incorrect password) or 2(User does not exist).
        Args:
            request (string): E-Mail and Password
        """
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
        """ Logs in the Guest user. If the Guest user does not already exist, the user is created.
        Args:
            request (json): User data of the Guest user
        """
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
        """ Checks if the username (email) already exist, if not the user is created.
        If the username already exists, it returns a json with the status 1.
        Args:
            request (json): New user data
        """
        newUserData = json.loads(request.body)
        get_user_obj = User.objects.filter(username=newUserData['email']).exists()
        if get_user_obj:
            return JsonResponse({
                "status": 1
            })
        else:          
            createObjectsForNewUser(newUserData)
            return Response({ "status": "OK - New user and contact created"})

class GetTimestampView(APIView): 
    def get(self, request, user_id):
        """Returns the timestamp that has been set, by resetting tha password (sending mail).
        Args:
            user_id (int): Id of the user
        """
        user= User.objects.get(pk=user_id)      
        if PwResetTimestamp.objects.filter(user=user):
            user_timestamp = PwResetTimestamp.objects.filter(user=user)
            serializer = PwResetTimestampSerializer(user_timestamp[0])
            return Response(serializer.data)
        else:
            print("No timestamp entry")
            return Response("OK")  

class SetTimestampView(APIView):
    #authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        """ Saves the timestamp after resetting the timestamp.
        Args:
            request (json): User id and timestamp
        """
        data = json.loads(request.body)
        user = User.objects.filter(pk=data['user_id'])      
       
        if PwResetTimestamp.objects.filter(user=user[0]):
            PwResetTimestamp.objects.filter(user=user[0]).update(
                timestamp=data['timestamp'],
            )    
            return Response({ "status": "OK - Timestamp set"})
        else:
            PwResetTimestamp.objects.create(
                user=user[0],
                timestamp=data['timestamp'],
            )    
            return Response({ "status": "OK - Timestamp set"})

class PasswordResetView(APIView):
    def post(self, request):
        """ Checks if the user that wants to reset the password eixists and sends an email to reset the password.
        If the user does not exist, it returns a json with the status 1.
        """
        email = request.POST['email']
        get_user_obj = User.objects.filter(username=email).exists()
        if get_user_obj:
            return sendEmail(email, request)
        else:
            return Response({ "status": 1})

class SetNewPasswordView(APIView):
    def post(self, request):
        """ Sets the new user password if the user exists and returns a json with the status 1(new password set).
        If the user does not exist, returns a json with the status 2(user does not exist).
        Args:
            request (form): User id and password

        Returns:
            _type_: _description_
        """
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