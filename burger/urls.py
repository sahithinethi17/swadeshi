from django.contrib import admin
from django.urls import path, include
from burger import views
from .views import*
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:cid>/', views.showcategory, name='category'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'logout.html'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('emptycart/', views.show_cart, name='emptycart'),
    path('pluscart/', views.pluscart),
    path('minuscart/', views.minuscart),
    path('checkout/', views.checkout, name='checkout'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)