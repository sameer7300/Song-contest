# 🚀 Deployment Guide

## Overview

This guide covers deploying the AI Song Contest Platform to various hosting environments, with specific focus on PythonAnywhere deployment.

## 🏗️ Pre-Deployment Checklist

### Environment Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed from `requirements.txt`
- [ ] Environment variables configured
- [ ] Database migrations completed
- [ ] Static files collected
- [ ] Superuser account created

### Security Configuration
- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured
- [ ] SMTP credentials secured
- [ ] File upload limits verified

## 🌐 PythonAnywhere Deployment

### 1. Account Setup
1. Create a PythonAnywhere account
2. Choose appropriate plan (Hacker plan minimum for custom domains)
3. Access the dashboard

### 2. File Upload
```bash
# Upload files via Git or file manager
git clone https://github.com/yourusername/ai-song-contest.git
cd ai-song-contest
```

### 3. Virtual Environment
```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.8 aicontest

# Install dependencies
pip install -r requirements.txt
```

### 4. Database Configuration
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 5. Web App Configuration
1. Go to Web tab in PythonAnywhere dashboard
2. Create new web app
3. Choose manual configuration
4. Set Python version to 3.8
5. Configure WSGI file path: `/home/yourusername/ai-song-contest/passenger_wsgi.py`

### 6. Static Files Setup
- **Static URL**: `/static/`
- **Static Directory**: `/home/yourusername/ai-song-contest/staticfiles/`
- **Media URL**: `/media/`
- **Media Directory**: `/home/yourusername/ai-song-contest/media/`

### 7. Environment Variables
```bash
# In PythonAnywhere console
echo 'export SECRET_KEY="your-production-secret-key"' >> ~/.bashrc
echo 'export DEBUG=False' >> ~/.bashrc
echo 'export EMAIL_HOST_USER="your-email@domain.com"' >> ~/.bashrc
echo 'export EMAIL_HOST_PASSWORD="your-email-password"' >> ~/.bashrc
source ~/.bashrc
```

### 8. Domain Configuration
1. Add custom domain in Web tab
2. Configure DNS settings:
   - **A Record**: Point to PythonAnywhere IP
   - **CNAME**: `www` subdomain
3. Update `ALLOWED_HOSTS` in settings

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ai_contest.wsgi:application"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - EMAIL_HOST_USER=${EMAIL_HOST_USER}
      - EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=aicontest
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## ☁️ Cloud Platform Deployment

### Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create ai-song-contest

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set EMAIL_HOST_USER="your-email"
heroku config:set EMAIL_HOST_PASSWORD="your-password"

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### DigitalOcean App Platform
```yaml
# app.yaml
name: ai-song-contest
services:
- name: web
  source_dir: /
  github:
    repo: yourusername/ai-song-contest
    branch: main
  run_command: gunicorn --worker-tmp-dir /dev/shm ai_contest.wsgi
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: SECRET_KEY
    value: your-secret-key
  - key: DEBUG
    value: "False"
  - key: EMAIL_HOST_USER
    value: your-email
  - key: EMAIL_HOST_PASSWORD
    value: your-password
databases:
- name: db
  engine: PG
  version: "13"
```

## 🗄️ Database Configuration

### PostgreSQL Production Setup
```python
# settings.py - Production database
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

### Migration Commands
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (if needed)
python manage.py flush
python manage.py migrate
```

## 📧 Email Configuration

### SMTP Settings
```python
# Production email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587  # or 465 for SSL
EMAIL_USE_TLS = True  # or EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your-email@domain.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'AI Song Contest <noreply@yourdomain.com>'
```

### Email Service Providers
- **Gmail**: Use App Passwords, enable 2FA
- **SendGrid**: API key authentication
- **Mailgun**: Domain verification required
- **Amazon SES**: AWS credentials needed

## 📁 Static Files & Media

### WhiteNoise Configuration
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Media Files
```python
# Production media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
```

## 🔐 Security Considerations

### Production Security
```python
# settings.py - Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS settings (if using HTTPS)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Environment Variables Security
- Never commit `.env` files to version control
- Use strong, unique secret keys
- Rotate credentials regularly
- Use environment-specific configurations

## 📊 Monitoring & Maintenance

### Health Checks
```python
# Add to urls.py
path('health/', lambda request: JsonResponse({'status': 'healthy'})),
```

### Log Configuration
```python
# settings.py - Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Backup Strategy
```bash
# Database backup
python manage.py dumpdata > backup.json

# Media files backup
tar -czf media_backup.tar.gz media/

# Restore database
python manage.py loaddata backup.json
```

## 🚨 Troubleshooting

### Common Issues

#### Static Files Not Loading
```bash
# Solution
python manage.py collectstatic --clear
python manage.py collectstatic --noinput
```

#### Email Not Sending
- Check SMTP credentials
- Verify firewall settings
- Test with Django shell:
```python
from django.core.mail import send_mail
send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
```

#### File Upload Errors
- Check file size limits
- Verify media directory permissions
- Ensure file format validation

#### Database Connection Issues
- Verify database credentials
- Check network connectivity
- Ensure database server is running

### Performance Optimization

#### Database Optimization
```python
# Use select_related and prefetch_related
songs = Song.objects.select_related('user').prefetch_related('tags')

# Add database indexes
class Meta:
    indexes = [
        models.Index(fields=['submitted_at']),
        models.Index(fields=['average_rating']),
    ]
```

#### Caching
```python
# Add Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## 📋 Deployment Checklist

### Pre-Production
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Database backup created
- [ ] SSL certificate installed

### Production Deployment
- [ ] Deploy to staging environment first
- [ ] Run full test suite
- [ ] Verify email functionality
- [ ] Test file uploads
- [ ] Check admin interface
- [ ] Monitor error logs
- [ ] Verify all pages load correctly

### Post-Deployment
- [ ] Monitor application logs
- [ ] Check email delivery
- [ ] Verify file upload functionality
- [ ] Test user registration flow
- [ ] Monitor performance metrics
- [ ] Set up automated backups

## 📞 Support

For deployment issues:
- **Email**: [info@spado.org.pk](mailto:info@spado.org.pk)
- **Documentation**: Check this guide and README.md
- **Issues**: Create GitHub issue with deployment details
