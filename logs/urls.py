from django.urls import path
from . import views

urlpatterns=[
    
    path('signin', views.validate_user, name='validate-user'),
    path('signup', views.add_user, name='add-user'),
    #path('get', views.get_user, name='get-user'),
    path('update', views.update_info, name='update-info'),
    path('deactivate', views.delete_user, name='delete-user'),
    #path('listing_users', views.get_user_list, name='listing-users'),
    path('generate_otp', views.generate_otp, name='generate-otp'),
    path('verify_otp', views.verify_otp, name='verify-otp'),
    path('reset_password', views.reset_password, name='reset-password'),

]