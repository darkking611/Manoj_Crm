from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.loginPage,name ='login'),
    path('logout/',views.logoutUser,name ='logout'),
    path('user/',views.userPage,name ='userpage'),
    path('register/',views.registerPage,name ='register'),
    path('about/',views.about,name ='about'),
    path('products/',views.products,name='products'),
    path('customers/<str:pk>/',views.customers,name='customer'),
    path('create-order/<str:pk>/',views.createOrder,name='createorder'),
    path('update-order/<str:pk>/',views.updateOrder,name='updateorder'),
    path('delete-order/<str:pk>/',views.deleteOrder,name='deleteorder'),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name ='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(),name ='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name ='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(),name ='password_reset_complete'),
]