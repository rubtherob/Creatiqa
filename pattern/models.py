from django.db import models

# Create your models here.
class Pattern(models.Model):
    group_patterns = (('INST', 'Instagram'), ('VK', 'Vkontakte'), ('FCBK', 'Facebook'))
    group = models.CharField(choices= group_patterns, max_length= 10)
    img = models.ImageField(upload_to='pattern', height_field=2000, width_field=2000)