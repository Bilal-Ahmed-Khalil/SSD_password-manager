from pathlib import Path

# === BASE CONFIG ===
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-xn2je#=+pbour0we7ec1*pt+xk2hhhgvx#-aj*rt-93%)@&$f7'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# === INSTALLED APPS ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'APPNAME', 
    'csp',
]

# === MIDDLEWARE ===
MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === URLS AND TEMPLATES ===
ROOT_URLCONF = 'PROJECTNAME.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PROJECTNAME.wsgi.application'

# === DATABASE ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === PASSWORD VALIDATION ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === INTERNATIONALIZATION ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# === STATIC AND MEDIA ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === EMAIL CONFIG ===
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "www.bilalahmedkhalil123456789@gmail.com"
EMAIL_HOST_PASSWORD = "ahjlvkgruflywmgi"
EMAIL_USE_TLS = True

# === ENCRYPTION KEY (FERNET) ===
KEY = b'v8Jg_MxD23z5U20QIAhgyrqnCLTbOGbj9oJHwr2VkUA='

# CSP Settings (Final Version for django-csp v4+)
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": ("'self'", "https://kit.fontawesome.com"),  # ✅ Allow FA script
        "style-src": ("'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com"),
        "font-src": ("'self'", "https://fonts.gstatic.com", "https://use.fontawesome.com"),
        "img-src": ("'self'", "data:", "cdn.example.com"),
        "connect-src": ("'self'",),
        "object-src": ("'none'",),
        "frame-ancestors": ("'none'",),
        "form-action": ("'self'",),
    }
}


# === SECURITY HEADERS ===s
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'