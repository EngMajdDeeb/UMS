from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CourseOfferingViewSet, StudentEnrollmentViewSet, AssignmentViewSet, StudentAssignmentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'offerings', CourseOfferingViewSet)
router.register(r'enrollments', StudentEnrollmentViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'student-assignments', StudentAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]