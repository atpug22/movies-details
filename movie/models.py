from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movies(models.Model):
    title =models.CharField(max_length=100)
    director=models.CharField(max_length=100)
    release_date =models.DateField()
    actors = models.TextField()
    description=models.TextField()
    movie_url = models.URLField()

    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    movie = models.ForeignKey(Movies,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user.get_full_name)