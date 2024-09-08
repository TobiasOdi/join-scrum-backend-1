from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
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
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
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
        if get_user_obj:
            if user:
                token, created = Token.objects.get_or_create(user=user)
            get_user=User.objects.filter(username=email)
            print("get_user", get_user)

            check_pass = check_password(upass, get_user[0].password)
            print("check_pass", check_pass)
            if not check_pass:
                print(f"Password dose not exist with username = {get_user[0].username}")
                return JsonResponse({
                    #"id": request.id,
                    "status": 1
                })
            else:
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
            print('Username dose not exist')
            return JsonResponse({
                #"id": request.id,
                "status": 2
            })

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
    def password_reset(request):
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                user_email = form.cleaned_data['email']
                associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
                if associated_user:
                    subject = "Password Reset request"
                    message = render_to_string("template_reset_password.html", {
                        'user': associated_user,
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                        #'token': default_token_generator.make_token(associated_user),
                        'token': Token.objects.get(user=associated_user),
                        "protocol": 'https' if request.is_secure() else 'http'
                    })
                    try:
                        mail = send_mail(subject, message, to=[associated_user.email])
                        mail.success(request,
                            
                            #<h2>Password reset sent</h2><hr>
                            #<p>
                            #    We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            #    You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            #    you registered with, and check your spam folder.
                            #</p>
                            
                        )
                        return Response({ "status": 2})

                    except:
                        mail.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")
                else:
                    return Response({ "status": 1})

        #for key, error in list(form.errors.items()):
            # if key == 'captcha' and error[0] == 'This field is required.':
            #     messages.error(request, "You must pass the reCAPTCHA test")
               
        

        form = PasswordResetForm()
        return render(request=request, template_name="password_reset.html", context={"form": form})


"""@user_not_authenticated
def password_reset_request(request):
    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    return redirect("homepage")
"""