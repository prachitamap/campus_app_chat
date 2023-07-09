from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message, ChatSession
from logs.models import CUser
from .serializers import MessageSerializer,ChatSessionSerializer
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django.utils import timezone
from knox.auth import TokenAuthentication
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json
from knox.models import AuthToken
from .utils import CustomJSONEncoder
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import UnsupportedMediaType
from json.decoder import JSONDecodeError
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
import json
from .utils import CustomJSONEncoder
from django.core.serializers import serialize
from django.contrib.auth import get_user_model


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_chat_session(request):
    buyer_id = request.user.id
    seller_id = int(request.data['seller_id'])
    
    if buyer_id == seller_id:
        return Response({'seller': 'seller ID is same as buyer ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        seller = CUser.objects.get(id=seller_id)
        # 
        # seller_name = CUser.objects.get(username=CUser.username)
        by = CUser.objects.get(id=buyer_id)
    except ObjectDoesNotExist:
        return Response({'seller': 'seller ID not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ch = ChatSession.objects.get(buyer=by.email, seller=seller)
    except ChatSession.DoesNotExist:
        ch = ChatSession(buyer=by.email, seller=seller)
        ch.save()
    seller = CUser.objects.get(id=seller_id)
    seller_name=seller.first_name
    expiry = timedelta(days=3)
    token = str(AuthToken.objects.create(request.user, expiry=expiry))
    
    resp = {
        'session_id': ch.id,
        'seller_name':seller_name,
    }
    return JsonResponse(resp, status=status.HTTP_201_CREATED, encoder=CustomJSONEncoder)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chat_list(request):
    sessions = ChatSession.objects.all()
    session_list = []
    for session in sessions:
        
        seller_emails= session.seller
        seller = CUser.objects.get(email=seller_emails)
        seller_username=seller.username  
        session_list.append({'username': seller_username},)
        # session_list=session_list + list({'username':seller_username}) 
        

    return JsonResponse(session_list, safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chat_details(request):
    seller_id = int(request.data['seller_id'])
    seller = CUser.objects.get(id=seller_id)
    seller_name= seller.first_name
    

        # by = CUser.objects.get(id=buyer_id)
        # buyer_username= by.username 
    resp= {'seller_name': seller_name,}
         
        

    return JsonResponse(resp, status=status.HTTP_201_CREATED, encoder=CustomJSONEncoder)
