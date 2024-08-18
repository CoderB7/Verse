from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from account.models import CustomUser
from common.models import BaseModel
from bot.models import TelegramChatInfo


class Blog(BaseModel):
    blog_title = models.CharField(max_length=250)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blogs')

    slug = models.SlugField(max_length=250, blank=True)

    def __str__(self):
        return self.blog_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.blog_title)
        super().save(*args, **kwargs)


class Post(BaseModel):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='posts')
    title = models.CharField(max_length=150)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(auto_now_add=timezone.now)
    chat = models.ForeignKey(TelegramChatInfo, on_delete=models.CASCADE, related_name='posts', null=True, default=None)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})





