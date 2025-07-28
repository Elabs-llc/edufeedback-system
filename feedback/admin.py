from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Lecturer, Course, Feedback

# Customize User Admin
class LecturerInline(admin.StackedInline):
    model = Lecturer
    can_delete = False
    verbose_name_plural = 'Lecturer Profile'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (LecturerInline,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('lecturer_name', 'department', 'title', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'department')
    readonly_fields = ('created_at',)
    
    def lecturer_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    lecturer_name.short_description = 'Lecturer Name'
    lecturer_name.admin_order_field = 'user__first_name'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'lecturer_name', 'student_count', 'created_at')
    list_filter = ('lecturer__department', 'created_at')
    search_fields = ('code', 'name', 'lecturer__user__username', 'lecturer__user__first_name', 'lecturer__user__last_name')
    readonly_fields = ('created_at',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "lecturer":
            kwargs["queryset"] = Lecturer.objects.select_related('user').all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def lecturer_name(self, obj):
        return obj.lecturer.user.get_full_name() or obj.lecturer.user.username
    lecturer_name.short_description = 'Lecturer'
    lecturer_name.admin_order_field = 'lecturer__user__first_name'
    
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Enrolled Students'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('course', 'student_name', 'clarity_rating', 'engagement_rating', 'effectiveness_rating', 'submitted_at')
    list_filter = ('course', 'submitted_at', 'clarity_rating', 'engagement_rating', 'effectiveness_rating')
    search_fields = ('course__name', 'course__code', 'student__username', 'student__first_name', 'student__last_name')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
    
    def student_name(self, obj):
        if obj.student:
            return obj.student.get_full_name() or obj.student.username
        return "Anonymous"
    student_name.short_description = 'Student'
    student_name.admin_order_field = 'student__first_name'
    
    # Make feedback read-only to preserve integrity
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# Customize admin site
admin.site.site_header = "Feedback System Administration"
admin.site.site_title = "Feedback Admin"
admin.site.index_title = "Welcome to Feedback System Administration"

