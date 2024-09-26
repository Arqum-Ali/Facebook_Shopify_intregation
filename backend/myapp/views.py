# facebook_ads/views.py
from django.conf import settings

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FacebookAccessToken
from .serializers import AdAccountSerializer
import requests
# auth_app/views.py

import os
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
# from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from a .env file

# FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
# FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
# FACEBOOK_REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI")
# auth_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import AdAccountSerializer  # Import the serializer

class LoginFacebookView(APIView):
    def get(self, request):
        # Redirect user to Facebook's OAuth login page with additional permissions
        facebook_auth_url = (
            f"https://www.facebook.com/v13.0/dialog/oauth?client_id={settings.FACEBOOK_APP_ID}"
            f"&redirect_uri={settings.FACEBOOK_REDIRECT_URI}&scope=email,ads_read,ads_management"
        )
        return Response({"redirect_url": facebook_auth_url})

class FacebookCallbackView(APIView):
    def get(self, request):
        code = request.GET.get("code")
        token_url = "https://graph.facebook.com/v13.0/oauth/access_token"
        params = {
            "client_id": settings.FACEBOOK_APP_ID,
            "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "code": code,
        }

        # Get the access token
        response = requests.get(token_url, params=params)
        access_token_info = response.json()

        if "access_token" in access_token_info:
            access_token = access_token_info["access_token"]

            # Fetch Facebook Ads accounts using the access token
            ads_url = "https://graph.facebook.com/v13.0/me/adaccounts"
            ads_response = requests.get(ads_url, params={"access_token": access_token})

            # Check if the request to get ads data was successful
            if ads_response.status_code == 200:
                ads_data = ads_response.json()
                
                # Log or print the ads_data for debugging
                print("ads_data--------------",ads_data)

                serializer = AdAccountSerializer(ads_data["data"], many=True)

                return Response({
                    "access_token": access_token,
                    "ads_data": serializer.data
                })
            else:
                return Response({
                    "error": "Failed to retrieve ads data",
                    "details": ads_response.json()
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Failed to retrieve access token", "details": access_token_info}, status=status.HTTP_400_BAD_REQUEST)

class GetCampaignsView(APIView):
    def get(self, request, account_id):
        access_token = request.GET.get("access_token")  # Retrieve the access token
        campaigns_url = f"https://graph.facebook.com/v20.0/act_{account_id}/campaigns"
        params = {
            "access_token": access_token,
            "fields": "id,name,status",
        }
        
        campaigns_response = requests.get(campaigns_url, params=params)
        print("campaigns_response",campaigns_response)
        if campaigns_response.status_code == 200:
            campaigns_data = campaigns_response.json()
            print("campaigns_data",campaigns_data)
            return Response(campaigns_data)
        else:
            return Response({
                "error": "Failed to retrieve campaigns",
                "details": campaigns_response.json()
            }, status=status.HTTP_400_BAD_REQUEST)
