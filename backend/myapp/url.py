# auth_app/urls.py

from django.urls import path
from .views import LoginFacebookView, FacebookCallbackView, GetCampaignsView

urlpatterns = [
    path('login/facebook/', LoginFacebookView.as_view(), name='login_facebook'),
    path('callback/', FacebookCallbackView.as_view(), name='callback'),
    path('adaccounts/<str:account_id>/campaigns/', GetCampaignsView.as_view(), name='get_campaigns'),  # New URL for fetching campaigns
]
