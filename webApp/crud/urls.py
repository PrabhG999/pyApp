from django.urls import path
from . import views

urlpatterns = [
    path('api/signup/', views.UserSignUpView.as_view(), name='api-signup'),
    path('api/login/', views.UserLoginView.as_view(), name='api-login'),
    path('api/crud/', views.CrudViewset.as_view(), name='crud-list-create'),
    path('api/crud/<int:id>/', views.CrudViewset.as_view(), name='crud-update-delete'),
    path('api/buy-car/<int:car_id>/', views.buy_car, name='buy-car'),
]