from django.db import models

class RandomCity(models.Model):
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.city
    
    class Meta:
        verbose_name_plural = 'cities'
