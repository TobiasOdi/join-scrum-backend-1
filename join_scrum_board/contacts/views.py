from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView, Response# Create your views here.
from contacts.models import ContactItem
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication

class SaveCreatedContactView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        currentContact = json.loads(request.body)
        #contactData = currentContact[0]['taskData']
        
        ContactItem.objects.create(
            first_name=currentContact['first_name'], 
            last_name=currentContact['last_name'],
            email=currentContact['email'],
            phone=currentContact['phone'],
            color=currentContact['color'],
            active_user=None
        )
        
        return Response({ "status": "OK - New contact created"})

class SaveChangedContactView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        currentContact = json.loads(request.body)
        
        ContactItem.objects.filter(pk=currentContact['id']).update(
            first_name=currentContact['first_name'],
            last_name=currentContact['last_name'],
            email=currentContact['email'],
            phone=currentContact['phone']
        )      
        return Response({ "status": "OK - Status category updated"})

class DeleteContactView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        currentContact = json.loads(request.body)
        
        if currentContact['active_user'] == None:
            ContactItem.objects.filter(id=currentContact['id']).delete()
            return Response({ "status": "OK - Contact deleted"})

    
    
    
    
    
    
    