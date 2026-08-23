from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

def home(request):
    """
    Haider Ali Hashmi - Portfolio Context & Dynamic Render
    """
    if request.method == 'POST':
        name = request.POST.get('from_name')
        email = request.POST.get('from_email')
        message_text = request.POST.get('message')

        if name and email and message_text:
            # 1. Database mein save karein
            ContactMessage.objects.create(name=name, email=email, message=message_text)

            # 2. Gmail par direct notification bhejein
            subject = f"New Portfolio Message from {name}"
            email_body = f"You have received a new message from your portfolio contact form.\n\nName: {name}\nEmail: {email}\nMessage:\n{message_text}"
            
            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    ['haideralihashmi2308@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully & delivered to your email!")
            except Exception as e:
                messages.success(request, "Message saved to database successfully!")

            return redirect('home')

    context = {
        'name': 'HAIDER ALI HASHMI',
        'title': 'Full Stack & Backend Web Developer',
        'bio': 'Experienced in backend engineering through hands-on internships in Python (Django) and Node.js, paired with practical expertise in Search Engine Optimization. Skilled in building clean server-side architectures, RESTful APIs, and database management.',
        'location': 'Lahore, Pakistan',
        'whatsapp': '923264607060',
        'email': 'haideralihashmi2308@gmail.com',
        'github_url': 'https://github.com/HaiderAli238',
        'linkedin_url': 'https://www.linkedin.com/in/haider-ali-hashmi-394a32349/',
        
        # EXACT RESUME EXPERIENCES
        'experiences': [
            {
                'role': 'SEO Expert',
                'company': 'Axcess',
                'period': 'April 2025 - May 2026',
                'desc': 'Executed comprehensive keyword research, technical website audits, on-page structure optimizations, and authority-building link strategies to boost organic traffic and indexability.',
                'tags': ['Keyword Strategy', 'Technical SEO', 'On-Page/Off-Page', 'Google Search Console']
            },
            {
                'role': 'Python Django Intern',
                'company': 'CodeXpace',
                'period': 'April 2025 - July 2025',
                'desc': 'Developed and maintained web apps using Django & Django REST Framework (DRF), designed SQLite database schemas, and optimized backend query logic.',
                'tags': ['Python', 'Django', 'Django REST Framework', 'SQLite', 'Git']
            },
            {
                'role': 'Node.js Developer Intern',
                'company': 'NexGen Solutions',
                'period': 'Sept 2024 - Dec 2024',
                'desc': 'Built scalable server-side logic using Node.js & Express.js, designed MongoDB schemas, and optimized API responsiveness and backend bottlenecks.',
                'tags': ['Node.js', 'Express.js', 'MongoDB', 'REST APIs', 'Async Programming']
            },
        ],

        # SKILLS ACCORDING TO CV
        'skill_categories': [
            {
                'title': 'Frontend',
                'skills': ['React.js', 'Next.js', 'Tailwind CSS', 'HTML5', 'JavaScript (ES6+)']
            },
            {
                'title': 'Backend & Databases',
                'skills': ['Python & Django', 'Node.js & Express.js', 'MongoDB', 'SQLite', 'Authentication']
            },
            {
                'title': 'State & APIs',
                'skills': ['RESTful APIs', 'Redux', 'Zustand', 'React Query']
            },
            {
                'title': 'Tools & SEO',
                'skills': ['Git/GitHub', 'Deployment', 'Technical SEO', 'On-Page SEO', 'Off-Page SEO']
            },
        ],

        # SERVICES
        'services': [
            {
                'title': 'Backend Engineering',
                'desc': 'Designing robust server-side architectures, database schemas, and high-performance REST APIs using Django and Node.js.',
                'icon': 'server'
            },
            {
                'title': 'Full Stack Development',
                'desc': 'End-to-end modern web applications leveraging Django/Node.js backends with responsive, clean React/Tailwind frontends.',
                'icon': 'layer-group'
            },
            {
                'title': 'SEO & Technical Optimization',
                'desc': 'Combining technical SEO, page speed performance, and structured metadata to maximize organic search visibility.',
                'icon': 'chart-line'
            },
        ],

        # DYNAMIC PROJECTS DATA
        'projects': [
            {
                'title': 'Student Management System',
                'category': 'Backend',
                'desc': 'A comprehensive portal built with Django to manage student records, course enrollments, attendance, and administrative workflows.',
                'tech': ['Python', 'Django', 'SQLite', 'Tailwind CSS'],
                'image_url': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&q=80&w=800',
                'github_url': 'https://github.com/HaiderAli238',
                'live_url': '#'
            },
            {
                'title': 'E-Commerce Platform',
                'category': 'Fullstack',
                'desc': 'Full-featured online store with product management, secure cart checkout, user order history, and payment gateway integration.',
                'tech': ['Python', 'Django', 'PostgreSQL', 'Tailwind CSS'],
                'image_url': 'https://plus.unsplash.com/premium_photo-1664201890375-f8fa405cdb7d?q=80&w=1170&auto=format&fit=crop',
                'github_url': 'https://github.com/HaiderAli238',
                'live_url': '#'
            },
            {
                'title': 'Secure Auth Engine',
                'category': 'Backend',
                'desc': 'Microservice authentication system built with Node.js & Express featuring JWT token rotation, bcrypt encryption, and rate limiting.',
                'tech': ['Node.js', 'Express.js', 'MongoDB', 'JWT', 'Bcrypt'],
                'image_url': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80&w=800',
                'github_url': 'https://github.com/HaiderAli238',
                'live_url': '#'
            },
        ]
    }
    return render(request, 'base.html', context)


# ==========================================
# AUTHENTICATION & AUTHORIZATION VIEWS
# ==========================================

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')