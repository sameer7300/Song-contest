# AI Song Contest Platform

A web platform for hosting AI-generated music competitions where users can submit, vote, and share AI-created songs.

## Features

- User authentication (signup, login, password reset)
- Song submission with audio and lyrics
- Song browsing and filtering
- Voting and rating system
- User profiles and dashboards
- Email verification system
- Admin dashboard for contest management

## Recent Updates (August 2025)

### Added
- Gender field to user profiles with options: Male, Female, Other, Prefer not to say
- Enhanced user profile management
- Improved form validation and user experience

### Removed
- Category field from songs to simplify the submission process
- Unused category-related code and templates

### Fixed
- Email verification flow
- Password reset functionality
- Form validation errors

## Technology Stack

- **Backend**: Django 5.0.7
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: PythonAnywhere
- **Version Control**: Git

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-song-contest.git
   cd ai-song-contest
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the environment variables in `.env`

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000/`

## Project Structure

```
ai-song-contest/
├── accounts/               # User authentication and profiles
├── ai_contest/             # Project configuration
├── contest/                # Main application
│   ├── migrations/         # Database migrations
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # HTML templates
│   ├── admin.py            # Admin configuration
│   ├── apps.py             # App configuration
│   ├── forms.py            # Form definitions
│   ├── models.py           # Database models
│   ├── urls.py             # URL routing
│   └── views.py            # View functions
├── email_verification/     # Email verification system
├── static/                 # Global static files
├── templates/              # Global templates
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── manage.py               # Django management script
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## Deployment

### Production

1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables in production
3. Set `DEBUG = False` in settings.py
4. Configure static files for production:
   ```bash
   python manage.py collectstatic
   ```
5. Set up a production WSGI server (e.g., Gunicorn with Nginx)

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [your-email@example.com](mailto:your-email@example.com)
