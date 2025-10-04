from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MoviePetition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_petitions')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def total_votes(self):
        return self.votes.count()
    
    def user_voted(self, user):
        return self.votes.filter(user=user).exists()
    
class PetitionVote(models.Model):
    petition = models.ForeignKey(MoviePetition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['petition', 'user']

    def __str__(self):
        return f"{self.user.username} voted for {self.petition.title}"