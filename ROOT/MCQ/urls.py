from django.contrib.auth import views as logview
from django.urls import path
from . import views
from ADMINPANEL import views as adminviews
import secrets, string
import numpy as np

app_name = "MCQ"

# rand = secrets.choice(string.ascii_letters)
func = lambda: secrets.choice(string.ascii_letters)
randm1 = "".join([func() for _ in range(1,8)])
randm2 = "".join([func() for _ in range(1,8)])
randm3 = np.random.randint(0,98)
randm4 = "".join([func() for _ in range(1,8)])
randm5 = "".join([func() for _ in range(1,8)])
randmNMBR = np.random.randint(0,98)
randmNMBR2 = np.random.randint(0,98)

urlpatterns = [

    path("", logview.LoginView.as_view(template_name='MAIN_PAGE/login.html'), name='login'),# login page
    path(r'accounts/login/', views.login_message, name='login_message'),# MESSAGE PAGE WHEN USER IN NOT LOGGED IN
    path('logout/', logview.LogoutView.as_view(template_name='MAIN_PAGE/logout.html'),name="logout"),# LOGOUT PAGE
    path("students_portal/", views.students_portal, name='students_portal'), # students portal
    path(f"{randm1}<str:randmNmbr>{randm2}{randmNMBR}{randm3}<int:mainID>{randm4}<str:randmNmbr2>{randm5}{randmNMBR2}<int:counter>-<str:resultedTime>", views.quiz_page, name='quiz'), # homePage
    path(f"register/", views.user_registration, name='register'), # homePage
    path(f"testover/<str:username>", views.time_out, name='time_out'), # time out
    path(f"result/<str:enroll>", adminviews.student_report, name='studentreport'), # result

    # temp path
    path(f"feedback/", views.feedback, name='feedback'), # result



]
