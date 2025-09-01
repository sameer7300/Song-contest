# 🎵 AI Song Contest Platform - Powered by SPADO

<div align="center">

![AI Song Contest](static/spado-logo.png)

**"Voices for Humanity" - "Stop Killer Robots"**

*A Django web platform for hosting AI-generated music competitions advocating for a global ban on Autonomous Weapons Systems*

[![Django](https://img.shields.io/badge/Django-5.0.7-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 🌟 Overview

The AI Song Contest Platform is a comprehensive web application designed to host music competitions where participants create original songs using AI music generation tools. The platform is organized by SPADO focuses on raising awareness about the humanitarian impact of Autonomous Weapons Systems and advocates for their global prohibition.

## ✨ Key Features

### 🎤 **Contest Management**
- **Phase-based contest system** with automatic progression
- **Submission tracking** with real-time statistics
- **Winner selection** with email notifications
- **Featured content** highlighting system

### 👥 **User Experience**
- **Comprehensive user profiles** with avatars and social links
- **Secure authentication** with email verification
- **Advanced search & filtering** by language, genre, rating
- **Interactive voting system** with 1-5 star ratings
- **Comment system** with moderation capabilities

### 🎵 **Song Management**
- **Multi-format support** (MP3, WAV for audio; TXT, PDF, DOC for lyrics)
- **File validation** with 50MB upload limits
- **Metadata tracking** (AI tool used, genre, language)
- **Engagement metrics** (views, votes, ratings)

### 📧 **Communication System**
- **6-digit verification codes** with 15-minute expiry
- **Rate limiting** (max 3 codes per 10 minutes)
- **Multiple verification types** (registration, login, password reset)
- **Automated notifications** for uploads and winner announcements

### 🛡️ **Security & Administration**
- **Custom authentication backends** supporting email/username login
- **CSRF protection** and secure middleware stack
- **Environment-based configuration** for sensitive data
- **Comprehensive admin interface** for platform management

## 🚀 Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend Framework** | Django | 5.0.7 |
| **Database** | SQLite (dev) / PostgreSQL (prod) | - |
| **Frontend** | Bootstrap + Custom CSS | 5.3.0 |
| **Authentication** | Django Auth + Custom Backends | - |
| **File Storage** | Local Media Files | - |
| **Email Service** | SMTP with Custom Templates | - |
| **Static Files** | WhiteNoise | 6.6.0 |
| **Deployment** | PythonAnywhere + Gunicorn | - |

## 📁 Project Architecture

```
ai-song-contest/
├── 🔐 accounts/                    # User authentication & profiles
│   ├── migrations/                 # Database migrations
│   ├── models.py                   # Custom User model
│   ├── views.py                    # Auth views (login, signup, etc.)
│   ├── forms.py                    # Authentication forms
│   ├── admin.py                    # User admin interface
│   └── backends.py                 # Custom auth backends
│
├── 🎵 contest/                     # Core contest functionality
│   ├── migrations/                 # Database migrations
│   ├── management/commands/        # Custom Django commands
│   ├── models.py                   # Song, Vote, Winner, Deadline models
│   ├── views.py                    # Contest views and logic
│   ├── forms.py                    # Contest forms
│   ├── admin.py                    # Contest admin interface
│   └── urls.py                     # URL routing
│
├── 📧 email_verification/          # Email verification system
│   ├── migrations/                 # Database migrations
│   ├── models.py                   # EmailVerification model
│   ├── views.py                    # Verification views
│   ├── services.py                 # Email service logic
│   └── forms.py                    # Verification forms
│
├── 🎨 templates/                   # HTML templates
│   ├── accounts/                   # Authentication templates
│   ├── contest/                    # Contest page templates
│   ├── email_verification/         # Email templates
│   └── base.html                   # Base template
│
├── 📦 static/                      # Static assets
│   ├── css/                        # Custom stylesheets
│   ├── js/                         # JavaScript files
│   └── spado-logo.png             # Platform logo
│
├── ⚙️ ai_contest/                  # Django project configuration
│   ├── settings.py                 # Application settings
│   ├── urls.py                     # Root URL configuration
│   └── wsgi.py                     # WSGI application
│
├── 📄 Documentation
│   ├── README.md                   # This file
│   ├── CHANGELOG.md                # Version history
│   ├── CONTRIBUTING.md             # Development guidelines
│   └── LICENSE                     # MIT License
│
└── 🔧 Configuration
    ├── requirements.txt            # Python dependencies (270+ packages)
    ├── .env.example               # Environment variables template
    ├── .gitignore                 # Git ignore patterns
    └── manage.py                  # Django management script
```

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+**
- **pip** (Python package manager)
- **Git** for version control
- **Virtual environment** (recommended)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-song-contest.git
   cd ai-song-contest
   ```

2. **Set up virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your settings
   # Required: SECRET_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
   ```

5. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open browser to `http://127.0.0.1:8000/`
   - Admin interface: `http://127.0.0.1:8000/admin/`

## 🎯 Usage Guide

### For Participants

1. **Registration**
   - Sign up with email verification
   - Complete profile with optional details (age, city, gender)

2. **Song Submission**
   - Upload AI-generated songs during submission phase
   - Provide metadata (title, description, AI tool used)
   - Include lyrics file and audio file

3. **Voting & Engagement**
   - Browse and listen to submitted songs
   - Rate songs (1-5 stars) with optional comments
   - View leaderboards and statistics

### For Administrators

1. **Contest Management**
   - Set contest phases and deadlines
   - Manage automatic phase transitions
   - Select winners and send notifications

2. **Content Moderation**
   - Review and approve comments
   - Feature outstanding submissions
   - Manage user accounts and permissions

## 🗃️ Database Schema

### Core Models

| Model | Purpose | Key Fields |
|-------|---------|------------|
| **User** | Extended user profiles | username, email, gender, bio, avatar, statistics |
| **Song** | Contest submissions | title, audio_file, lyrics_file, genre, language, ratings |
| **Vote** | Rating system | user, song, rating (1-5), comment |
| **Winner** | Contest results | song, selected_at, prize_amount, admin_notes |
| **Deadline** | Phase management | status, deadline_date, description |
| **EmailVerification** | Security system | user, code, verification_type, expires_at |

### Relationships
- **One-to-Many**: User → Songs, User → Votes, Song → Votes
- **Many-to-Many**: Song → Tags
- **One-to-One**: Song → Winner

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | ✅ | - |
| `DEBUG` | Debug mode | ❌ | False |
| `EMAIL_HOST_USER` | SMTP username | ✅ | - |
| `EMAIL_HOST_PASSWORD` | SMTP password | ✅ | - |

### Contest Phases

1. **Open for Submission** - Users can upload songs
2. **Judging** - Voting and evaluation period
3. **Winner Announced** - Results published with notifications

## 🚀 Deployment

### Production Deployment

1. **Server Setup**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure production settings
   export DEBUG=False
   export SECRET_KEY="your-production-secret-key"
   ```

2. **Database Migration**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

3. **WSGI Configuration**
   - Use `passenger_wsgi.py` for PythonAnywhere
   - Configure `gunicorn` for other platforms

### Environment Setup
- **Development**: SQLite database
- **Production**: PostgreSQL recommended
- **Static Files**: WhiteNoise for serving
- **Media Files**: Local storage with 50MB limit

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Check code style
flake8 .

# Run with coverage
pytest --cov=.
```

## 📊 Features Deep Dive

### Authentication System
- **Email or username login** support
- **Secure password reset** with email verification
- **Username recovery** functionality
- **Account activation** via email codes

### Contest Management
- **Automated phase transitions** based on deadlines
- **Real-time statistics** tracking
- **Winner selection** with email notifications
- **Featured content** promotion system

### File Handling
- **Audio formats**: MP3, WAV (max 50MB)
- **Lyrics formats**: TXT, PDF, DOC, DOCX
- **Validation**: File type and size checking
- **Storage**: Organized by upload type and date

### Email System
- **SMTP integration** with custom templates
- **Rate limiting**: 3 codes per 10 minutes
- **Multiple verification types** for different actions
- **Automatic cleanup** of expired codes

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit with descriptive messages: `git commit -m 'Add amazing feature'`
5. Push to your fork: `git push origin feature/amazing-feature`
6. Submit a pull request

### Code Standards
- Follow **PEP 8** Python style guidelines
- Use **meaningful variable names** and comments
- Write **tests** for new functionality
- Update **documentation** for changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact [info@spado.org.pk](mailto:info@spado.org.pk)

### Common Issues
- **Email not sending**: Check SMTP configuration in `.env`
- **File upload errors**: Verify file size and format requirements
- **Database errors**: Run `python manage.py migrate`

## 🏆 About the Contest

The National AI Song Contest is organized to raise awareness about the humanitarian implications of Autonomous Weapons Systems. Through the power of AI-generated music, we aim to amplify voices calling for a global ban on lethal autonomous weapons.

### Contest Theme
**"Voices for Humanity"** encourages participants to create songs that:
- Highlight the value of human life and dignity
- Advocate for peaceful conflict resolution
- Call for international cooperation on AI governance
- Promote ethical AI development and deployment

---

<div align="center">

**Made with ❤️ for Humanity**

[🌐 Website](https://contest.spado.org.pk) • [📧 Contact](mailto:info@spado.org.pk) • [🐛 Report Issues](https://github.com/yourusername/ai-song-contest/issues)

</div>
