from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('student-details', StudentView, basename='student-details')
router.register('studentview',StudentViewSet, basename='student-view')

urlpatterns = [
    path('student/', StudentAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('get-book/', get_book),
    path('generic-student/', StudentGeneric.as_view()),
     path('', include(router.urls)),
    # path('',home),
    # path('student/', post_student),
    # path('update-student/<id>/', update_student),
    # path('delete-student/<id>/', delete_student),
]   