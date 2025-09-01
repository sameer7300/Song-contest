# 🔌 API Documentation

## Overview

The AI Song Contest Platform provides a web-based interface with Django views and forms. While primarily designed as a web application, this document outlines the key endpoints and their functionality.

## 🔐 Authentication Endpoints

### User Registration
- **URL**: `/accounts/signup/`
- **Method**: GET, POST
- **Purpose**: User registration with email verification
- **Fields**: username, email, password, gender, phone, city, age

### User Login
- **URL**: `/accounts/login/`
- **Method**: GET, POST
- **Purpose**: User authentication with email/username support
- **Features**: Automatic email verification for inactive users

### Password Reset
- **URL**: `/accounts/password-reset/`
- **Method**: GET, POST
- **Purpose**: Initiate password reset with email verification
- **Flow**: Request → Email Code → Verify → Reset Password

### Username Recovery
- **URL**: `/accounts/username-recovery/`
- **Method**: GET, POST
- **Purpose**: Recover forgotten username via email

## 🎵 Contest Endpoints

### Home Page
- **URL**: `/`
- **Method**: GET
- **Purpose**: Landing page with contest info and featured content
- **Data**: Winners, featured songs, top-rated songs, statistics

### Dashboard
- **URL**: `/dashboard/`
- **Method**: GET
- **Auth**: Required
- **Purpose**: User's personal dashboard
- **Data**: User's songs, winner status, submission statistics

### Song Upload
- **URL**: `/upload/`
- **Method**: GET, POST
- **Auth**: Required
- **Purpose**: Submit new songs to contest
- **Validation**: Phase checking, file format validation
- **Files**: Audio (MP3/WAV), Lyrics (TXT/PDF/DOC/DOCX)

### Browse Songs
- **URL**: `/browse/`
- **Method**: GET
- **Purpose**: Browse and search all submitted songs
- **Filters**: Language, genre, category, search term, sort options
- **Pagination**: 12 songs per page

### Song Detail
- **URL**: `/song/<int:song_id>/`
- **Method**: GET
- **Purpose**: View individual song with voting and comments
- **Features**: View count tracking, user vote display

### Vote on Song
- **URL**: `/song/<int:song_id>/vote/`
- **Method**: POST
- **Auth**: Required
- **Purpose**: Rate a song (1-5 stars) with optional comment
- **Validation**: One vote per user per song

### Add Comment
- **URL**: `/song/<int:song_id>/comment/`
- **Method**: POST
- **Auth**: Required
- **Purpose**: Add comment to a song
- **Moderation**: Comments can be approved/rejected by admin

### Edit Song
- **URL**: `/song/<int:song_id>/edit/`
- **Method**: GET, POST
- **Auth**: Required (owner only)
- **Purpose**: Edit song metadata (not files)

### Delete Song
- **URL**: `/song/<int:song_id>/delete/`
- **Method**: GET, POST
- **Auth**: Required (owner only)
- **Purpose**: Request song deletion with email verification

### Winners Page
- **URL**: `/winners/`
- **Method**: GET
- **Purpose**: Display all contest winners
- **Pagination**: 10 winners per page

### Leaderboard
- **URL**: `/leaderboard/`
- **Method**: GET
- **Purpose**: Show top-rated songs and active users

## 📧 Email Verification Endpoints

### Verify Email
- **URL**: `/email-verification/verify/`
- **Method**: GET, POST
- **Purpose**: Verify email with 6-digit code
- **Session**: Requires pending verification session
- **Timeout**: 15 minutes expiry

### Resend Code
- **URL**: `/email-verification/resend/`
- **Method**: POST
- **Purpose**: Resend verification code
- **Rate Limit**: Max 3 codes per 10 minutes
- **Response**: JSON with success/error status

## 🛡️ Admin Endpoints

### Admin Dashboard
- **URL**: `/manage/dashboard/`
- **Auth**: Staff required
- **Purpose**: Overview of platform statistics and recent activity

### Manage Users
- **URL**: `/manage/users/`
- **Auth**: Staff required
- **Purpose**: User management interface
- **Features**: Search, filter, edit user details

### Manage Songs
- **URL**: `/manage/songs/`
- **Auth**: Staff required
- **Purpose**: Song moderation and management
- **Actions**: Feature songs, mark as winners, delete

### Manage Winners
- **URL**: `/manage/winners/`
- **Auth**: Staff required
- **Purpose**: Winner selection and management
- **Features**: Set prize amounts, admin notes

### Manage Deadlines
- **URL**: `/manage/deadlines/`
- **Auth**: Staff required
- **Purpose**: Contest phase management
- **Features**: Set deadlines, change phases, automatic transitions

## 📊 Data Models

### Song Model Fields
```python
{
    "title": "string",
    "description": "text",
    "language": "choice[urdu, english]",
    "genre": "choice[pop, rock, classical, folk, electronic, hip_hop, jazz, country, other]",
    "ai_tool_used": "string",
    "audio_file": "file[mp3, wav]",
    "lyrics_file": "file[txt, pdf, doc, docx]",
    "tags": "many_to_many[Tag]",
    "view_count": "integer",
    "vote_count": "integer",
    "average_rating": "float",
    "is_featured": "boolean",
    "is_winner": "boolean"
}
```

### Vote Model Fields
```python
{
    "user": "foreign_key[User]",
    "song": "foreign_key[Song]",
    "rating": "choice[1, 2, 3, 4, 5]",
    "comment": "text[optional]",
    "created_at": "datetime"
}
```

### User Model Extensions
```python
{
    "phone_number": "string[optional]",
    "city": "string[optional]",
    "age": "integer[optional]",
    "gender": "choice[M, F, O, N]",
    "bio": "text[optional]",
    "avatar": "image[optional]",
    "website": "url[optional]",
    "social_media": "string[optional]",
    "total_votes_received": "integer",
    "total_songs_uploaded": "integer"
}
```

## 🔒 Security Features

### Authentication
- **Custom backends** supporting email/username login
- **Email verification** required for account activation
- **Password validation** (minimum 4 characters for user convenience)
- **Session management** with secure cookies

### File Upload Security
- **File type validation** using Django validators
- **File size limits** (50MB maximum)
- **Secure file storage** in organized directory structure
- **Extension whitelist** for audio and document files

### Rate Limiting
- **Email verification**: 3 codes per 10 minutes per user
- **Verification attempts**: Maximum 5 attempts per code
- **Automatic cleanup** of expired verification codes

## 🚀 Response Formats

### Success Response
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": {...}
}
```

### Error Response
```json
{
    "success": false,
    "message": "Error description",
    "errors": {...}
}
```

### Pagination Response
```json
{
    "count": 100,
    "next": "url_to_next_page",
    "previous": "url_to_previous_page",
    "results": [...]
}
```

## 📝 Usage Examples

### Submitting a Song
1. Ensure user is authenticated and contest is in submission phase
2. POST to `/upload/` with form data including audio and lyrics files
3. System validates files and creates Song record
4. Email confirmation sent to user
5. User statistics updated automatically

### Voting Process
1. User navigates to song detail page
2. Selects rating (1-5 stars) and optional comment
3. POST to `/song/<id>/vote/` with rating data
4. System checks for existing vote and updates/creates accordingly
5. Song's average rating recalculated automatically

### Phase Management
1. Admin sets contest deadlines via admin interface
2. System automatically checks and advances phases
3. Users see appropriate UI based on current phase
4. Email notifications sent for phase transitions

## 🔧 Configuration

### Required Environment Variables
- `SECRET_KEY`: Django secret key for cryptographic signing
- `EMAIL_HOST_USER`: SMTP username for email sending
- `EMAIL_HOST_PASSWORD`: SMTP password for email authentication

### Optional Environment Variables
- `DEBUG`: Enable/disable debug mode (default: False)
- Database configuration for production deployment

## 📈 Monitoring & Analytics

### Built-in Metrics
- **Song engagement**: Views, votes, ratings, comments
- **User activity**: Submissions, votes given, profile completeness
- **Contest progress**: Phase timing, participation rates
- **System health**: Email delivery, file upload success rates

### Admin Dashboard Features
- **Real-time statistics** display
- **Recent activity** monitoring
- **User engagement** metrics
- **Content moderation** tools
