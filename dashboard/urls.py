from django.urls import path
from dashboard.views import Dashboard
urlpatterns = [
    path('dashboard',Dashboard.as_view(),name='dashboard'),

]