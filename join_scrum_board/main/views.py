from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import json
from main.models import UserAccount
from add_task.models import TaskItem, SubtaskItem, AssignedContactItem
from contacts.models import ContactItem
from rest_framework.views import APIView, Response
from add_task.serializers import TaskItemSerializer, SubtaskItemSerializer, AssignedContactItemSerializer
from contacts.serializers import ContactItemSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

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
    def post(self, request, format=None):
        email = request.POST['email']
        upass = request.POST['password']
        user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
        get_user_obj = User.objects.filter(username=email).exists()
        pass
        if get_user_obj:
            get_user=User.objects.filter(username=email)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                check_pass = check_password(upass, get_user[0].password)
                login(request, user)
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
                
            else:
                print(f"Password dose not exist with username = {get_user[0].username}")
                return JsonResponse({"status": 1})
            
        else:
            print('Username dose not exist')
            return JsonResponse({"status": 2 })

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
    def get(self, request, format=None):
        #tasks = TaskItem.objects.filter(created_by=request.user)
        #tasks = TaskItem.objects.filter(created_by=1)
        tasks = TaskItem.objects.all()
        serializer = TaskItemSerializer(tasks, many=True)
        print(Response(serializer.data))
        return Response(serializer.data)

class SubtasksView(APIView): 
    authenticaiton_classes = [TokenAuthentication]
    def get(self, request, format=None):
        subtasks = SubtaskItem.objects.all()
        serializer = SubtaskItemSerializer(subtasks, many=True)
        print(Response(serializer.data))
        return Response(serializer.data)

class AssignedContactView(APIView): 
    authenticaiton_classes = [TokenAuthentication]
    def get(self, request, format=None):
        assignedContacts = AssignedContactItem.objects.all()
        serializer = AssignedContactItemSerializer(assignedContacts, many=True)
        print(Response(serializer.data))
        return Response(serializer.data)

class ContactsView(APIView): 
    authenticaiton_classes = [TokenAuthentication]
    def get(self, request, format=None):
        contacts = ContactItem.objects.all()
        serializer = ContactItemSerializer(contacts, many=True)
        print(Response(serializer.data))
        return Response(serializer.data)

"""
class LogoutView(APIView):
    def logout_view(request):
        #if request.method == 'POST':
        #if "logout" in request.body:
        logout(request)
        #Redirect to a success page.
        #return Response({ "status": "OK - User logged out"})
"""
       

class PasswordResetView(APIView):
    def post(self, request):
        email = request.POST['email']
        get_user_obj = User.objects.filter(username=email).exists()
        if get_user_obj:
            user = User.objects.get(username=email)
            token, created = Token.objects.get_or_create(user=user)
            subject = "Password Reset request"
            print("USER ID", user.pk)
            pass
            message = render_to_string("email_template_pw_reset.html", {
                'user': user.first_name,
                'domain': get_current_site(request).domain,
                'uid': user.pk,
                #'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #'token': default_token_generator.make_token(user),
                'token': token,
                "protocol": 'https' if request.is_secure() else 'http'
            })
            print(message)
            try:
                mail = send_mail(
                    subject, 
                    message, 
                    from_email='tobias.odermatt@gmx.net',
                    recipient_list = [email,], 
                    fail_silently=False)
                print(mail)
                return Response({ "status": 3})

            except NameError:
                print("Problem sending reset password email", NameError)
                return Response({ "status": 2})
        else:
            return Response({ "status": 1})


"""
def password_reset_request(request):
    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset.html", 
        context={"form": form}
        )
"""

"""
class PasswordResetConfirmView(APIView):
    def passwordResetConfirm(request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            print("UID", uid)
            user = User.objects.get(pk=uid)
            print("USER", user)

            user_with_token = Token.objects.get(user=user)
            print("USER TOKEN", user.token)
            print("USER WITH TOKEN", user_with_token)
        except:
            user = None

        if user is not None and token == user_with_token:
            if request.method == 'POST':
                # Redirect to change password html
                return Response({ "status": 1})
        else:
            print(request, "Link is expired")
            return Response({ "status": 2})

        pass
        print(request, 'Something went wrong, redirecting back to Homepage')
        return Response({ "status": 3})
"""
class SetNewPasswordView(APIView):
    def post(self, request):
        newPassword = request.POST['newPw']
        uid = request.POST['uid']
        get_user_obj = User.objects.filter(pk=uid)
        if get_user_obj:
            user = User.objects.get(pk=uid)
            print("PASSWORT VOR", get_user_obj[0].password)
            get_user_obj[0].set_password(newPassword)
            get_user_obj[0].save()          
            #usernewPW = User.objects.filter(pk=uid).update(
            #    password=newPassword,
            #)
            print("PASSWORT NACH", get_user_obj[0].password)
            return JsonResponse({"status": 1})
        else:
            print('User dose not exist')
            return JsonResponse({"status": 2})
