from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
 
from django.contrib.auth import authenticate
 
from .serializers import RegisterSerializer, LoginSerializer
 
 
class RegisterView(APIView):
 

    permission_classes = [AllowAny]
 
    def post(self, request):
     
        serializer = RegisterSerializer(data=request.data)
 
        if not serializer.is_valid():
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        user = serializer.save()
 
        
        token, _ = Token.objects.get_or_create(user=user)
 
        # Step 5: Return success response with the token
        return Response(
            {
                "message": "Account created successfully.",
                "username": user.username,
                "token": token.key,   # This is the string the client will send in headers
            },
            status=status.HTTP_201_CREATED
        )
 
 
class LoginView(APIView):
    
 
    permission_classes = [AllowAny]
 
    def post(self, request):
       
 
        # Step 1: Validate that fields are present and non-empty
        serializer = LoginSerializer(data=request.data)
 
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
 
        # Step 2: Django's authenticate checks username + password
        # Returns a User object on success, or None on failure
        user = authenticate(username=username, password=password)
 
        if user is None:
            # Invalid credentials — don't reveal which field is wrong (security)
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        # Step 3: Retrieve the user's token (or create one if missing)
        token, _ = Token.objects.get_or_create(user=user)
 
        return Response(
            {
                "message": "Login successful.",
                "username": user.username,
                "token": token.key,
            },
            status=status.HTTP_200_OK
        )
 