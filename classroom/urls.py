from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('student_login', views.s_login,name="s_login"),
    path('teacher_login',views.t_login,name="t_login"),
    path('admin_login',views.a_login,name="a_login"),
    
    path('dashboard',views.s_dash,name="dashboard"),
    path('teacher_dashboard',views.t_dash,name="t_dash"),
    path('admin_dashboard',views.a_dash,name="a_dash"),
    
    path('school_register',views.s_register,name="s_register"),
    path('teacher_registration',views.t_register,name="t_register" ),
    path('stdnt_registration',views.stdnt_registration,name="stdnt_registration"),
   
    path('Logout_session',views.session_logout,name="logout_session"),

    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="classroom/reset_password.html"),
    name="reset_password"),
    
    path('reset_password_done/',
    auth_views.PasswordResetDoneView.as_view(template_name="classroom/password_reset_sent.html"),
    name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="classroom/password_reset_form.html"),
    name="password_reset_confirm"),

    path('reset_password_completed/',
    auth_views.PasswordResetCompleteView.as_view(template_name="classroom/password_reset_done.html"),
    name="password_reset_complete"),

]