# Django Feedback System

A comprehensive feedback management system built with Django that allows students to submit anonymous feedback for courses and lecturers to view detailed reports.

## Features

### For Students
- **Submit Anonymous Feedback**: Rate courses on clarity, engagement, and effectiveness
- **Course Enrollment**: Only enrolled students can provide feedback
- **User-Friendly Interface**: Modern Bootstrap UI with rating guides
- **Duplicate Prevention**: Each student can only submit one feedback per course

### For Lecturers
- **Detailed Reports**: View feedback statistics with charts and tables
- **Export Data**: Download reports in CSV and PDF formats
- **Visual Analytics**: Interactive charts showing feedback trends
- **Course Management**: View all assigned courses and their feedback

### For Administrators
- **Course Registration**: Add new courses and assign lecturers
- **User Management**: Manage student and lecturer accounts
- **System Administration**: Full Django admin panel access

## Technology Stack

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5.3.3 with Bootstrap Icons
- **Database**: SQLite (development) / PostgreSQL (production)
- **Charts**: Chart.js for data visualization
- **PDF Export**: xhtml2pdf for report generation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd feedback_system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
feedback_system/
├── feedback/                 # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Form definitions
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin interface
│   └── migrations/          # Database migrations
├── feedback_system/         # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── feedback/            # Feedback templates
│   └── registration/        # Authentication templates
├── static/                  # Static files (CSS, JS)
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## Database Models

### User (Django built-in)
- Standard Django user model for authentication

### Lecturer
- Extended user profile for lecturers
- Department and title information

### Course
- Course information (name, code, description)
- Lecturer assignment
- Student enrollment (many-to-many)

### Feedback
- Anonymous feedback submissions
- Rating scales (1-5) for clarity, engagement, effectiveness
- Optional comments
- Unique constraint per student per course

## Usage Guide

### Setting Up Courses

1. **Login as Admin**
   - Access the admin panel at `/admin/`
   - Create lecturer accounts if needed

2. **Register Courses**
   - Use the "Register Course" feature
   - Assign lecturers to courses
   - Enroll students in courses

### Student Workflow

1. **Register as Student**
   - Create account via registration page
   - Wait for admin to enroll you in courses

2. **Submit Feedback**
   - Login and navigate to dashboard
   - Select "Submit Feedback"
   - Rate courses and add comments

### Lecturer Workflow

1. **Register as Lecturer**
   - Create account and register lecturer profile
   - Wait for admin to assign courses

2. **View Reports**
   - Access feedback reports from dashboard
   - Export data in CSV/PDF formats
   - Analyze feedback trends

## Security Features

- **CSRF Protection**: All forms protected against cross-site request forgery
- **Authentication Required**: All views require proper authentication
- **Role-Based Access**: Different interfaces for students, lecturers, and admins
- **Input Validation**: Comprehensive form validation and sanitization
- **Anonymous Feedback**: Student identity not revealed to lecturers

## API Endpoints

| URL | Method | Description | Access |
|-----|--------|-------------|--------|
| `/` | GET | Dashboard | Authenticated |
| `/submit-feedback/` | GET/POST | Submit feedback form | Students |
| `/lecturer-report/` | GET | Feedback reports | Lecturers |
| `/register/student/` | GET/POST | Student registration | Public |
| `/register/lecturer/` | GET/POST | Lecturer registration | Authenticated |
| `/admin/register-course/` | GET/POST | Course registration | Admin |

## Configuration

### Environment Variables
Create a `.env` file for production settings:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Production Settings
- Set `DEBUG = False`
- Configure proper database (PostgreSQL recommended)
- Set up static file serving
- Configure email backend for notifications
- Enable HTTPS and security headers

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py migrate --fake-initial
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Permission Denied**
   - Check user roles and permissions
   - Ensure proper authentication

### Support
For issues and questions, please create an issue in the repository or contact the development team.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 2.0.0 (Current)
- Enhanced UI with Bootstrap 5 and icons
- Improved security and validation
- Better error handling and user feedback
- Export functionality for reports
- Role-based navigation
- Responsive design

### Version 1.0.0
- Basic feedback submission
- Simple reporting
- User authentication
- Basic admin interface
