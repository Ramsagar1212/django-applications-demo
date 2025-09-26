from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user




class StudentSerializer(serializers.ModelSerializer):
    # age = serializers.IntegerField(default=18, validators=[MinValueValidator(18),MaxValueValidator(80)])
    class Meta:
        model = Student
        fields =  '__all__'
        # exclude = ['id','name']

    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError({"error": "age is not less than 18"})
        
        if data['name']:
            for n in data['name']:
                if n.isdigit():
                    raise serializers.ValidationError({'errors ':"name cannot be numeric"})
        
        return data
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =  ['category_name',]
    
    
class BookSerializer(serializers.Serializer):
    category = CategorySerializer()
    class Meta:
        model = Book
        fields =  '__all__'
        
        