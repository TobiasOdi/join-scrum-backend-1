from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from main.models import UserAccount
from contacts.models import ContactItem
import time
import calendar;
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework.views import Response

def returnUserData(upass, get_user, request, user):
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
    
def createObjectsForGuestUser(newUserData, upass):
    print('User does not exist')            
    new_user = User.objects.create_user(
        username=newUserData['email'],
        password=newUserData['password'],
        email=newUserData['email'],
        first_name=newUserData['first_name'],
        last_name=newUserData['last_name']
    )
    new_user.set_password(upass)
    new_user.save()
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
    
def returnGuestUserData(upass, get_user, request, user, newUserData):
    token, created = Token.objects.get_or_create(user=user)
    check_pass = check_password(upass, get_user[0].password)
    login(request, user)
    return JsonResponse({
        "id": user.pk,
        "username": user.username,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "email": user.email,
        "userColor": newUserData['color'],
        "token": token.key
    })

def createObjectsForNewUser(newUserData):
    new_user = User.objects.create_user(
        username=newUserData['email'],
        password=newUserData['password'],
        email=newUserData['email'],
        first_name=newUserData['first_name'],
        last_name=newUserData['last_name']
    )
    new_user.set_password(newUserData['password'])
    new_user.save()
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

def sendEmail(email, request):
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    user = User.objects.get(username=email)
    token, created = Token.objects.get_or_create(user=user)
    subject = "Password Reset request"
    message = render_to_string("email_template_pw_reset.html", {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': user.pk,
        'token': token,
        'ts': ts,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    try:
        mail = send_mail(
            subject, 
            message, 
            from_email='jointeam@gmx.net',
            recipient_list = [email,], 
            fail_silently=False)
        return Response({ "status": 3})

    except NameError:
        print("Problem sending reset password email", NameError)
        return Response({ "status": 2})

