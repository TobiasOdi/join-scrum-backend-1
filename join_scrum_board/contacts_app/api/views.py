from django.shortcuts import render
import json
from rest_framework.views import APIView, Response
from contacts_app.models import ContactItem
from rest_framework.authentication import TokenAuthentication

class SaveCreatedContactView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        """ Creates a new contact item in the database.
        Args:
            request (json): Contact data
        Returns a string that says "OK - New contact created".
        """
        currentContact = json.loads(request.body)
        #contactData = currentContact[0]['taskData']
        
        ContactItem.objects.create(
            first_name=currentContact['first_name'], 
            last_name=currentContact['last_name'],
            email=currentContact['email'],
            phone=currentContact['phone'],
            color=currentContact['color'],
            text_color=currentContact['text_color'],
            active_user=None
        )
        
        return Response({ "status": "OK - New contact created"})

class SaveChangedContactView(APIView):
    authenticaiton_classes = [TokenAuthentication]
    def post(self, request):
        """ Updates the changed contact item.
        Args:
            request (json): Contact data
        Returns a string that says "OK - Status category updated".
        """
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
        """ Deletes the contact item.
        Args:
            request (json): Contact data
        Returns a string that says "OK - Contact deleted".
        """
        currentContact = json.loads(request.body)
        
        if currentContact['active_user'] == None:
            ContactItem.objects.filter(id=currentContact['id']).delete()
            return Response({ "status": "OK - Contact deleted"})

    
    
    
    
    
    
    