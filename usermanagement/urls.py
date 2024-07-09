from django.urls import path
from usermanagement import views
from utils import token_authentication_required

urlpatterns = [
    path('registration/', views.UserResistrationView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('getallusers/', token_authentication_required(views.GetAllUsers.as_view())),
    path('createuser/', views.CreateUser.as_view()),
    path('getuser/<int:pk>/', views.GetUser.as_view()),
    path('edituser/<int:pk>/', views.UpdateUser.as_view()),
    path('deleteuser/<int:pk>/', views.DeleteUser.as_view()),
    # path('hello/', token_authentication_required(printView.as_view()))
]
