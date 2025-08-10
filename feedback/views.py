import csv
from django.db import IntegrityError
from django.db import models
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import AdminRegistrationForm, CourseForm, FeedbackForm, LecturerRegistrationForm, LecturerSignupForm, StudentRegistrationForm
from .models import Feedback, Course, Lecturer
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import login

def health_check(request):
    """Health check endpoint for debugging"""
    try:
        # Check database
        user_count = User.objects.count()
        admin_count = User.objects.filter(is_superuser=True).count()
        
        # Check if admin user exists
        admin_exists = User.objects.filter(username='admin').exists()
        
        data = {
            'status': 'healthy',
            'database': 'connected',
            'users_total': user_count,
            'admins_total': admin_count,
            'admin_user_exists': admin_exists,
            'debug_info': {
                'path': request.path,
                'method': request.method,
                'user_authenticated': request.user.is_authenticated if hasattr(request, 'user') else False
            }
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'database': 'disconnected'
        }, status=500)

def get_user_role(user):
    """Utility function to determine user role"""
    if user.is_superuser:
        return "Super Admin"
    elif user.is_staff:
        return "Administrator"
    elif hasattr(user, 'lecturer'):
        return "Lecturer"
    else:
        return "Student"

def get_user_role_badge_class(user):
    """Get Bootstrap badge class for user role"""
    if user.is_superuser:
        return "bg-danger"
    elif user.is_staff:
        return "bg-warning text-dark"
    elif hasattr(user, 'lecturer'):
        return "bg-info"
    else:
        return "bg-success"

def home(request):
    return HttpResponse("Hello, Feedback System is working!")

@login_required
def submit_feedback(request, course_id=None):
    # Only allow students (non-staff users) to submit feedback
    if request.user.is_staff or hasattr(request.user, 'lecturer'):
        messages.warning(request, 'Only students can submit feedback.')
        return redirect('dashboard')
    
    # Get the specific course if course_id is provided
    selected_course = None
    if course_id:
        try:
            selected_course = Course.objects.get(id=course_id)
            # Check if user is enrolled in this course
            if not request.user.enrolled_courses.filter(id=course_id).exists():
                messages.error(request, 'You are not enrolled in this course.')
                return redirect('course_list')
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('course_list')
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, user=request.user, selected_course=selected_course)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user
            try:
                feedback.save()
                messages.success(request, 'Feedback submitted successfully!')
                return redirect('course_list')
            except Exception as e:
                messages.error(request, 'You have already submitted feedback for this course.')
    else:
        form = FeedbackForm(user=request.user, selected_course=selected_course)

    context = {
        'form': form,
        'selected_course': selected_course,
    }
    return render(request, 'feedback/submit_feedback.html', context)

@login_required
def lecturer_report(request):
    if not hasattr(request.user, 'lecturer'):
        return render(request, 'not_lecturer.html')

    lecturer = request.user.lecturer
    courses = Course.objects.filter(lecturer=lecturer).prefetch_related('feedback_set')

    report_data = []
    total_feedback_count = 0
    total_clarity_sum = 0
    total_engagement_sum = 0
    total_effectiveness_sum = 0
    courses_with_feedback = 0
    
    for course in courses:
        feedbacks = course.feedback_set.all()
        count = feedbacks.count()

        if count == 0:
            avg_clarity = avg_engagement = avg_effectiveness = overall_avg = 0
        else:
            avg_clarity = round(sum(f.clarity_rating for f in feedbacks) / count, 2)
            avg_engagement = round(sum(f.engagement_rating for f in feedbacks) / count, 2)
            avg_effectiveness = round(sum(f.effectiveness_rating for f in feedbacks) / count, 2)
            overall_avg = round((avg_clarity + avg_engagement + avg_effectiveness) / 3, 2)
            
            # Add to totals for overall statistics
            total_feedback_count += count
            total_clarity_sum += avg_clarity
            total_engagement_sum += avg_engagement
            total_effectiveness_sum += avg_effectiveness
            courses_with_feedback += 1

        report_data.append({
            'course': course,
            'count': count,
            'avg_clarity': avg_clarity,
            'avg_engagement': avg_engagement,
            'avg_effectiveness': avg_effectiveness,
            'overall_avg': overall_avg,
            'clarity_percentage': avg_clarity * 20,  # For progress bar (0-5 scale to 0-100%)
            'engagement_percentage': avg_engagement * 20,
            'effectiveness_percentage': avg_effectiveness * 20,
            'feedbacks': feedbacks,  # Needed for table display
        })

    # Calculate overall statistics
    if courses_with_feedback > 0:
        overall_rating = round((total_clarity_sum + total_engagement_sum + total_effectiveness_sum) / (courses_with_feedback * 3), 1)
    else:
        overall_rating = 0.0

    context = {
        'report_data': report_data,
        'total_courses': courses.count(),
        'total_feedback': total_feedback_count,
        'overall_rating': overall_rating,
        'active_courses': courses_with_feedback,
        'user_role': get_user_role(request.user),
        'role_badge_class': get_user_role_badge_class(request.user),
    }
    
    return render(request, 'lecturer_report.html', context)


@login_required
def dashboard(request):
    user = request.user
    is_lecturer = hasattr(user, 'lecturer')
    
    # Get user role information
    user_role = get_user_role(user)
    role_badge_class = get_user_role_badge_class(user)
    
    # Calculate statistics based on user role
    context = {
        'is_lecturer': is_lecturer,
        'user_role': user_role,
        'role_badge_class': role_badge_class
    }
    
    if user.is_staff:
        # Admin statistics
        all_feedback = Feedback.objects.all()
        total_ratings = 0
        count = 0
        for feedback in all_feedback:
            total_ratings += (feedback.clarity_rating + feedback.engagement_rating + feedback.effectiveness_rating) / 3
            count += 1
        avg_rating = total_ratings / count if count > 0 else 0
        
        context.update({
            'total_users': User.objects.count(),
            'active_courses': Course.objects.count(),
            'total_feedback': all_feedback.count(),
            'avg_rating': round(avg_rating, 1)
        })
    elif is_lecturer:
        # Lecturer statistics
        lecturer_courses = user.lecturer.courses.all()
        lecturer_feedback = Feedback.objects.filter(course__in=lecturer_courses)
        
        context.update({
            'my_courses_count': lecturer_courses.count(),
            'total_students': sum(course.students.count() for course in lecturer_courses),
            'new_feedback': lecturer_feedback.count()
        })
    else:
        # Student statistics
        enrolled_courses = user.enrolled_courses.all()
        submitted_feedback = Feedback.objects.filter(student=user)
        
        context.update({
            'enrolled_courses_count': enrolled_courses.count(),
            'feedback_submitted': submitted_feedback.count(),
            'pending_feedback': enrolled_courses.count() - submitted_feedback.count()
        })
    
    return render(request, 'feedback/dashboard.html', context)

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Student registered successfully.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'registration/register_student.html', {'form': form})

# @login_required
def register_lecturer(request):
    if hasattr(request.user, 'lecturer'):
        messages.info(request, "You are already registered as a lecturer.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST, user=request.user)
        if form.is_valid():
            lecturer = form.save()
            messages.success(request, "Lecturer account created successfully.")
            return redirect('dashboard')
    else:
        form = LecturerRegistrationForm(user=request.user)

    return render(request, 'registration/register_lecturer.html', {'form': form})


@login_required
@staff_member_required
def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = False  # Optional: change to True if they should access full Django admin
            user.save()
            messages.success(request, 'Admin account created successfully.')
            return redirect('login')
    else:
        form = AdminRegistrationForm()

    return render(request, 'registration/register_admin.html', {'form': form})

@staff_member_required
def register_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course registered successfully!')
            return redirect('register_course')
    else:
        form = CourseForm()

    return render(request, 'admin/register_course.html', {'form': form})


from django.db.models import Avg, Count

@login_required
def export_feedback_csv(request):
    if not hasattr(request.user, 'lecturer'):
        messages.error(request, 'You must be a lecturer to access this feature.')
        return redirect('dashboard')
    
    lecturer = request.user.lecturer
    courses = Course.objects.filter(lecturer=lecturer)

    feedback_data = (
        Feedback.objects
        .filter(course__in=courses)
        .values('course__name')
        .annotate(
            count=Count('id'),
            avg_clarity=Avg('clarity_rating'),
            avg_engagement=Avg('engagement_rating'),
            avg_effectiveness=Avg('effectiveness_rating')
        )
    )

    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lecturer_feedback_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Course', 'Feedback Count', 'Avg Clarity', 'Avg Engagement', 'Avg Effectiveness'])

    for item in feedback_data:
        writer.writerow([
            item['course__name'],
            item['count'],
            round(item['avg_clarity'], 1),
            round(item['avg_engagement'], 1),
            round(item['avg_effectiveness'], 1),
        ])

    return response



@login_required
def export_feedback_pdf(request):
    if not hasattr(request.user, 'lecturer'):
        messages.error(request, 'You must be a lecturer to access this feature.')
        return redirect('dashboard')
    
    lecturer = request.user.lecturer
    courses = Course.objects.filter(lecturer=lecturer)

    report_data = (
        Feedback.objects
        .filter(course__in=courses)
        .values('course__name')
        .annotate(
            count=Count('id'),
            avg_clarity=Avg('clarity_rating'),
            avg_engagement=Avg('engagement_rating'),
            avg_effectiveness=Avg('effectiveness_rating')
        )
    )

    template = get_template('feedback/lecturer_report_pdf.html')
    html = template.render({'report_data': report_data})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="feedback_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation failed', status=500)
    return response



def lecturer_signup(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = LecturerSignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "Lecturer account created and logged in!")
                return redirect('lecturer_dashboard')
            except IntegrityError:
                form.add_error('username', 'This username is already taken. Please choose another.')
    else:
        form = LecturerSignupForm()
    
    return render(request, 'registration/signup_lecturer.html', {'form': form})


@login_required
def lecturer_dashboard(request):
    return render(request, 'dashboard/lecturer_dashboard.html')

@login_required
def course_list(request):
    """Display list of courses for students to provide feedback"""
    # Get courses the user is enrolled in
    enrolled_courses = request.user.enrolled_courses.all()
    
    # Add feedback information for each course
    courses_with_feedback = []
    for course in enrolled_courses:
        user_feedback = Feedback.objects.filter(course=course, student=request.user).first()
        courses_with_feedback.append({
            'course': course,
            'user_feedback': user_feedback,
            'has_submitted_feedback': user_feedback is not None
        })
    
    return render(request, 'course_list.html', {'courses_data': courses_with_feedback})

@login_required
def available_courses(request):
    """Display all available courses for students to enroll in"""
    if request.user.is_staff or hasattr(request.user, 'lecturer'):
        messages.warning(request, 'Only students can view available courses.')
        return redirect('dashboard')
    
    # Get all courses excluding those the user is already enrolled in
    enrolled_course_ids = request.user.enrolled_courses.values_list('id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_course_ids).order_by('code')
    
    return render(request, 'feedback/available_courses.html', {'courses': available_courses})

@login_required
def enroll_course(request, course_id):
    """Enroll student in a course"""
    if request.user.is_staff or hasattr(request.user, 'lecturer'):
        messages.warning(request, 'Only students can enroll in courses.')
        return redirect('dashboard')
    
    try:
        course = Course.objects.get(id=course_id)
        
        # Check if already enrolled
        if request.user.enrolled_courses.filter(id=course_id).exists():
            messages.warning(request, f'You are already enrolled in {course.name}.')
        else:
            # Enroll the student
            course.students.add(request.user)
            messages.success(request, f'Successfully enrolled in {course.name}!')
            
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
    
    return redirect('available_courses')

@login_required
def unenroll_course(request, course_id):
    """Unenroll student from a course"""
    if request.user.is_staff or hasattr(request.user, 'lecturer'):
        messages.warning(request, 'Only students can unenroll from courses.')
        return redirect('dashboard')
    
    try:
        course = Course.objects.get(id=course_id)
        
        # Check if enrolled
        if not request.user.enrolled_courses.filter(id=course_id).exists():
            messages.warning(request, f'You are not enrolled in {course.name}.')
        else:
            # Check if feedback already submitted
            if Feedback.objects.filter(course=course, student=request.user).exists():
                messages.error(request, f'Cannot unenroll from {course.name} because you have already submitted feedback.')
            else:
                # Unenroll the student
                course.students.remove(request.user)
                messages.success(request, f'Successfully unenrolled from {course.name}.')
                
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
    
    return redirect('course_list')

def not_lecturer(request):
    """Display access denied page for non-lecturers"""
    return render(request, 'not_lecturer.html')

@login_required
def view_feedback_results(request, course_id):
    """View feedback results for a specific course (staff only)"""
    if not request.user.is_staff:
        return redirect('not_lecturer')
    
    try:
        course = Course.objects.get(id=course_id)
        feedbacks = Feedback.objects.filter(course=course).select_related('student')
        
        # Calculate average ratings
        if feedbacks:
            avg_clarity = sum(f.clarity_rating for f in feedbacks) / len(feedbacks)
            avg_engagement = sum(f.engagement_rating for f in feedbacks) / len(feedbacks)
            avg_effectiveness = sum(f.effectiveness_rating for f in feedbacks) / len(feedbacks)
        else:
            avg_clarity = avg_engagement = avg_effectiveness = 0
        
        context = {
            'course': course,
            'feedbacks': feedbacks,
            'avg_clarity': round(avg_clarity, 2),
            'avg_engagement': round(avg_engagement, 2),
            'avg_effectiveness': round(avg_effectiveness, 2),
            'total_feedback': len(feedbacks),
        }
        return render(request, 'course_feedback_results.html', context)
        
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('course_list')