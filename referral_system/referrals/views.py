from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from .models import Referral
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ReferralSerializer
from .models import UserSerializer
from .models import UserProfile
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

class ReferralListView(generics.ListAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        user_serializer = UserRegistrationSerializer(data=request.data)
        profile_serializer = UserProfileSerializer(data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            profile_data = {
                'user': user.id,
                'name': profile_serializer.validated_data.get('name'),
                'referral_code': profile_serializer.validated_data.get('referral_code')
            }
            profile = UserProfile.objects.create(**profile_data)

            # Check for referral code and award points if applicable
            referral_code = profile_serializer.validated_data.get('referral_code')
            if referral_code:
                # Implement logic to award points to the referring user

                return Response({'user_id': user.id, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            errors = {}
            errors.update(user_serializer.errors)
            errors.update(profile_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReferralsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        referral_code = user_profile.referral_code

        if referral_code:
            referred_users = UserProfile.objects.filter(referral_code=referral_code)
            serializer = UserProfileSerializer(referred_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No referrals found'}, status=status.HTTP_404_NOT_FOUND)