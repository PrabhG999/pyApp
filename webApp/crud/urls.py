# crud app endpoints
# import statements are important
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView  # login view import

urlpatterns = [
    # This URL will match a GET or POST request without an ID.
    path('crud/', views.CrudViewset.as_view()),

    # This URL will match GET, PATCH, and DELETE requests with an ID.
    path('crud/<int:id>/', views.CrudViewset.as_view()),

    # Add paths for user registration and login
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Path to buy car
    path('buy-car/<int:car_id>/', views.buy_car, name='buy-car'),
]
