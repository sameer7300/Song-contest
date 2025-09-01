# 🛠️ Development Guide

## Development Environment Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool
- Code editor (VS Code recommended)

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/ai-song-contest.git
cd ai-song-contest

# Setup virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Environment configuration
cp .env.example .env
# Edit .env with your local settings

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 🏗️ Project Architecture

### Django Apps Structure
- **accounts/**: User authentication and profile management
- **contest/**: Core contest functionality and song management
- **email_verification/**: Email verification system
- **ai_contest/**: Project configuration and settings

### Key Design Patterns
- **Model-View-Template (MVT)**: Django's architectural pattern
- **Custom User Model**: Extended AbstractUser for additional fields
- **Service Layer**: EmailVerificationService for email operations
- **Form-based Validation**: Django forms for data validation
- **Signal-based Actions**: Automatic updates via Django signals

## 🗃️ Database Design

### Entity Relationships
```
User (1) ──── (N) Song
User (1) ──── (N) Vote
User (1) ──── (N) Comment
User (1) ──── (N) EmailVerification
Song (1) ──── (N) Vote
Song (1) ──── (N) Comment
Song (1) ──── (1) Winner
Song (N) ──── (N) Tag
```

### Model Conventions
- Use descriptive field names
- Include created_at/updated_at timestamps
- Implement __str__ methods for admin display
- Add Meta classes for ordering and constraints
- Use choices for predefined options

## 🎨 Frontend Development

### Template Structure
```
templates/
├── base.html                    # Base template with navigation
├── accounts/                    # Authentication templates
├── contest/                     # Contest-related templates
└── email_verification/          # Email templates
```

### CSS Framework
- **Bootstrap 5.3.0** for responsive design
- **Custom CSS** for theme-specific styling
- **Font Awesome** for icons
- **CSS Variables** for consistent theming

### JavaScript Guidelines
- Use vanilla JavaScript for simple interactions
- Implement progressive enhancement
- Follow accessibility guidelines
- Minimize external dependencies

## 🧪 Testing Strategy

### Test Types
```python
# Unit Tests
class SongModelTest(TestCase):
    def test_song_creation(self):
        # Test model creation and validation
        pass

# View Tests
class SongViewTest(TestCase):
    def test_upload_song_view(self):
        # Test view responses and redirects
        pass

# Form Tests
class SongFormTest(TestCase):
    def test_valid_form_submission(self):
        # Test form validation
        pass
```

### Test Data
- Use Django fixtures for consistent test data
- Create factory classes for complex objects
- Mock external services (email, file uploads)
- Test both success and failure scenarios

## 🔧 Development Tools

### Code Quality
```bash
# Formatting
black .
isort .

# Linting
flake8 .
pylint **/*.py

# Type checking
mypy .

# Security scanning
bandit -r .
```

### Database Tools
```bash
# Create migrations
python manage.py makemigrations

# Check migration status
python manage.py showmigrations

# SQL inspection
python manage.py sqlmigrate app_name migration_name

# Database shell
python manage.py dbshell
```

### Django Management
```bash
# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# Load fixtures
python manage.py loaddata fixture_name.json
```

## 📊 Performance Considerations

### Database Optimization
- Use `select_related()` for foreign key relationships
- Use `prefetch_related()` for many-to-many relationships
- Add database indexes for frequently queried fields
- Implement pagination for large datasets

### Caching Strategy
- Cache expensive database queries
- Use template fragment caching
- Implement view-level caching where appropriate
- Consider Redis for session storage

### File Handling
- Validate file types and sizes
- Implement proper file storage organization
- Consider cloud storage for production
- Optimize image uploads with compression

## 🔒 Security Best Practices

### Authentication Security
- Use Django's built-in authentication
- Implement proper session management
- Add rate limiting for sensitive operations
- Use HTTPS in production

### Data Validation
- Validate all user inputs
- Use Django forms for validation
- Implement CSRF protection
- Sanitize file uploads

### Email Security
- Use environment variables for credentials
- Implement rate limiting for email sending
- Validate email addresses
- Use secure SMTP connections

## 🚀 Deployment Preparation

### Pre-deployment Checklist
- [ ] All tests passing
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Security settings enabled
- [ ] Error logging configured

### Environment Configuration
```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🐛 Debugging

### Common Issues
- **Migration conflicts**: Use `--merge` flag or manual resolution
- **Static files not loading**: Run `collectstatic` and check settings
- **Email not sending**: Verify SMTP configuration
- **File upload errors**: Check file size and format validation

### Debug Tools
```python
# Django Debug Toolbar (development only)
if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

### Logging Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

## 📈 Monitoring

### Application Metrics
- Track user registration and activity
- Monitor song upload success rates
- Measure email delivery performance
- Analyze contest participation

### Error Tracking
- Implement error logging
- Use Django's built-in error reporting
- Monitor 404 and 500 errors
- Track performance bottlenecks

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Django CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test
    
    - name: Check code style
      run: |
        black --check .
        flake8 .
```

## 📚 Additional Resources

### Django Documentation
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [Django Security Guide](https://docs.djangoproject.com/en/stable/topics/security/)

### Python Resources
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Documentation](https://docs.python.org/)
- [Real Python](https://realpython.com/)

### Testing Resources
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [Factory Boy](https://factoryboy.readthedocs.io/)

---

**Happy coding! 🎵**
