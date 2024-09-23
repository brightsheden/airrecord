from rest_framework import serializers
from base.models import *
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)
  
  
    class Meta:
        model = User
        fields = ['id','username','email','user_type',  'isAdmin', 'is_emailverified', 'createdAt']

    def get_isAdmin(self,obj):
        return obj.is_staff
    

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['username','email','user_type',"isAdmin", 'token']

    def get_token(self, obj):
        token =RefreshToken.for_user(obj)
        return str(token.access_token)
    

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Equipment
        fields = "__all__"
