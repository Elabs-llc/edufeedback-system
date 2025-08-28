from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Course, Feedback, Lecturer

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['course', 'clarity_rating', 'engagement_rating', 'effectiveness_rating', 'comments']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'clarity_rating': forms.NumberInput(attrs={
                'min': 1, 'max': 5, 'class': 'form-control',
                'placeholder': 'Rate 1-5'
            }),
            'engagement_rating': forms.NumberInput(attrs={
                'min': 1, 'max': 5, 'class': 'form-control',
                'placeholder': 'Rate 1-5'
            }),
            'effectiveness_rating': forms.NumberInput(attrs={
                'min': 1, 'max': 5, 'class': 'form-control',
                'placeholder': 'Rate 1-5'
            }),
            'comments': forms.Textarea(attrs={
                'rows': 4, 'class': 'form-control',
                'placeholder': 'Optional feedback comments...'
            }),
        }
        labels = {
            'clarity_rating': 'Clarity Rating',
            'engagement_rating': 'Engagement Rating',
            'effectiveness_rating': 'Effectiveness Rating',
            'comments': 'Additional Comments (Optional)',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        selected_course = kwargs.pop('selected_course', None)
        super().__init__(*args, **kwargs)
        if user:
            # Only show courses the student is enrolled in
            self.fields['course'].queryset = Course.objects.filter(students=user)
            
            # If a specific course is selected, pre-select it and make it read-only
            if selected_course:
                self.fields['course'].initial = selected_course
                self.fields['course'].widget = forms.HiddenInput()
                self.initial['course'] = selected_course


class LecturerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Lecturer
        fields = ['department', 'title']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Professor, Dr., Mr., Ms.'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        lecturer = super().save(commit=False)
        if self.user:
            # Update user info
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.save()
            lecturer.user = self.user
        if commit:
            lecturer.save()
        return lecturer


class AdminRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'lecturer', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CS101'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Introduction to Computer Science'}),
            'lecturer': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize how lecturers are displayed in the dropdown
        self.fields['lecturer'].label_from_instance = lambda obj: f"{obj.user.get_full_name() or obj.user.username} - {obj.department}"


class LecturerSignupForm(forms.ModelForm):
    # --- Personal Information ---
    first_name = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )

    # --- Account Credentials ---
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )

    # Lecturer Specific Details
    
    title = forms.CharField(
        max_length=100, 
        required=False, # Make it clear this field is optional
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Professor, Dr., Mr., Ms.'})
    )
    department = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'})
    )
    
    # --- Password Fields ---
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Lecturer
        # These fields from the Lecturer model will be handled by the form.
        fields = ['department', 'title']

    # Your validation and save methods are already correct and need no changes.
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        lecturer = super().save(commit=False)
        lecturer.user = user
        if commit:
            lecturer.save()
        return user

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})

    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email



    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_staff = False  # Ensure students are not staff
        if commit:
            user.save()
        return user

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter OTP'}),
        help_text='Enter the 6-digit OTP sent to your email.'
    )
