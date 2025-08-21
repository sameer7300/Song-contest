from django.contrib import admin
from django.contrib import messages
from .models import Song, Vote, Comment, Winner, Tag, Deadline
from email_verification.services import EmailVerificationService

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    search_fields = ['name']

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'language', 'genre', 'average_rating', 'vote_count', 'view_count', 'is_winner', 'is_featured', 'submitted_at']
    list_filter = ['language', 'genre', 'is_winner', 'is_featured', 'submitted_at']
    search_fields = ['title', 'user__username', 'user__email']
    readonly_fields = ['submitted_at', 'view_count', 'vote_count', 'average_rating']
    filter_horizontal = ['tags']
    actions = ['mark_as_winner', 'mark_as_featured']
    
    def mark_as_winner(self, request, queryset):
        """Mark selected songs as winners and send notifications"""
        count = 0
        for song in queryset:
            winner, created = Winner.objects.get_or_create(song=song)
            if created:
                count += 1
                # Email will be sent automatically via signal
        
        if count > 0:
            self.message_user(request, f'{count} song(s) marked as winners. Email notifications sent.', messages.SUCCESS)
        else:
            self.message_user(request, 'No new winners created (songs may already be winners).', messages.INFO)
    
    def mark_as_featured(self, request, queryset):
        """Mark selected songs as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} song(s) marked as featured.', messages.SUCCESS)
    
    mark_as_winner.short_description = "Mark selected songs as winners"
    mark_as_featured.short_description = "Mark selected songs as featured"

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'song', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'song__title']
    readonly_fields = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'song', 'content_preview', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__username', 'song__title', 'content']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content Preview"

@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ['song', 'selected_at', 'featured_until', 'prize_amount']
    list_filter = ['selected_at', 'featured_until']
    search_fields = ['song__title', 'song__user__username']
    readonly_fields = ['selected_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('song__user')

@admin.register(Deadline)
class DeadlineAdmin(admin.ModelAdmin):
    list_display = ('status', 'deadline_date', 'is_active_display', 'created_at')
    search_fields = ('description',)
    list_filter = ('status', 'deadline_date', 'created_at')
    readonly_fields = ('is_active_display', 'time_remaining_display')
    fields = ('status', 'deadline_date', 'description', 'is_active_display', 'time_remaining_display')

    def is_active_display(self, obj):
        return "✅ Active" if obj.is_active else "❌ Expired"
    is_active_display.short_description = 'Status'
    
    def time_remaining_display(self, obj):
        if obj.time_remaining:
            days = obj.time_remaining.days
            hours, remainder = divmod(obj.time_remaining.seconds, 3600)
            return f"{days} days, {hours} hours"
        return "Expired"
    time_remaining_display.short_description = 'Time Remaining'
