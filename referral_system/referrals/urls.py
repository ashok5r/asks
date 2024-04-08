from django.urls import path
from .views import UserDetailView, ReferralListView
from .views import UserRegistrationView
from .views import UserDetailsView
from .views import ReferralsView

urlpatterns = [
    path('user/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('referrals/', ReferralListView.as_view(), name='referral-list'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/details/', UserDetailsView.as_view(), name='user-details'),
    path('referrals/', ReferralsView.as_view(), name='referrals'),
]