from django.urls import path 
from .views import dashboard
from . import views


urlpatterns = [
    path('dashboard/', dashboard, name='client-dashboard'),
    path('browse-articles/', views.browse_articles, name='browse-articles'),
    path('subscribe-plan/', views.subscribe_plan, name='subscribe-plan'),
    path('create-subscription/<str:sub_id>/<str:plan>', views.create_subscription, name='create-subscription'),
    path('update-client/', views.update_client, name='update-client'),
]