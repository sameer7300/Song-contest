from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.http import JsonResponse
from .models import Song, Vote, Comment, Winner, Deadline, Category, Tag
from .forms import SongUploadForm, VoteForm, CommentForm, SongSearchForm, SongForm
from django.contrib.auth import get_user_model
from .models import Song, Vote, Comment, Winner, Category, Tag, Deadline
from .forms import SongUploadForm, VoteForm, CommentForm, SongSearchForm
from email_verification.services import EmailVerificationService

User = get_user_model()

def home(request):
    """Home page showing contest info and recent winners"""
    winners = Winner.objects.select_related('song__user').order_by('-selected_at')[:3]
    featured_songs = Song.objects.filter(is_featured=True).order_by('-submitted_at')[:6]
    top_rated_songs = Song.objects.filter(average_rating__gt=0).order_by('-average_rating')[:3]
    
    # Check and advance phases if needed
    Deadline.check_and_advance_phases()
    
    # Get current contest phase
    current_phase = Deadline.get_current_phase()
    can_submit = Deadline.can_submit_songs()
    
    context = {
        'winners': winners,
        'featured_songs': featured_songs,
        'top_rated_songs': top_rated_songs,
        'total_submissions': Song.objects.count(),
        'total_participants': Song.objects.values('user').distinct().count(),
        'total_votes': Vote.objects.count(),
        'current_phase': current_phase,
        'can_submit_songs': can_submit,
    }
    return render(request, 'contest/home.html', context)

@login_required
def dashboard(request):
    """User dashboard showing their submissions and winner status"""
    user_songs = Song.objects.filter(user=request.user).order_by('-submitted_at')
    user_winners = Winner.objects.filter(song__user=request.user).select_related('song')
    
    context = {
        'user_songs': user_songs,
        'user_winners': user_winners,
        'total_submissions': user_songs.count(),
    }
    return render(request, 'contest/dashboard.html', context)

@login_required
def upload_song(request):
    """Upload a new song"""
    # Check and advance phases if needed
    Deadline.check_and_advance_phases()
    
    # Check if song submissions are currently allowed
    if not Deadline.can_submit_songs():
        current_phase = Deadline.get_current_phase()
        phase_message = Deadline.get_phase_message()
        
        context = {
            'current_phase': current_phase,
            'phase_message': phase_message,
            'can_submit': False,
        }
        return render(request, 'contest/upload_song.html', context)
    
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.user = request.user
            
            # Calculate file size
            if song.audio_file:
                song.file_size_mb = song.audio_file.size / (1024 * 1024)
            
            song.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            
            # Update user statistics
            request.user.total_songs_uploaded = Song.objects.filter(user=request.user).count()
            request.user.save(update_fields=['total_songs_uploaded'])
            
            # Send upload confirmation email
            try:
                EmailVerificationService.send_notification_email(
                    request.user, 
                    request.user.email, 
                    'song_upload',
                    {'song': song}
                )
            except Exception as e:
                # Don't fail the upload if email fails
                pass
            
            messages.success(request, 'Song uploaded successfully! Check your email for confirmation.')
            return redirect('contest:dashboard')
        else:
            # Debug form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SongUploadForm()
    
    context = {
        'form': form,
        'can_submit': True,
        'current_phase': Deadline.get_current_phase(),
    }
    return render(request, 'contest/upload_song.html', context)

def winners_page(request):
    """Page showing all winners"""
    winners = Winner.objects.select_related('song__user').order_by('-selected_at')
    paginator = Paginator(winners, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'contest/winners.html', {'page_obj': page_obj})

def song_detail(request, song_id):
    """View individual song details with voting and comments"""
    song = get_object_or_404(Song, id=song_id)
    
    # Increment view count
    song.increment_view_count()
    
    # Get user's existing vote if any
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(user=request.user, song=song)
        except Vote.DoesNotExist:
            pass
    
    # Get comments
    comments = Comment.objects.filter(song=song, is_approved=True).select_related('user')[:10]
    
    # Forms
    vote_form = VoteForm()
    comment_form = CommentForm()
    
    context = {
        'song': song,
        'user_vote': user_vote,
        'comments': comments,
        'vote_form': vote_form,
        'comment_form': comment_form,
    }
    return render(request, 'contest/song_detail.html', context)

@login_required
@require_POST
def vote_song(request, song_id):
    """Vote on a song"""
    song = get_object_or_404(Song, id=song_id)
    
    # Check if user already voted
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        song=song,
        defaults={'rating': int(request.POST.get('rating', 5))}
    )
    
    if not created:
        # Update existing vote
        vote.rating = int(request.POST.get('rating', 5))
        vote.save()
        messages.success(request, 'Your vote has been updated!')
    else:
        messages.success(request, 'Thank you for voting!')
    
    # Update song rating
    song.update_rating()
    
    return redirect('contest:song_detail', song_id=song.id)

@login_required
@require_POST
def add_comment(request, song_id):
    """Add a comment to a song"""
    song = get_object_or_404(Song, id=song_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.song = song
        comment.save()
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Please enter a valid comment.')
    
    return redirect('contest:song_detail', song_id=song.id)

def browse_songs(request):
    """Browse all songs with search and filtering"""
    form = SongSearchForm(request.GET)
    songs = Song.objects.select_related('user', 'category').prefetch_related('tags')
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        language = form.cleaned_data.get('language')
        genre = form.cleaned_data.get('genre')
        category = form.cleaned_data.get('category')
        sort_by = form.cleaned_data.get('sort_by', 'newest')
        
        # Apply filters
        if search:
            songs = songs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )
        
        if language:
            songs = songs.filter(language=language)
        
        if genre:
            songs = songs.filter(genre=genre)
        
        if category:
            songs = songs.filter(category=category)
        
        # Apply sorting
        if sort_by == 'oldest':
            songs = songs.order_by('submitted_at')
        elif sort_by == 'most_voted':
            songs = songs.order_by('-vote_count')
        elif sort_by == 'highest_rated':
            songs = songs.order_by('-average_rating')
        elif sort_by == 'most_viewed':
            songs = songs.order_by('-view_count')
        else:  # newest
            songs = songs.order_by('-submitted_at')
    
    # Pagination
    paginator = Paginator(songs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'total_results': songs.count(),
    }
    return render(request, 'contest/browse_songs.html', context)

def leaderboard(request):
    """Show leaderboard of top artists and songs"""
    # Top artists by total votes received
    top_artists = (Song.objects
                   .values('user__username', 'user__first_name', 'user__last_name')
                   .annotate(
                       total_votes=Count('votes'),
                       avg_rating=Avg('votes__rating'),
                       song_count=Count('id')
                   )
                   .filter(total_votes__gt=0)
                   .order_by('-total_votes')[:10])
    
    # Top songs by rating
    top_songs = Song.objects.filter(average_rating__gt=0).order_by('-average_rating')[:10]
    
    # Most viewed songs
    most_viewed = Song.objects.filter(view_count__gt=0).order_by('-view_count')[:10]
    
    context = {
        'top_artists': top_artists,
        'top_songs': top_songs,
        'most_viewed': most_viewed,
    }
    return render(request, 'contest/leaderboard.html', context)

# Admin helper function
def is_admin(user):
    """Check if user is admin (staff or superuser)"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with overview statistics"""
    from django.db.models import Count
    
    total_users = User.objects.count()
    total_songs = Song.objects.count()
    total_votes = Vote.objects.count()
    total_comments = Comment.objects.count()
    
    # Additional stats
    active_users = User.objects.filter(is_active=True).count()
    featured_songs = Song.objects.filter(is_featured=True).count()
    total_winners = Winner.objects.count()
    winner_songs = Song.objects.filter(is_winner=True).count()
    
    # Recent activity
    recent_songs = Song.objects.select_related('user').order_by('-submitted_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_votes = Vote.objects.select_related('user', 'song').order_by('-created_at')[:5]
    
    # Demographics - using available fields
    city_stats = User.objects.exclude(city__isnull=True).exclude(city__exact='').values('city').annotate(count=Count('id')).order_by('-count')[:5]
    verified_users = User.objects.filter(is_verified=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    # Current deadline and all deadlines
    current_deadline = Deadline.get_current_phase()
    all_deadlines = Deadline.objects.all().order_by('-deadline_date')
    
    context = {
        'total_users': total_users,
        'total_songs': total_songs,
        'total_votes': total_votes,
        'total_comments': total_comments,
        'active_users': active_users,
        'featured_songs': featured_songs,
        'total_winners': total_winners,
        'winner_songs': winner_songs,
        'recent_songs': recent_songs,
        'recent_users': recent_users,
        'recent_votes': recent_votes,
        'city_stats': city_stats,
        'verified_users': verified_users,
        'staff_users': staff_users,
        'current_deadline': current_deadline,
        'all_deadlines': all_deadlines,
    }
    return render(request, 'contest/admin_dashboard.html', context)

@user_passes_test(is_admin)
def admin_users(request):
    """Admin page for managing users"""
    users_list = User.objects.select_related().order_by('-date_joined')

    # Search and filter functionality
    search = request.GET.get('search')
    status = request.GET.get('status')
    role = request.GET.get('role')
    verified = request.GET.get('verified')
    sort = request.GET.get('sort', '-date_joined')

    if search:
        users_list = users_list.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    if status == 'active':
        users_list = users_list.filter(is_active=True)
    elif status == 'inactive':
        users_list = users_list.filter(is_active=False)

    if role == 'staff':
        users_list = users_list.filter(is_staff=True)
    elif role == 'superuser':
        users_list = users_list.filter(is_superuser=True)
    elif role == 'user':
        users_list = users_list.filter(is_staff=False, is_superuser=False)

    if verified == 'yes':
        users_list = users_list.filter(is_verified=True)
    elif verified == 'no':
        users_list = users_list.filter(is_verified=False)

    users_list = users_list.order_by(sort)

    # Stats
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    verified_users = User.objects.filter(is_verified=True).count()
    staff_users = User.objects.filter(is_staff=True).count()

    # Pagination
    paginator = Paginator(users_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_users': total_users,
        'active_users': active_users,
        'verified_users': verified_users,
        'staff_users': staff_users,
        'search': search,
        'status': status,
        'role': role,
        'verified': verified,
        'sort': sort,
    }
    return render(request, 'contest/admin_users.html', context)

@user_passes_test(is_admin)
def admin_edit_user(request, user_id):
    """Admin page for editing a specific user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.is_active = request.POST.get('is_active') == 'on'
            user.is_staff = request.POST.get('is_staff') == 'on'
            user.save()
            messages.success(request, f'User {user.username} updated successfully.')
        
        elif action == 'reset_password':
            # This would typically send a password reset email
            messages.success(request, f'Password reset email sent to {user.email}.')
        
        elif action == 'delete_user':
            username = user.username
            user.delete()
            messages.success(request, f'User {username} deleted successfully.')
            return redirect('contest:admin_users')
    
    # Get user's songs and activity
    user_songs = Song.objects.filter(user=user).order_by('-submitted_at')[:10]
    user_votes = Vote.objects.filter(user=user).select_related('song').order_by('-created_at')[:10]
    
    context = {
        'profile_user': user,
        'user_songs': user_songs,
        'user_votes': user_votes,
    }
    return render(request, 'contest/admin_edit_user.html', context)

@user_passes_test(is_admin)
def admin_songs(request):
    """Admin page for managing songs"""
    songs = Song.objects.select_related('user', 'category').prefetch_related('tags').order_by('-submitted_at')
    
    # Search and filter functionality
    search = request.GET.get('search')
    status = request.GET.get('status')
    
    if search:
        songs = songs.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(user__username__icontains=search)
        )
    
    if status == 'featured':
        songs = songs.filter(is_featured=True)
    elif status == 'pending':
        songs = songs.filter(is_approved=False)
    elif status == 'approved':
        songs = songs.filter(is_approved=True)
    
    # Pagination
    paginator = Paginator(songs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
    }
    return render(request, 'contest/admin_songs.html', context)

@user_passes_test(is_admin)
def admin_winners(request):
    """Admin page for managing contest winners"""
    winners = Winner.objects.select_related('song__user').order_by('-selected_at')
    
    # Get eligible songs for winner selection (all songs, ordered by rating)
    eligible_songs = Song.objects.all().order_by('-average_rating')[:50]
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'select_winners':
            first_place = request.POST.get('first_place')
            second_place = request.POST.get('second_place')
            third_place = request.POST.get('third_place')
            
            # Clear existing winners for current period (simplified)
            Winner.objects.all().delete()
            
            # Create new winners
            if first_place:
                song = Song.objects.get(id=first_place)
                Winner.objects.create(song=song, position=1)
            
            if second_place:
                song = Song.objects.get(id=second_place)
                Winner.objects.create(song=song, position=2)
            
            if third_place:
                song = Song.objects.get(id=third_place)
                Winner.objects.create(song=song, position=3)
            
            messages.success(request, 'Winners selected successfully!')
            return redirect('contest:admin_winners')
        
        elif action == 'remove_winner':
            winner_id = request.POST.get('winner_id')
            winner = get_object_or_404(Winner, id=winner_id)
            winner.delete()
            messages.success(request, 'Winner removed successfully!')
            return redirect('contest:admin_winners')
    
    context = {
        'winners': winners,
        'eligible_songs': eligible_songs,
    }
    return render(request, 'contest/admin_winners.html', context)

@user_passes_test(is_admin)
def admin_deadlines(request):
    """Admin page for managing contest deadlines"""
    deadlines = Deadline.objects.all()
    
    now = timezone.now()
    current_phase = deadlines.filter(deadline_date__gte=now).order_by('deadline_date').first()
    if not current_phase:
        current_phase = deadlines.order_by('-deadline_date').first()

    context = {
        'deadlines': deadlines,
        'current_phase': current_phase
    }
    return render(request, 'contest/admin_deadlines.html', context)

@login_required
def edit_song(request, song_id):
    """Edit song details (metadata only, not files)"""
    song = get_object_or_404(Song, id=song_id, user=request.user)
    
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, 'Song updated successfully!')
            return redirect('contest:song_detail', song_id=song.id)
    else:
        form = SongForm(instance=song)
    
    context = {
        'form': form,
        'song': song,
    }
    return render(request, 'contest/edit_song.html', context)

@login_required
def delete_song_request(request, song_id):
    """Request song deletion with email verification"""
    from email_verification.models import EmailVerification
    from django.core.mail import send_mail
    from django.conf import settings
    import random
    import string
    
    song = get_object_or_404(Song, id=song_id, user=request.user)
    
    if request.method == 'POST':
        # Generate verification code
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        # Create email verification record
        EmailVerification.objects.filter(
            user=request.user,
            verification_type='song_deletion'
        ).delete()  # Remove any existing codes
        
        email_verification = EmailVerification.objects.create(
            user=request.user,
            email=request.user.email,
            code=verification_code,
            verification_type='song_deletion'
        )
        
        # Send email using the template
        try:
            admin_email = getattr(settings, 'ADMIN_EMAIL', 'info@spado.org.pk')
            
            email_context = {
                'user': request.user,
                'song': song,
                'verification_code': verification_code,
                'admin_email': admin_email,
            }
            
            html_message = render_to_string('email_verification/song_deletion_email.html', email_context)
            plain_message = f'Your verification code for deleting "{song.title}" is: {verification_code}'

            send_mail(
                subject=f'Song Deletion Verification - {song.title}',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                html_message=html_message
            )
            messages.success(request, 'Verification code sent to your email!')
            return redirect('contest:delete_song_verify', song_id=song.id)
        except Exception as e:
            messages.error(request, f'Failed to send verification email: {e}')
    
    context = {'song': song}
    return render(request, 'contest/delete_song_request.html', context)

@login_required
def delete_song_verify(request, song_id):
    """Verify deletion code and delete song"""
    from email_verification.models import EmailVerification
    from django.core.mail import send_mail
    from django.conf import settings
    import os
    
    try:
        song = Song.objects.get(id=song_id, user=request.user)
    except Song.DoesNotExist:
        messages.error(request, 'The song you are trying to delete does not exist or you do not have permission to delete it.')
        return redirect('contest:dashboard')
    
    if request.method == 'POST':
        from email_verification.forms import EmailVerificationForm
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            
            try:
                # Check if song still exists before proceeding
                if not Song.objects.filter(id=song_id, user=request.user).exists():
                    messages.error(request, 'The song you are trying to delete no longer exists.')
                    return redirect('contest:dashboard')
                    
                verification = EmailVerification.objects.get(
                    user=request.user,
                    code=code,
                    verification_type='song_deletion',
                    is_used=False
                )
                
                if verification.is_expired():
                    messages.error(request, 'Verification code has expired. Please request a new one.')
                    return redirect('contest:delete_song_request', song_id=song_id)
                
                # Mark as used
                verification.is_used = True
                verification.save()
                
                # Get fresh instance of song
                song = Song.objects.get(id=song_id, user=request.user)
                
                # Delete song files
                if song.audio_file:
                    if os.path.exists(song.audio_file.path):
                        try:
                            os.remove(song.audio_file.path)
                        except OSError:
                            pass  # Continue even if file deletion fails
                            
                if song.lyrics_file:
                    if os.path.exists(song.lyrics_file.path):
                        try:
                            os.remove(song.lyrics_file.path)
                        except OSError:
                            pass  # Continue even if file deletion fails
                
                # Store song title for success message
                song_title = song.title
                
                # Delete the song
                song.delete()
                
                # Send confirmation email using template
                try:
                    from django.template.loader import render_to_string
                    from django.contrib.sites.shortcuts import get_current_site
                    
                    email_context = {
                        'user': request.user,
                        'song_title': song_title,
                        'song_ai_tool': song.ai_tool_used if hasattr(song, 'ai_tool_used') else None,
                        'site_name': 'AI Song Contest',
                        'site_url': f'https://{get_current_site(request).domain}',
                        'admin_email': getattr(settings, 'ADMIN_EMAIL', 'support@contest.spado.org.pk')
                    }
                    
                    html_message = render_to_string('email_verification/song_deletion_confirmed.html', email_context)
                    plain_message = f'Your song "{song_title}" has been permanently deleted from the platform.'
                    
                    send_mail(
                        subject=f'Song Deleted - {song_title}',
                        message=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[request.user.email],
                        html_message=html_message
                    )
                except Exception as e:
                    # Log the error but don't fail the deletion
                    print(f"Failed to send deletion confirmation email: {e}")
                
                messages.success(request, f'Song "{song_title}" has been permanently deleted.')
                return redirect('contest:dashboard')
                
            except EmailVerification.DoesNotExist:
                messages.error(request, 'Invalid verification code. Please try again.')
    else:
        from email_verification.forms import EmailVerificationForm
        form = EmailVerificationForm()
    
    # Check again if song exists before rendering template
    if not Song.objects.filter(id=song_id, user=request.user).exists():
        messages.error(request, 'The song you are trying to delete no longer exists.')
        return redirect('contest:dashboard')
    
    context = {
        'form': form,
        'song': song,
    }
    return render(request, 'contest/delete_song_verify.html', context)
