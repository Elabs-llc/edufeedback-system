from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone # Import timezone

class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"{name} ({self.department})"

    class Meta:
        verbose_name = "Lecturer"
        verbose_name_plural = "Lecturers"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['code']


class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    clarity_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the clarity of the lecturer's explanations (1–5)"
    )
    engagement_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the lecturer's ability to engage the class (1–5)"
    )
    effectiveness_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the overall effectiveness of the course (1–5)"
    )
    comments = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.course.name} on {self.submitted_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"
        unique_together = ['course', 'student']  # Prevent duplicate feedback from same student
        ordering = ['-submitted_at']

# OTP verification
class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # allows multiple OTP history
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)  # to limit retries

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def is_valid(self):
        return (timezone.now() < self.expires_at) and (self.attempts < 5)

    def __str__(self):
        return f"OTP for {self.user.username} (expires {self.expires_at})"

    class Meta:
        verbose_name = "OTP Verification"
        verbose_name_plural = "OTP Verifications"
        ordering = ["-created_at"]
