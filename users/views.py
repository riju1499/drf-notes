from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
 
from django.contrib.auth import authenticate
 
from .serializers import RegisterSerializer, LoginSerializer
 
 
class RegisterView(APIView):
    """
    POST /api/auth/register/
    ─────────────────────────
    Creates a new user account and returns an authentication token.
 
    permission_classes = [AllowAny]
        This OVERRIDES the global IsAuthenticated setting.
        Registration must be publicly accessible — no token needed yet!
    """
 
    # Override global auth requirement — this endpoint is public
    permission_classes = [AllowAny]
 
    def post(self, request):
        """
        Step-by-step flow:
          1. Pass request.data (the incoming JSON) to the serializer
          2. Call is_valid() — this runs all validation methods
          3. If valid, call save() — this calls serializer.create()
          4. Create a Token for the new user
          5. Return the token so the client can start making authenticated requests
        """
 
        # Step 1 & 2: Validate incoming data
        serializer = RegisterSerializer(data=request.data)
 
        if not serializer.is_valid():
            # serializer.errors contains a dict of field: [error messages]
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        # Step 3: Save creates the User in the database
        user = serializer.save()
 
        # Step 4: Create (or retrieve) a token for the new user
        # get_or_create returns (object, created_boolean)
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
    """
    POST /api/auth/login/
    ──────────────────────
    Authenticates a user and returns their token.
 
    We use Django's built-in authenticate() function which:
    - Looks up the username in the database
    - Verifies the password against the stored hash
    - Returns the User object if valid, or None if not
    """
 
    permission_classes = [AllowAny]
 
    def post(self, request):
        """
        Step-by-step flow:
          1. Validate that username and password are present
          2. Use authenticate() to verify credentials
          3. If valid, get or create a Token and return it
          4. If invalid, return a 400 error
        """
 
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
 