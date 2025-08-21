from django.urls import path
from . import views

app_name = 'contest'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_song, name='upload_song'),
    path('winners/', views.winners_page, name='winners'),
    path('browse/', views.browse_songs, name='browse_songs'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('song/<int:song_id>/', views.song_detail, name='song_detail'),
    path('song/<int:song_id>/vote/', views.vote_song, name='vote_song'),
    path('song/<int:song_id>/comment/', views.add_comment, name='add_comment'),
    path('song/<int:song_id>/edit/', views.edit_song, name='edit_song'),
    path('song/<int:song_id>/delete/', views.delete_song_request, name='delete_song_request'),
    path('song/<int:song_id>/delete/verify/', views.delete_song_verify, name='delete_song_verify'),
    
    # Admin URLs
    path('manage/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/users/', views.admin_users, name='admin_users'),
    path('manage/users/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('manage/songs/', views.admin_songs, name='admin_songs'),
    path('manage/winners/', views.admin_winners, name='admin_winners'),
    path('manage/deadlines/', views.admin_deadlines, name='admin_deadlines'),
]
