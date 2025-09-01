# 🤝 Contributing to AI Song Contest Platform

Thank you for your interest in contributing to the AI Song Contest platform! We welcome all contributions from the community.

## 🌟 Ways to Contribute

- 🐛 Report bugs and issues
- ✨ Suggest new features
- 💻 Submit code improvements
- 📚 Improve documentation
- 🧪 Write tests
- 🎨 Enhance UI/UX

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
git clone https://github.com/yourusername/ai-song-contest.git
cd ai-song-contest
git remote add upstream https://github.com/original/ai-song-contest.git
```

### 2. Development Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Database setup
python manage.py migrate
python manage.py createsuperuser
```

## 📋 Development Guidelines

### Code Style
- **Follow PEP 8** Python style guidelines
- **Use Black** for formatting: `black .`
- **Use isort** for imports: `isort .`
- **Run flake8** for linting: `flake8 .`
- **Maximum line length**: 88 characters

### Django Best Practices
- Use class-based views where appropriate
- Follow Django naming conventions
- Implement proper error handling
- Use Django's security features
- Write comprehensive tests

### Testing
```bash
# Run tests
python manage.py test

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔄 Workflow Process

1. **Create branch**: `git checkout -b feature/your-feature`
2. **Make changes** with descriptive commits
3. **Test thoroughly** and ensure code quality
4. **Update documentation** if needed
5. **Submit pull request** with clear description

## 📝 Commit Guidelines

### Format
```
type(scope): description

[optional body]
```

### Types
- **feat**: New feature
- **fix**: Bug fix  
- **docs**: Documentation
- **style**: Formatting
- **refactor**: Code restructuring
- **test**: Adding tests
- **chore**: Maintenance

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers learn
- Focus on project goals

## 📞 Support

- **GitHub Issues**: Bug reports and features
- **Email**: [info@spado.org.pk](mailto:info@spado.org.pk)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
