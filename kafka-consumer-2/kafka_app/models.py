from django.db import models

# Create your models here.
class Device(models.Model):
    sn = models.CharField(max_length=100) 
    description = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.sn