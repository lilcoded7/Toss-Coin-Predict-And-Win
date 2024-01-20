from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from accounts.serializers import *
from accounts.middlewares import UserMiddlewares
from rest_framework.response import Response 
from accounts.models import Verification
from rest_framework import status


User = get_user_model()
# Create your views here.


class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response({"message": "Account created successfully"}, 201)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        user = UserMiddlewares.getUserByEmailOrUsername(
			email=validated_data["email"],
			password=validated_data["password"],
		)

        if user:
            token = RefreshToken.for_user(user)
            return Response(
				{
					"message": "Login successful",
					"token": {
						"access": str(token.access_token),
						"refresh":str(token) 
					},
					"data": RegisterSerializer(user).data
				},
				status=status.HTTP_201_CREATED,
                
			)
        else:
            return Response(
                {'message':'enter correct email and password'}, 404
            )

		
