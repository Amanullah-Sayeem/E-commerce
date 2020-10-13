from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('signup/',views.signup_view, name='signup'),
	path('login/',views.login_view, name='login'),
	path('logout/',views.logout_view, name='logout'),
	path('cart/', views.cart, name="cart"),
	path('product/<str:pk>/', views.product, name="product"),
]