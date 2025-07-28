from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from feedback.models import Lecturer, Course
import random


class Command(BaseCommand):
    help = 'Set up demo data for EduFeedback System'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-admin',
            action='store_true',
            help='Create a demo admin user',
        )
        parser.add_argument(
            '--create-lecturers',
            action='store_true',
            help='Create demo lecturer accounts',
        )
        parser.add_argument(
            '--create-courses',
            action='store_true',
            help='Create demo courses',
        )

    def handle(self, *args, **options):
        if options['create_admin']:
            self.create_admin()
        
        if options['create_lecturers']:
            self.create_lecturers()
            
        if options['create_courses']:
            self.create_courses()

    def create_admin(self):
        """Create a demo admin user"""
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@edufeedback.com',
                password='admin123',
                first_name='System',
                last_name='Administrator'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Admin user created: admin/admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists')
            )

    def create_lecturers(self):
        """Create demo lecturer accounts"""
        lecturers_data = [
            {
                'username': 'prof_smith',
                'email': 'smith@university.edu',
                'first_name': 'John',
                'last_name': 'Smith',
                'department': 'Computer Science',
                'title': 'Professor'
            },
            {
                'username': 'dr_johnson',
                'email': 'johnson@university.edu',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'department': 'Mathematics',
                'title': 'Dr.'
            },
            {
                'username': 'prof_brown',
                'email': 'brown@university.edu',
                'first_name': 'Michael',
                'last_name': 'Brown',
                'department': 'Physics',
                'title': 'Professor'
            }
        ]

        for lecturer_data in lecturers_data:
            if not User.objects.filter(username=lecturer_data['username']).exists():
                user = User.objects.create_user(
                    username=lecturer_data['username'],
                    email=lecturer_data['email'],
                    password='lecturer123',
                    first_name=lecturer_data['first_name'],
                    last_name=lecturer_data['last_name']
                )
                
                Lecturer.objects.create(
                    user=user,
                    department=lecturer_data['department'],
                    title=lecturer_data['title']
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Lecturer created: {lecturer_data["username"]}/lecturer123')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Lecturer {lecturer_data["username"]} already exists')
                )

    def create_courses(self):
        """Create demo courses"""
        if not Lecturer.objects.exists():
            self.stdout.write(
                self.style.ERROR('No lecturers found. Create lecturers first.')
            )
            return

        courses_data = [
            {
                'name': 'Introduction to Programming',
                'code': 'CS101',
                'description': 'Basic programming concepts using Python'
            },
            {
                'name': 'Data Structures and Algorithms',
                'code': 'CS201',
                'description': 'Advanced programming concepts and algorithm design'
            },
            {
                'name': 'Calculus I',
                'code': 'MATH101',
                'description': 'Differential and integral calculus'
            },
            {
                'name': 'Linear Algebra',
                'code': 'MATH201',
                'description': 'Vector spaces and matrix operations'
            },
            {
                'name': 'Physics I',
                'code': 'PHYS101',
                'description': 'Classical mechanics and thermodynamics'
            }
        ]

        lecturers = list(Lecturer.objects.all())
        
        for course_data in courses_data:
            if not Course.objects.filter(code=course_data['code']).exists():
                lecturer = random.choice(lecturers)
                
                Course.objects.create(
                    name=course_data['name'],
                    code=course_data['code'],
                    description=course_data['description'],
                    lecturer=lecturer
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Course created: {course_data["code"]} - {course_data["name"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Course {course_data["code"]} already exists')
                )

        self.stdout.write(
            self.style.SUCCESS('\nDemo data setup complete!')
        )
        self.stdout.write(
            self.style.SUCCESS('You can now test the system with the created accounts.')
        )
