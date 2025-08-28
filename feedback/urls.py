# feedback/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Changed from 'home' to 'dashboard'
    path('health/', views.health_check, name='health_check'),  # Health check for debugging
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('submit-feedback/<int:course_id>/', views.submit_feedback, name='submit_feedback'),
    path('lecturer-report/', views.lecturer_report, name='lecturer_report'),
    path('course-list/', views.course_list, name='course_list'),
    path('available-courses/', views.available_courses, name='available_courses'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('unenroll/<int:course_id>/', views.unenroll_course, name='unenroll_course'),
    path('course/<int:course_id>/results/', views.view_feedback_results, name='view_feedback_results'),
    path('not-lecturer/', views.not_lecturer, name='not_lecturer'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/lecturer/', views.register_lecturer, name='register_lecturer'),
    path('register/admin/', views.register_admin, name='register_admin'),
    path('register-course/', views.register_course, name='register_course'),
    path('lecturer/export_csv/', views.export_feedback_csv, name='export_feedback_csv'),
    path('lecturer/export_pdf/', views.export_feedback_pdf, name='export_feedback_pdf'),
    path('signup/lecturer/', views.lecturer_signup, name='lecturer_signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'), # New OTP verification URL
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('dashboard/lecturer/', views.lecturer_dashboard, name='lecturer_dashboard'),
]
