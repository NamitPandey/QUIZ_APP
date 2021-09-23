from django.contrib.auth import views as logview
from django.urls import path
from . import views

app_name = "ADMINPANEL"


urlpatterns = [
# university/adminpanel/
    path("", views.admin_home, name='admin_home'),
    path("uploadfiles/", views.upload_files, name='uploadfiles'),
    path("upload_data/<int:dataBaseKey>", views.upload_data, name='upload_data'),
    path("download_data/", views.download_data, name='download_data'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("studentreport/<str:enroll>", views.student_report, name='studentreport'),
    path("records/", views.records, name='records'),
    path("announcement/<int:status>/<str:pageDictKey>", views.toggle_result, name='announcement'),
    path("template/<int:setNO>", views.template_download, name='template'),
    path("information/", views.get_dept_information, name='information'),
    path("feedbaack/", views.feedback_page, name='feedbackpage'),
    path("feedback/download", views.download_feedback, name='feedback'),
    path("downloadtemplate/universitydata", views.download_university_template, name='universitydataTemplate'),
    path("uploadfiles/universitydata", views.update_university_data, name='universitydata'),
    path("whoami", views.my_detail, name='whoami'),
    path("department/iforgot", views.reset_faculty_pass, name='reset_faculty_pass'),
]
