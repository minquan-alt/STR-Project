from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('',views.home, name='home'),
    path('product/<str:pk>', views.product, name='product'),
    path('create-product/', views.createProduct, name="create-product"),
    path('update-product/<str:pk>/', views.updateProduct, name="update-product"),
    path('delete-product/<str:pk>/', views.deleteProduct, name="delete-product"),
    path('delete-remarkable/<str:pk>/', views.deleteRemarkable, name="delete-remarkable"),
    path('update-remarkable/<str:pk>/', views.updateRemarkable, name="update-remarkable"),
    path('purchase-product/<int:pk>/', views.purchaseProduct, name='purchase-product'),
    path('pay-a-bill/', views.pay_a_bill, name='pay-a-bill'),
]