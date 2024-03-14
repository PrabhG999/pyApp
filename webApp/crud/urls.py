#App level Urls
from django.urls import path
from .views import UserSignUpView, UserLoginView, CrudViewset, buy_car

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('crud/', CrudViewset.as_view(), name='crud-list-create'),
    path('crud/<int:id>/', CrudViewset.as_view(), name='crud-update-delete'),
    path('buy-car/<int:car_id>/', buy_car, name='buy-car'),
]
