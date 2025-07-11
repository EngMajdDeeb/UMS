from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacultyViewSet, FacultyQualificationViewSet, FacultyLeaveViewSet

router = DefaultRouter()
router.register(r'faculty', FacultyViewSet)
router.register(r'qualifications', FacultyQualificationViewSet)
router.register(r'leaves', FacultyLeaveViewSet)

urlpatterns = [
    path('', include(router.urls)),
]