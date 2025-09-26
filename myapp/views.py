from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.views import Token
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import viewsets



class StudentGeneric(generics.ListAPIView, generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    
# ModelViewSet - is a class based view that automatically provides complete set of CRUD action for a given model
class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer




class StudentViewSet(viewsets.ViewSet):
    
    def list(self, request):
        student_obj = Student.objects.all()
        serializer = StudentSerializer(student_obj, many=True) 
        return Response(serializer.data)



    def create(self,request):
        serializer=StudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response({'message': 'Data created', 'payload': serializer.data})



@api_view(['GET'])
def get_book(request):
    book_object = Book.objects.all()
    serialer = BookSerializer(book_object, many=True)
    return Response({'status':200,'payload':serialer.data})



class RegisterAPI(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        if not username or not password:
            return Response({'error': 'username and password is required'})
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"})
        
        user = User.objects.create_user(username=username, password=password)
        # token, created = Token.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)
         
        return Response({
            'status':200,
            'payload':user.data,
            "refresh":str(refresh),
            "access": str(refresh.access_token),
            'message':'user registration is successfull'
        })
        
        
        
        # serializer = UserSerializer(data = request.data)
        # if not serializer.is_valid():
        #     return Response({'status':403,'error':serializer.errors, 'message':'something went wrong'})    
        # serializer.save()
        
        # user = User.objects.get(usename = serializer.data['username'])
        # refresh = RefreshToken.for_user(user)
         
        # return Response({
        #     'status':200,
        #     'payload':serializer.data,
        #     "refresh":str(refresh),
        #     "access": str(refresh.access_token),
        #     'message':'user registration is successfull'})



class StudentAPI(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    
    def get(self, request):
        student_object = Student.objects.all()
        
        #todo -- PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 3
        final_page = paginator.paginate_queryset(student_object, request)
        
        #todo --- limitoffsetPagination
        # paginator = LimitOffsetPagination()
        # final_page = paginator.paginate_queryset(student_object, request)
        
    
        serializer = StudentSerializer(final_page, many=True)
        return Response({'status': 200, 'payload': serializer.data})

    
    def post(self, request):
        # phone=6667
        data = request.data


        # new_data = data.copy()
        # new_data['phone'] = phone
        # serializer = StudentSerializer(data=new_data)
        # content = {'phone': 23423}
        
        
        serializer = StudentSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({'status':404,'error':serializer.errors, 'message':'something went wrong'})    
        serializer.save()
        
        return Response({'status':200,'payload':serializer.data,'message':'you sent'})
    

    
    def patch(self, request):
        try:
            student_object = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializer(student_object,data=request.data, partial=True)
    
            if not serializer.is_valid():
                return Response({'status':403,'error':serializer.errors, 'message':'something went wrong'})    
            serializer.save()
            return Response({'status':200,'payload':serializer.data,'message':'your data is updated at this {{id}}'})
            
        except Exception as e:
            return Response({'status':403,'message':'invalid id'}) 
        
    
    def put(self, request):
        try:
            student_object = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializer(student_object,data=request.data)
    
            if not serializer.is_valid():
                return Response({'status':403,'error':serializer.errors, 'message':'something went wrong'})    
            serializer.save()
            return Response({'status':200,'payload':serializer.data,'message':'your data is updated at this {{id}}'})
            
        except Exception as e:
            return Response({'status':403,'message':'invalid id'}) 
        
    
    
    def delete(self, request):
        try:
            student_object = Student.objects.get(id=request.data['id'])
            student_object.delete()
            return Response({'status':200,'message': 'successfully deleted'})
            
        except Exception as e:
            return Response({'status':403,'message':'invalid id'})
        
        
    
    
    
# @api_view(['GET'])
# def home(request):
#     student_object = Student.objects.all()
#     serializer = StudentSerializer(student_object, many=True)
#     return Response({'status': 200, 'payload': serializer.data})


# @api_view(['POST'])
# def post_student(request):
#     data = request.data
#     serializer = StudentSerializer(data=data)
    
#     if not serializer.is_valid():
#         return Response({'status':404,'error':serializer.errors, 'message':'something went wrong'})    
#     serializer.save()
#     return Response({'status':200,'payload':serializer.data,'message':'you sent'})


# @api_view(['PUT'])
# def update_student(request, id):
#     try:
#         student_object = Student.objects.get(id=id)
#         serializer = StudentSerializer(student_object,data=request.data, partial=True)
        
#         if not serializer.is_valid():
#             return Response({'status':403,'error':serializer.errors, 'message':'something went wrong'})    
#         serializer.save()
#         return Response({'status':200,'payload':serializer.data,'message':'you sent'})
        
#     except Exception as e:
#         return Response({'status':403,'message':'invalid id'}) 
    
    



# @api_view(['DELETE'])
# def delete_student(request, id):
#     try:
#         student_object = Student.objects.get(id=id)
#         student_object.delete()
#         return Response({'status':200,'message': 'successfully deleted'})
        
#     except Exception as e:
#         return Response({'status':403,'message':'invalid id'})