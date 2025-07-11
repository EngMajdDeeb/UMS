from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeanViewSet, DeanshipDecisionViewSet, DeanshipMeetingViewSet, DepartmentBudgetViewSet, DeanshipReportViewSet

router = DefaultRouter()
router.register(r'deans', DeanViewSet)
router.register(r'decisions', DeanshipDecisionViewSet)
router.register(r'meetings', DeanshipMeetingViewSet)
router.register(r'budgets', DepartmentBudgetViewSet)
router.register(r'reports', DeanshipReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]