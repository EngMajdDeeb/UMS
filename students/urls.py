from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, StudentViewSet, StudentAcademicRecordViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'students', StudentViewSet)
router.register(r'academic-records', StudentAcademicRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]