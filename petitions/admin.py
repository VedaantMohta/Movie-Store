from django.contrib import admin
from .models import MoviePetition, PetitionVote
# Register your models here.

@admin.register(MoviePetition)
class MoviePetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_active', 'total_votes')
    list_filter = ('is_active', 'created_at', 'created_by')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('created_at',)

@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ('petition', 'user', 'voted_at')
    list_filter = ('voted_at',)
    search_fields = ('petition__title', 'user__username')
