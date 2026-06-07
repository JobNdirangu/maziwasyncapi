
# MaziwaSync

## Project Overview

MaziwaSync is a Cooperative Management Information System designed to digitize and streamline milk collection, farmer management, communication, and operational analytics within dairy cooperatives.

The system aims to improve transparency, efficiency, accountability, and communication between cooperative administrators, milk porters/collectors, and farmers.

Traditionally, many dairy cooperatives rely on manual records, paper-based tracking, and inefficient communication channels, which often lead to data inconsistencies, delayed payments, poor farmer engagement, and operational inefficiencies. MaziwaSync addresses these challenges through a centralized digital platform built using Django and Django REST Framework.

The platform supports multiple user roles, including administrators, milk porters, and farmers, each with role-specific dashboards and functionalities.

---

# Core Features

* Role-based authentication and authorization
* Milk collection tracking
* Farmer supply monitoring
* Porter activity management
* Cooperative analytics dashboard
* Complaint and feedback management
* Notice board and announcements
* AI-powered sentiment analysis for farmer feedback
* Payment tracking and future Mpesa B2C integration
* Reporting and operational insights

---

# User Roles

## Administrator

Administrators oversee the entire cooperative system. They can:

* Monitor total milk collection
* View porter performance
* Manage farmer complaints
* Publish notices and announcements
* Track analytics and reports
* Monitor payment estimations

---

## Porter / Milk Collector

Porters are responsible for collecting milk from farmers and recording:

* Farmer details
* Amount of milk collected
* Collection session (morning/evening)
* Date and time of collection

---

## Farmer

Farmers can:

* View milk supply history
* Track expected payments
* View notices and announcements
* Submit complaints and comments
* Monitor complaint resolution status
* View supply analytics and trends

---

# Objectives

The main objective of MaziwaSync is to modernize cooperative operations by providing a scalable, secure, and data-driven platform that enhances operational efficiency and farmer welfare.

The system also seeks to improve farmer engagement, operational monitoring, communication, and decision-making through centralized data management and analytics.

---

# Technology Stack

* Backend Framework: Django
* API Framework: Django REST Framework
* Database: MySQL
* Authentication: JWT Authentication
* API Documentation: drf-spectacular (Swagger/OpenAPI)
* Future Integrations:

  * Mpesa Daraja API
  * AI Sentiment Analysis

---

# Software Development Methodology

The project follows an Agile Software Development Lifecycle (SDLC) approach to support iterative development, continuous improvement, modular feature implementation, and continuous testing throughout the course development process.

Development will be carried out in iterative phases (sprints), allowing gradual implementation of features such as authentication, milk collection management, dashboards, analytics, complaints management, and payment integration.

---

# Future Enhancements

* Mpesa B2C automated farmer payments
* AI-based farmer sentiment classification
* SMS notification integration
* Advanced analytics and reporting
* Multi-cooperative support
* Mobile application integration

---

# System Architecture and Application Design

## Architectural Design Decision

MaziwaSync follows a modular application architecture based on the principle of **Separation of Concerns (SoC)**.

Instead of placing all functionalities into a single Django application, the system is divided into specialized modules where each application handles a specific domain responsibility. This improves:

* Maintainability
* Scalability
* Code organization
* Readability
* Team collaboration
* Testing and debugging

The architecture also aligns with professional software engineering practices used in production systems.

---

# Core Design Principles Applied

## 1. Separation of Concerns (SoC)

Each application is responsible for a specific business domain.

Example:

* Authentication logic should not be mixed with milk collection logic.
* Farmer operations should not directly control cooperative administrative operations.

This reduces coupling and improves maintainability.

---

## 2. Modularity

The project is broken into independent modules (apps) that can evolve separately without heavily affecting the entire system.

This supports:

* easier updates
* feature expansion
* isolated testing
* cleaner architecture

---

## 3. Scalability

The architecture is designed to support future enhancements such as:

* Mpesa integration
* AI sentiment analysis
* SMS notifications
* mobile applications
* multi-cooperative support

without requiring major restructuring.

---

## 4. Reusability

Shared functionalities such as authentication, permissions, and notifications can be reused across multiple modules.

---

## 5. Maintainability

A well-structured modular system is easier to debug, document, test, and maintain over time.

---

# System Applications

The project uses five main Django applications.

---

# 1. Core Application


## Responsibilities

The core application handles:

* Custom User model
* Authentication
* JWT Authentication
* Registration
* Authorization & Permissions
* User Roles
* User Profiles
* Base Models
* Shared Utilities
* Shared Mixins

Supported Roles
* Administrator
* Farmer
* Porter / Milk Collector

## Engineering Reasoning

A dedicated core app provides:
- The Core application contains all system-wide functionality required by every other module. Since authentication, authorization, user management, and role handling are foundational concerns used throughout the system, keeping them together with the custom User model provides a single source of truth and reduces unnecessary application fragmentation.

---

# 2. Accounts Application

## Responsibilities

The accounts application handles:

* User authentication
* JWT authentication
* User registration
* Role management
* User profiles
* Authorization and permissions

## Supported Roles

* Administrator
* Farmer
* Porter / Milk Collector

## Engineering Reasoning

Authentication is isolated because it is a shared system-wide responsibility used across all modules.

---

# 3. Cooperative Application

## Responsibilities

The cooperative application handles:

* Cooperative dashboard
* Notices and announcements
* Complaints management
* Analytics and reports
* Payment calculations
* Farmer welfare tracking
* Administrative operations

## Engineering Reasoning

Administrative and management operations are grouped together because they belong to the cooperative business domain.

---

# 4. Collector Application

## Responsibilities

The collector application handles:

* Milk collection records
* Collection sessions
* Farmer milk entries
* Daily collection tracking
* Collection history

## Engineering Reasoning

Milk collection is the system's operational core process and deserves isolation from administrative logic.

---

# 5. Farmer Application

## Responsibilities

The farmer application handles:

* Farmer dashboard
* Supply history
* Farmer analytics
* Complaints submission
* Viewing notices
* Payment estimations

## Engineering Reasoning

Farmer-facing functionality is isolated to improve user-specific logic management and support future mobile or farmer portal integrations.

---

# Initial Project Setup

## Step 1: Create the Django Project

```bash
django-admin startproject maziwasyncapi
```

Move into the project directory:

```bash
cd maziwasyncapi
```

---

## Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install django djangorestframework mysqlclient drf-spectacular djangorestframework-simplejwt django-cors-headers python-decouple
```

---

## Step 4: Save Dependencies

```bash
pip freeze > requirements.txt
```

---

## Step 5: Create the Applications

```bash
python manage.py startapp core
python manage.py startapp cooperative
python manage.py startapp collector
python manage.py startapp farmer
```

---

## Step 6: Configure Settings

### AUTH_USER_MODEL Declaration

In `maziwasyncapi/settings.py`:

```python
AUTH_USER_MODEL = 'core.User'
```

### INSTALLED_APPS Configuration

```python
INSTALLED_APPS = [
    # Default Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'rest_framework',
    'drf_spectacular',

    # Local Apps
    'core',
    'accounts',
    'cooperative',
    'collector',
    'farmer',
]
```

### REST Framework Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### JWT Settings

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

### Database Configuration

```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='maziwasyncdb'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}
```

### CORS Configuration

```python
CORS_ALLOW_ALL_ORIGINS = True  # Development only
```

### Static & Media Files

```python
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Environment Variables (.env file)

```env
SECRET_KEY=your-super-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=maziwasyncdb
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

---
You're absolutely right! Here's the corrected `core/models.py` section for your README.md that matches YOUR actual implementation:


## Step 7: Create Models in Core Application

In `core/models.py`:

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# ============================================================
# CUSTOM USER MODEL (First - before any profile uses it)
# ============================================================

class User(AbstractUser):
    """Custom User model with role-based access"""
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('porter', 'Porter'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='farmer')
    phone_number = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"


# ============================================================
# BASE ABSTRACT MODEL
# ============================================================

class BaseModel(models.Model):
    """Abstract base model with common timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


# ============================================================
# FARMER PROFILE
# ============================================================

class FarmerProfile(BaseModel):
    """Complete farmer profile - all information a cooperative needs"""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='farmer_profile'
    )
    
    # Personal Information
    profile_image = models.ImageField(
        upload_to='farmers/profiles/', 
        null=True, 
        blank=True
    )
    national_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, 
        choices=[('MALE', 'Male'), ('FEMALE', 'Female')], 
        null=True, 
        blank=True
    )
    
    # Contact Information
    phone_number = models.CharField(max_length=15, unique=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    
    # Farm Information
    farm_name = models.CharField(max_length=200, blank=True, null=True)
    farm_size_acres = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    number_of_cows = models.IntegerField(default=0)
    membership_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
    
    # Banking Information
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_branch = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    mpesa_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Statistics (auto-updated by system)
    total_milk_delivered = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ============================================================
# PORTER PROFILE
# ============================================================

class PorterProfile(BaseModel):
    """Porter/Collector profile"""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='porter_profile'
    )
    profile_image = models.ImageField(
        upload_to='porters/profiles/', 
        null=True, 
        blank=True
    )
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    route_name = models.CharField(max_length=200)
    assigned_farmers = models.ManyToManyField(
        FarmerProfile, 
        related_name='assigned_porters', 
        blank=True
    )
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    total_collections = models.IntegerField(default=0)
    total_liters_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.employee_id}"


# ============================================================
# MILK COLLECTION
# ============================================================

class MilkCollection(BaseModel):
    """Daily milk collection record"""
    
    SESSION_CHOICES = [
        ('MORNING', 'Morning'),
        ('EVENING', 'Evening'),
    ]
    
    farmer = models.ForeignKey(
        FarmerProfile, 
        on_delete=models.CASCADE, 
        related_name='collections'
    )
    porter = models.ForeignKey(
        PorterProfile, 
        on_delete=models.CASCADE, 
        related_name='collections'
    )
    liters = models.DecimalField(max_digits=10, decimal_places=2)
    session = models.CharField(max_length=10, choices=SESSION_CHOICES)
    collection_date = models.DateField(auto_now_add=True)
    price_per_liter = models.DecimalField(max_digits=8, decimal_places=2, default=50.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"{self.collection_date}: {self.farmer.first_name} - {self.liters}L"
    
    def save(self, *args, **kwargs):
        self.total_amount = self.liters * self.price_per_liter
        super().save(*args, **kwargs)


# ============================================================
# FEEDBACK
# ============================================================

class Feedback(BaseModel):
    """Farmer complaints tracking"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]
    
    farmer = models.ForeignKey(
        FarmerProfile, 
        on_delete=models.CASCADE, 
        related_name='feedbacks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return self.title


# ============================================================
# NOTICE / ANNOUNCEMENT
# ============================================================

class Notice(BaseModel):
    """System announcements for different user groups"""
    
    TARGET_CHOICES = [
        ('ALL', 'All Users'),
        ('FARMERS', 'Farmers Only'),
        ('PORTERS', 'Porters Only'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    target = models.CharField(max_length=10, choices=TARGET_CHOICES, default='ALL')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_important = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


# ============================================================
# PAYMENT
# ============================================================

class Payment(BaseModel):
    """Payment records for milk deliveries"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    METHOD_CHOICES = [
        ('MPESA', 'M-Pesa'),
        ('CASH', 'Cash'),
    ]
    
    farmer = models.ForeignKey(
        FarmerProfile, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transaction_ref = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.transaction_ref} - KES {self.amount}" ```

---

## Step 8: Create and Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Database Schema Overview

The core app contains the following models:

| Model | Purpose |
|-------|---------|
| `User` | Custom user with role-based authentication |
| `BaseModel` | Abstract base with timestamps (inherited by all models) |
| `FarmerProfile` | Complete farmer information and statistics |
| `PorterProfile` | Milk collector/porter information |
| `MilkCollection` | Daily milk collection records |
| `Complaint` | Farmer complaint tracking |
| `Notice` | System announcements |
| `Payment` | Payment records for milk deliveries |

## Model Relationships

```
User (auth)
  ├── FarmerProfile (OneToOne)
  │     ├── MilkCollection (ForeignKey)
  │     ├── Complaint (ForeignKey)
  │     └── Payment (ForeignKey)
  │
  └── PorterProfile (OneToOne)
        ├── MilkCollection (ForeignKey)
        └── assigned_farmers (ManyToMany with FarmerProfile)
```


---

## Step 8: Create and Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Expected Project Structure

```
maziwasyncapi/
│
├── core/
│   ├── models.py
│   ├── admin.py
│   └── ...
│
├── accounts/
├── cooperative/
├── collector/
├── farmer/
│
├── maziwasyncapi/
│   ├── settings.py
│   └── ...
│
├── manage.py
└── requirements.txt
```

---

# Important Engineering Decisions

## Why Core App Instead of Accounts App for User Model?

| Consideration | Benefit |
|--------------|---------|
| Circular Imports | Clean dependency tree |
| Reusability | System-wide accessibility |
| Separation of Concerns | Pure base model isolation |
| Future Extensibility | Easy to add shared models |

## Migration Strategy (Critical Order)

1. Create `core` app and define `User` model
2. Set `AUTH_USER_MODEL = 'core.User'` in settings
3. Register all apps in INSTALLED_APPS
4. Create migrations for all apps simultaneously
5. Apply migrations in one operation

---

# ⚠️ Critical Reminders

1. **Never change AUTH_USER_MODEL after migrations** - It's set for the project lifetime
2. **Core app must be in INSTALLED_APPS** - Other apps depend on it
3. **Always reference User as `settings.AUTH_USER_MODEL`** - Never import directly
4. **Document architectural decisions** - Future developers need to understand design choices

---

# Engineering Questions Considered During Design

## System Architecture Questions

* Should the system use monolithic or modular architecture?
* How can the project remain scalable as features grow?
* Which responsibilities belong to which modules?

## Authentication Questions

* Should user roles be separated or centralized?
* Should the system extend Django's default user model?
* How can permissions be managed securely?

## Database Design Questions

* How should relationships between farmers, collectors, and collections be structured?
* How can data consistency be maintained during transactions?
* Should transactional operations support rollback mechanisms?

## Scalability Questions

* Can the architecture support future Mpesa integration?
* Can AI features be added without restructuring the system?
* Can mobile applications consume the same APIs later?

## Maintainability Questions

* How can code duplication be minimized?
* How can future developers easily understand the system?
* How can debugging and testing be simplified?

---

# Software Engineering Principles Applied

1. **Single Responsibility Principle** - Each app handles one domain
2. **Separation of Concerns** - Clear boundaries between modules
3. **Don't Repeat Yourself (DRY)** - Shared logic in core app
4. **API-First Design** - All features exposed via REST endpoints
5. **Security by Design** - JWT authentication, environment variables
```


Here's the formatted section for your README.md:

```markdown
## Step 9: Register Models in Django Admin

Create `core/admin.py`:

```python
from django.contrib import admin
from .models import User, FarmerProfile, PorterProfile, MilkCollection, Complaint, Notice, Payment

# Register Custom User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')

# Register FarmerProfile
@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'farm_name', 'total_milk_delivered')
    search_fields = ('first_name', 'last_name', 'phone_number', 'national_id')
    list_filter = ('gender', 'join_date')

# Register PorterProfile
@admin.register(PorterProfile)
class PorterProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'employee_id', 'route_name', 'total_collections')
    search_fields = ('first_name', 'last_name', 'employee_id')
    list_filter = ('is_active', 'hire_date')

# Register MilkCollection
@admin.register(MilkCollection)
class MilkCollectionAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'liters', 'session', 'collection_date', 'total_amount')
    list_filter = ('session', 'collection_date')
    search_fields = ('farmer__first_name', 'farmer__last_name', 'porter__first_name', 'porter__last_name')
    readonly_fields = ('total_amount',)

# Register Complaint
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'farmer', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'farmer__first_name', 'farmer__last_name')

# Register Notice
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'target', 'is_important', 'created_at')
    list_filter = ('target', 'is_important')
    search_fields = ('title', 'message')

# Register Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method')
    search_fields = ('farmer__first_name', 'farmer__last_name', 'transaction_ref')
```

---

## Step 10: Create Admin Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:

```
Username: admin
Email: admin@example.com
Password: yourpassword
```

---

## Step 11: Run Development Server

```bash
python manage.py runserver
```

Access the applications:

- Admin Panel: http://127.0.0.1:8000/admin/
- API Endpoints: http://127.0.0.1:8000/api/

---

## Admin Panel Features

After registering all models, the Django admin panel provides:

| Model | Admin Capabilities |
|-------|-------------------|
| **User** | View, filter by role, search users |
| **FarmerProfile** | Manage farmer data, search by name/ID/national ID |
| **PorterProfile** | Manage porters, filter by active status |
| **MilkCollection** | View collections, filter by session/date, auto-calculated amounts |
| **Complaint** | Track and resolve farmer complaints |
| **Notice** | Create and manage announcements for different user groups |
| **Payment** | Track payment status and methods |

---

## Admin Screenshot

![Django Admin Panel](screenshots/django andmin.png)

![Django Admin Panel](screenshots/django andmin two.png)



# Step 12: Implement Core Authentication

MaziwaSync uses JWT (JSON Web Token) Authentication through Django REST Framework SimpleJWT.

The authentication module is responsible for:

* Registering Farmers
* Registering Porters
* User Login
* User Logout
* Token Refresh
* Retrieving Current Logged-in User Information

---

# Authentication URLs

Create `accounts/urls.py`

```python
from django.urls import path
from .views import LogoutView, RegisterView, LoginView, MeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView, name='register'),
    path('auth/login/', LoginView, name='login'),
    path('auth/logout/', LogoutView, name='logout'),
    path('auth/me/', MeView, name='me'),

    # Refresh Access Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

# JWT Configuration

Inside `settings.py`

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### Explanation

| Setting                  | Purpose                                    |
| ------------------------ | ------------------------------------------ |
| ACCESS_TOKEN_LIFETIME    | Access token expires after 1 minute        |
| REFRESH_TOKEN_LIFETIME   | Refresh token valid for 7 days             |
| ROTATE_REFRESH_TOKENS    | Generates a new refresh token each refresh |
| BLACKLIST_AFTER_ROTATION | Invalidates old refresh tokens             |

---

# Enable Token Blacklisting

Add the blacklist app inside `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...

    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    ...
]
```

---

# IMPORTANT: Run Migrations

After adding token blacklisting, migrations MUST be executed.

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the blacklist tables required for logout and token invalidation.

Failure to run migrations will cause logout functionality to fail.

---

# Registration Endpoint

URL

```http
POST /api/auth/register/
```

Permission

```text
Admin Only
```

The administrator creates farmer and porter accounts.

---

## Register Farmer Example

```json
{
    "username": "farmer001",
    "email": "farmer001@gmail.com",
    "password": "password123",
    "role": "farmer",
    "phone_number": "0712345678",

    "first_name": "John",
    "last_name": "Kamau",
    "national_id": "12345678",
    "farm_name": "Green Farm"
}
```

Response

```json
{
    "user_id": 2,
    "username": "farmer001",
    "role": "farmer",
    "message": "Farmer registered successfully."
}
```

---

## Register Porter Example

```json
{
    "username": "porter001",
    "email": "porter001@gmail.com",
    "password": "password123",
    "role": "porter",
    "phone_number": "0798765432",

    "first_name": "Peter",
    "last_name": "Mwangi",
    "employee_id": "EMP001",
    "national_id": "98765432",
    "route_name": "Route A"
}
```

Response

```json
{
    "user_id": 3,
    "username": "porter001",
    "role": "porter",
    "message": "Porter registered successfully."
}
```

---

# Login Endpoint

URL

```http
POST /api/auth/login/
```

Permission

```text
Public
```

Request

```json
{
    "username": "farmer001",
    "password": "password123"
}
```

Response

```json
{
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token",
    "user_id": 2,
    "username": "farmer001",
    "role": "farmer"
}
```

Store both tokens because they will be needed later.

---

# Current Logged User Endpoint

URL

```http
GET /api/auth/me/
```

Header

```http
Authorization: Bearer access_token
```

---

## Farmer Response

```json
{
    "id": 2,
    "username": "farmer001",
    "role": "farmer",
    "profile": {
        "first_name": "John",
        "last_name": "Kamau",
        "phone_number": "0712345678",
        "farm_name": "Green Farm"
    }
}
```

---

## Porter Response

```json
{
    "id": 3,
    "username": "porter001",
    "role": "porter",
    "profile": {
        "first_name": "Peter",
        "last_name": "Mwangi",
        "employee_id": "EMP001",
        "route_name": "Route A"
    }
}
```

---

# Refresh Token Endpoint

Since access tokens expire after one minute, the frontend should request a new access token using the refresh token.

URL

```http
POST /api/token/refresh/
```

Request

```json
{
    "refresh": "your_refresh_token"
}
```

Response

```json
{
    "access": "new_access_token",
    "refresh": "new_refresh_token"
}
```

---

# Logout Endpoint

URL

```http
POST /api/auth/logout/
```

Header

```http
Authorization: Bearer access_token
```

Body

```json
{
    "refresh": "your_refresh_token"
}
```

Response

```json
{
    "message": "Logout successful."
}
```

The refresh token is added to the blacklist and can no longer be used.

---

# Authentication Flow

```text
Admin Login
      │
      ▼
Create Farmer/Porter Account
      │
      ▼
User Login
      │
      ▼
Receive Access Token
Receive Refresh Token
      │
      ▼
Access Protected Endpoints
      │
      ▼
Access Token Expires
      │
      ▼
Call /token/refresh/
      │
      ▼
Receive New Access Token
      │
      ▼
Continue Using System
      │
      ▼
Logout
      │
      ▼
Refresh Token Blacklisted
```

---

# Testing Authentication Using Insomnia

## 1. Login

Create a POST request

```http
POST http://127.0.0.1:8000/api/auth/login/
```

Body → JSON

```json
{
    "username": "admin",
    "password": "adminpassword"
}
```

Copy:

* access token
* refresh token

---

## 2. Register Farmer

Create POST request

```http
POST http://127.0.0.1:8000/api/auth/register/
```

Header

```http
Authorization: Bearer ACCESS_TOKEN
```

Body

```json
{
    "username": "farmer001",
    "email": "farmer001@gmail.com",
    "password": "password123",
    "role": "farmer",
    "phone_number": "0712345678",
    "first_name": "John",
    "last_name": "Kamau",
    "national_id": "12345678",
    "farm_name": "Green Farm"
}
```

Expected Response

```json
{
    "message": "Farmer registered successfully."
}
```

---

## 3. Test Me Endpoint

Create GET request

```http
GET http://127.0.0.1:8000/api/auth/me/
```

Header

```http
Authorization: Bearer ACCESS_TOKEN
```

Expected Result

Current user information should be returned.

---

## 4. Test Expired Token

Wait one minute.

Call:

```http
GET /api/auth/me/
```

Expected Response

```json
{
    "detail": "Given token not valid for any token type"
}
```

---

## 5. Refresh Token

Create POST request

```http
POST http://127.0.0.1:8000/api/token/refresh/
```

Body

```json
{
    "refresh": "YOUR_REFRESH_TOKEN"
}
```

Expected Result

New access token returned.

---

## 6. Logout

Create POST request

```http
POST http://127.0.0.1:8000/api/auth/logout/
```

Header

```http
Authorization: Bearer ACCESS_TOKEN
```

Body

```json
{
    "refresh": "YOUR_REFRESH_TOKEN"
}
```

Expected Result

```json
{
    "message": "Logout successful."
}
```

The refresh token becomes invalid and cannot be reused.


# Add Milk Collection

This endpoint allows an authenticated porter to record milk supplied by a farmer.

The porter is identified automatically using the JWT access token.

# Milk Collection Serializer

Before returning milk collection records to the API client, Django REST Framework needs a serializer to convert model objects into JSON.

The `MilkCollectionSerializer` controls which fields are exposed to the frontend.

---

## Serializer Implementation

```python
from rest_framework import serializers
from core.models import MilkCollection

class MilkCollectionSerializer(serializers.ModelSerializer):
    farmer_name = serializers.SerializerMethodField()

    farmer_code = serializers.CharField(
        source='farmer.membership_number',
        read_only=True
    )

    class Meta:
        model = MilkCollection
        fields = [
            'id',
            'farmer_code',
            'farmer_name',
            'liters',
            'session',
            'total_amount',
            'collection_date',
        ]

    def get_farmer_name(self, obj):
        return f"{obj.farmer.first_name} {obj.farmer.last_name}"
```

---

## Why Do We Need a Serializer?

Database objects cannot be sent directly as JSON responses.

A serializer converts:

```python
MilkCollection Object
```

into:

```json
{
    "id": 1,
    "farmer_code": "FRM001",
    "farmer_name": "John Kamau",
    "liters": 55,
    "session": "EVENING",
    "total_amount": 2750,
    "collection_date": "2025-07-10"
}
```

---

## Understanding Each Field

### ID

```python
'id'
```

The unique collection record identifier.

Example:

```json
{
    "id": 1
}
```

---

### Farmer Code

```python
farmer_code = serializers.CharField(
    source='farmer.membership_number',
    read_only=True
)
```

Instead of returning the farmer's database ID, the serializer returns the membership number.

Example:

```json
{
    "farmer_code": "FRM001"
}
```

The value comes from:

```python
farmer.membership_number
```

---

### Farmer Name

```python
farmer_name = serializers.SerializerMethodField()
```

This field does not exist in the database.

It is generated dynamically.

```python
def get_farmer_name(self, obj):
    return f"{obj.farmer.first_name} {obj.farmer.last_name}"
```

Example:

```json
{
    "farmer_name": "John Kamau"
}
```

---

### Liters

```python
'liters'
```

The quantity of milk supplied.

Example:

```json
{
    "liters": 55
}
```

---

### Session

```python
'session'
```

Indicates whether the milk was collected during:

```text
MORNING
```

or

```text
EVENING
```

Example:

```json
{
    "session": "EVENING"
}
```

---

### Total Amount

```python
'total_amount'
```

The monetary value of the collected milk.

Example:

```json
{
    "total_amount": 2750
}
```

---

### Collection Date

```python
'collection_date'
```

The date the milk was collected.

Example:

```json
{
    "collection_date": "2025-07-10"
}
```

---

## Example Serialization Process

### Database Record

```text
MilkCollection
    id = 1
    farmer = John Kamau
    liters = 55
    session = EVENING
    total_amount = 2750
```

### Serialized Output

```json
{
    "id": 1,
    "farmer_code": "FRM001",
    "farmer_name": "John Kamau",
    "liters": 55,
    "session": "EVENING",
    "total_amount": 2750,
    "collection_date": "2025-07-10"
}
```

## Learning Outcome

After completing this example, students should understand:

* What a Serializer is
* Why Serializers are needed in DRF
* ModelSerializer
* SerializerMethodField
* Using `source`
* Read-only fields
* Converting Django models into JSON
* How serializers work with Class-Based Views


---

## View Implementation

```python
# function based
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddMilkCollection(request):

    # Get logged-in porter
    try:
        porter = request.user.porter_profile
    except PorterProfile.DoesNotExist:
        return Response(
            {"error": "Only porters can add milk collections."},
            status=status.HTTP_403_FORBIDDEN
        )

    farmer_code = request.data.get('farmer_code')

    try:
        farmer = FarmerProfile.objects.get(
            membership_number=farmer_code
        )
    except FarmerProfile.DoesNotExist:
        return Response(
            {"error": "Farmer not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    collection = MilkCollection.objects.create(
        farmer=farmer,
        porter=porter,
        liters=request.data.get('liters'),
        session=request.data.get('session')
    )

    return Response({
        "message": "Milk collection recorded successfully.",
        "collection_id": collection.id,
        "farmer": f"{farmer.first_name} {farmer.last_name}",
        "porter": f"{porter.first_name} {porter.last_name}",
        "liters": collection.liters
    }, status=status.HTTP_201_CREATED)
```

---

## How the Logic Works

### Step 1: Verify User is a Porter

```python
porter = request.user.porter_profile
```

The authenticated user is extracted from the JWT token.

If the user does not have a porter profile:

```python
return Response(
    {"error": "Only porters can add milk collections."},
    status=403
)
```

---

### Step 2: Find the Farmer

```python
farmer_code = request.data.get('farmer_code')
```

The farmer membership number is submitted by the porter.

Example:

```json
{
    "farmer_code": "FRM001"
}
```

The system searches for the farmer:

```python
farmer = FarmerProfile.objects.get(
    membership_number=farmer_code
)
```

---

### Step 3: Create Milk Collection

```python
collection = MilkCollection.objects.create(
    farmer=farmer,
    porter=porter,
    liters=request.data.get('liters'),
    session=request.data.get('session')
)
```

A milk collection record is created and linked to:

* The farmer
* The authenticated porter
* Quantity of milk
* Collection session

---

## Testing in Insomnia

### Endpoint

```http
POST http://127.0.0.1:8000/api/porters/milk-collections/add/
```

---

### Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

---

### Request Body

```json
{
    "farmer_code": "FRM001",
    "liters": 55,
    "session": "EVENING"
}
```

---

### Successful Response

```json
{
    "message": "Milk collection recorded successfully.",
    "collection_id": 1,
    "farmer": "John Kamau",
    "porter": "Peter Mwangi",
    "liters": 55
}
```

---

### Invalid Farmer

Request:

```json
{
    "farmer_code": "FRM999",
    "liters": 55,
    "session": "EVENING"
}
```

Response:

```json
{
    "error": "Farmer not found."
}
```

---

### Non-Porter User

If a Farmer or Administrator attempts the request:

```json
{
    "error": "Only porters can add milk collections."
}
```

---

## Learning Outcome

After completing this example, students should understand:

* JWT Authentication
* Using `request.user`
* Role-based authorization
* Querying related models
* Creating records with Django ORM
* Returning API responses with Django REST Framework
* Testing secured APIs using Insomnia

```
```

# View My Collections

This endpoint allows a porter to view all milk collections that they have personally recorded.

The porter is identified automatically from the JWT token.

---

## View Implementation

```python
class MyCollectionsView(generics.ListAPIView):
    serializer_class = MilkCollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        porter = self.request.user.porter_profile

        collections = (
            MilkCollection.objects
            .filter(porter=porter)
            .select_related('farmer')
            .order_by('-created_at')
        )

        return collections
```

---

## How the Logic Works

### Step 1: Verify User is Authenticated

```python
permission_classes = [IsAuthenticated]
```

Only users with a valid JWT access token can access this endpoint.

---

### Step 2: Get the Logged-in Porter

```python
porter = self.request.user.porter_profile
```

The authenticated user is extracted from the JWT token.

Example:

```text
Token → User → PorterProfile
```

The system automatically knows which porter is making the request.

No porter ID is required in the URL or request body.

---

### Step 3: Retrieve the Porter's Collections

```python
MilkCollection.objects.filter(
    porter=porter
)
```

This ensures a porter can only view their own records.

Example:

| Porter | Collections Returned     |
| ------ | ------------------------ |
| Peter  | Peter's collections only |
| James  | James's collections only |

---

### Step 4: Load Related Farmer Data

```python
.select_related('farmer')
```

This optimizes database queries by loading farmer information together with collection records.

Without this optimization:

```text
1 query for collections
+
many farmer queries
```

With `select_related()`:

```text
1 optimized query
```

---

### Step 5: Sort by Latest Records

```python
.order_by('-created_at')
```

Collections are displayed from newest to oldest.

Example:

```text
10:00 PM
08:00 PM
06:00 PM
```

---

## Testing in Insomnia

### Endpoint

```http
GET http://127.0.0.1:8000/api/porters/collections/my/
```

---

### Headers

```http
Authorization: Bearer <access_token>
```

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

---

### Request Body

No request body is required.

```http
GET /api/porters/collections/my/
```

---

## Successful Response

```json
[
    {
        "id": 12,
        "farmer": "John Kamau",
        "liters": "55.00",
        "session": "EVENING",
        "total_amount": "2750.00",
        "created_at": "2025-07-10T18:20:30Z"
    },
    {
        "id": 11,
        "farmer": "Mary Wanjiru",
        "liters": "40.00",
        "session": "MORNING",
        "total_amount": "2000.00",
        "created_at": "2025-07-10T08:15:10Z"
    }
]
```

---

## What the Response Means

| Field        | Description              |
| ------------ | ------------------------ |
| id           | Collection record ID     |
| farmer       | Farmer who supplied milk |
| liters       | Quantity collected       |
| session      | MORNING or EVENING       |
| total_amount | Calculated payment value |
| created_at   | Collection timestamp     |

---

## Example Scenario

Suppose Porter Peter records the following collections:

| Farmer        | Liters |
| ------------- | ------ |
| John Kamau    | 55     |
| Mary Wanjiru  | 40     |
| Samuel Kiptoo | 30     |

When Peter sends:

```http
GET /api/porters/collections/my/
```

The API returns only Peter's records.

If another porter logs in, they will only see their own collections.

This is possible because:

```python
.filter(porter=porter)
```

uses the authenticated user's porter profile.

---

## Learning Outcome

After completing this example, students should understand:

* JWT Authentication
* Class-Based Views (CBVs)
* ListAPIView
* QuerySet filtering
* Using `request.user`
* One-to-One relationships
* Database optimization with `select_related`
* Ordering query results
* Testing protected endpoints with Insomnia
* Returning serialized data using Django REST Framework



# Porter Dashboard

The Porter Dashboard provides a summary of the porter's daily milk collection activities.

Instead of returning individual collection records, this endpoint returns statistics and analytics for the current day.

---

## View Implementation

```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PorterDashboardView(request):

    try:
        porter = request.user.porter_profile
    except:
        return Response(
            {"error": "Only porters can access this dashboard."},
            status=403
        )

    today = timezone.now().date()

    collections = MilkCollection.objects.filter(
        porter=porter,
        collection_date=today
    )

    total_liters = collections.aggregate(
        total=Sum('liters')
    )['total'] or 0

    total_amount = collections.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_collections = collections.count()

    assigned_farmers = porter.assigned_farmers.count()

    return Response({
        "date": today,
        "assigned_farmers": assigned_farmers,
        "total_collections_today": total_collections,
        "total_liters_today": total_liters,
        "total_amount_today": total_amount
    })
```

---

## How the Logic Works

### Step 1: Verify the User is a Porter

```python
porter = request.user.porter_profile
```

The authenticated user is retrieved from the JWT token.

If the user is not a porter:

```python
return Response(
    {"error": "Only porters can access this dashboard."},
    status=403
)
```

---

### Step 2: Get Today's Date

```python
today = timezone.now().date()
```

Example:

```text
2025-07-10
```

The dashboard only displays statistics for the current day.

---

### Step 3: Retrieve Today's Collections

```python
collections = MilkCollection.objects.filter(
    porter=porter,
    collection_date=today
)
```

Example:

| Farmer | Liters |
| ------ | ------ |
| John   | 55     |
| Mary   | 40     |
| Samuel | 30     |

Only records collected today by the logged-in porter are included.

---

### Step 4: Calculate Total Liters

```python
total_liters = collections.aggregate(
    total=Sum('liters')
)['total'] or 0
```

Example:

```text
55 + 40 + 30 = 125 Liters
```

Result:

```json
{
    "total_liters_today": 125
}
```

---

### Step 5: Calculate Total Amount

```python
total_amount = collections.aggregate(
    total=Sum('total_amount')
)['total'] or 0
```

Example:

| Collection | Amount |
| ---------- | ------ |
| 2750       | KES    |
| 2000       | KES    |
| 1500       | KES    |

Total:

```text
2750 + 2000 + 1500 = 6250
```

---

### Step 6: Count Total Collections

```python
total_collections = collections.count()
```

Example:

```text
3 collection records
```

Result:

```json
{
    "total_collections_today": 3
}
```

---

### Step 7: Count Assigned Farmers

```python
assigned_farmers = porter.assigned_farmers.count()
```

Example:

If the porter is responsible for:

* John
* Mary
* Samuel
* David
* Ruth

Result:

```json
{
    "assigned_farmers": 5
}
```

---

## Testing in Insomnia

### Endpoint

```http
GET http://127.0.0.1:8000/api/porters/dashboard/
```

---

### Headers

```http
Authorization: Bearer <access_token>
```

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

---

### Request Body

No request body is required.

```http
GET /api/porters/dashboard/
```

---

## Successful Response

```json
{
    "date": "2025-07-10",
    "assigned_farmers": 25,
    "total_collections_today": 18,
    "total_liters_today": 820,
    "total_amount_today": 41000
}
```

---

## Response Fields

| Field                   | Description                         |
| ----------------------- | ----------------------------------- |
| date                    | Current date                        |
| assigned_farmers        | Farmers assigned to the porter      |
| total_collections_today | Number of collection records today  |
| total_liters_today      | Total milk collected today          |
| total_amount_today      | Total value of milk collected today |

---

## Example Scenario

Suppose Porter Peter has:

### Assigned Farmers

```text
25 Farmers
```

### Today's Collections

| Farmer | Liters | Amount |
| ------ | ------ | ------ |
| John   | 55     | 2750   |
| Mary   | 40     | 2000   |
| Samuel | 30     | 1500   |

The dashboard will calculate:

```text
Assigned Farmers = 25
Collections = 3
Total Liters = 125
Total Amount = 6250
```

Response:

```json
{
    "date": "2025-07-10",
    "assigned_farmers": 25,
    "total_collections_today": 3,
    "total_liters_today": 125,
    "total_amount_today": 6250
}
```

---

## Learning Outcome

After completing this example, students should understand:

* JWT Authentication
* Role-Based Access Control
* Filtering QuerySets
* Django ORM Aggregation
* Using `Sum()`
* Using `count()`
* Building Dashboard Analytics
* Returning Summary Statistics
* Testing Protected GET Endpoints with Insomnia
* Creating Real-World Business Dashboards using Django REST Framework

