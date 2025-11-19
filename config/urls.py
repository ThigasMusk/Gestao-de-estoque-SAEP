"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from estoque import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 4. Autenticação (Login/Logout)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # 5. Principal
    path('', views.home, name='home'),
    
    # 6. Produtos
    path('produtos/', views.produto_lista, name='produto_lista'),
    path('produtos/novo/', views.produto_criar, name='produto_criar'),
    path('produtos/editar/<int:pk>/', views.produto_editar, name='produto_editar'),
    path('produtos/deletar/<int:pk>/', views.produto_deletar, name='produto_deletar'),
    
    # 7. Estoque
    path('estoque/', views.gestao_estoque, name='gestao_estoque'),
]