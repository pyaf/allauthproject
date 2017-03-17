from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout
from .views import (RegisterView, DashboardView,
                    LoginView, PhoneVerificationView,
                    IndexView )

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="register_url"),
    # url(r'^login/', LoginView.as_view(), name="login_url"),
    # url(r'^verify/$', PhoneVerificationView.as_view(), name="phone_verification_url"),
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard_url"),
    # url(r'^logout/$', logout, {'next_page': '/'})

]
