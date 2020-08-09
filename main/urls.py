"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views


from accounts.views import (testpage, login, register, change_password,
                            user_account, logout)
from accounts.urls import urlpatterns as accounts_urls
from accounts.forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    # url patterns for all account functionality
    path('login/', login, name='login'),
    path('login/', login, name='signin'),
    path('register/', register, name='register'),
    path('change_password/', change_password, name='change_password'),
    path('account/', user_account, name='account'),
    path('logout/', logout, name='logout'),
    # url patterns for the forgot password flow
    url(r'^password_reset/$',
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm),
        name='password_reset'),
    url(r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa: E501
        auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm),  # noqa: E501
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    path(r'accounts/', include(accounts_urls)),
    # url patterns for additional django apps
    path('', testpage, name='testpage'),
]

handler404 = 'accounts.views.handler404'
