from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    photo=models.ImageField(upload_to='note_photos/' ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.owner.username}] {self.title}"


class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks',
    )
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='bookmarked_by',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'note')

    def __str__(self):
        return f"{self.user.username} ★ '{self.note.title}'"