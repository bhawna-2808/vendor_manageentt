from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *



"""register api """
class RegisterUserApiview(APIView):
    @staticmethod
    def post(request):
        """Create the User model with given data"""
        try:
            if CustomUser.objects.filter(email=request.data["email"], is_active=True).exists():
                    return Response(
                        data={
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Email already exist",
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            elif CustomUser.objects.filter(mobile_number=request.data["mobile_number"], is_active=True).exists():
                return Response(
                    data={
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Mobile Number already exist",
                        },
                        status=status.HTTP_400_BAD_REQUEST
                )
            elif CustomUser.objects.filter(email=request.data["email"], mobile_number=request.data["mobile_number"], is_active=True).exists():
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Your account has been already exists",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
                  
            elif CustomUser.objects.filter(email=request.data["email"], is_active=False).exists():
                ins_user = CustomUser.objects.filter(email=request.data["email"]).first()
                ins_user.delete()
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    email = serializer.validated_data["email"] 
                    user = CustomUser.objects.get(email=email)
                    token = Token.objects.get_or_create(user=user)[0]
                    return Response(
                        data={
                            "status": status.HTTP_200_OK,
                            "message": "Successfully Signup.",
                            "token":token.key
                            },
                        )
                else:
                    return Response(
                        data={
                            "status": status.HTTP_400_BAD_REQUEST,
                            "error": serializer.errors,
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                            
                    
                    
            elif CustomUser.objects.filter(mobile_number=request.data["mobile_number"], is_active=False).exists():
                ins_user = CustomUser.objects.filter(mobile_number=request.data["mobile_number"]).first()
                ins_user.delete()
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    
                    serializer.save()
                    email = serializer.validated_data["email"] 
                    user = CustomUser.objects.get(email=email)
                    token = Token.objects.get_or_create(user=user)[0]
                    return Response(
                        data={
                            "status": status.HTTP_200_OK,
                            "message": "Successfully Signup.",
                            "token":token.key
                            },
                    )
                else:
                    return Response(
                        data={
                            "status": status.HTTP_400_BAD_REQUEST,
                            "error": serializer.errors,
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                        
            else:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    
                    serializer.save()
                    email = serializer.validated_data["email"] 
                    user = CustomUser.objects.get(email=email)
                    token = Token.objects.get_or_create(user=user)[0]
                   
                    return Response(
                        data={
                            "status": status.HTTP_200_OK,
                            "message": "Successfully Signup.",
                            "token":token.key
                        },
                    )
                    
                else:
                    return Response(
                        data={
                            "status": status.HTTP_400_BAD_REQUEST,
                            "error": serializer.errors,
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        except Exception as ex:
            print("Error in RegisterUserApiview Post method", ex)
            return Response(
                data={
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "error",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            


"""This method is used to Login user"""
@api_view(["POST"])
def login_page(request):
    email = request.data["email"].lower()
    # mobile_number = request.data["mobile_number"]
    password = request.data["password"]
    try:
        user = CustomUser.objects.filter(
         email=email
        ).first()
        if user.check_password(password):
            if user.is_active:
                token = Token.objects.get_or_create(user=user)[0]
                userData = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "mobile_no": user.mobile_number,
                   
                }
                return Response(
                    data = {
                        "status": status.HTTP_200_OK,
                        "auth_token": "%s" % token,
                        "message": "Successfully Login",
                        "userData": userData,
                    }
                )
            else:
                # user.delete()
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "User is not active. Please contact admin..",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    
                )
        else:
            return Response(
                data={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid password...",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    except CustomUser.DoesNotExist:
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST, 
                "message": f"user does not exists with this {email}"
                },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST, 
                "message": f"user does not exists with this {email}"
            },
             status=status.HTTP_400_BAD_REQUEST
        )  
