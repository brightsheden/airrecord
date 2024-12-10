from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from base.serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def register(request):
    data = request.data
    if not data:
        return Response({"message": "email and username is compulsory"}, status=status.HTTP_400_BAD_REQUEST)
    
    email = data.get('email')
    username = data.get('username')
    user_type = data.get("user_type")
    password = data.get('password')

    user = User.objects.create(
        email=email,
        username=username,
        user_type= user_type,
        password = make_password(password)

    )

    serializer = UserSerializerWithToken(user)

    return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(['GET'])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_all_equipment(request):
    equipment = Equipment.objects.all()
    serializer = EquipmentSerializer(equipment, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_equipment(request):
    data=request.data
    print(data)
    serializer = EquipmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_equipment(request, pk):
    try:
        user = request.user
        if user.user_type != 'user':
            return Response({"message":"You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        equipment = Equipment.objects.get(pk=pk)
    except Equipment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_equipment_by_id(request, pk):
    try:
        equipment = Equipment.objects.get(pk=pk)
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data)
    except Equipment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_equipment(request, pk):
    equment = Equipment.objects.get(pk=pk)
    equment.delete()
    return Response("Deleted")