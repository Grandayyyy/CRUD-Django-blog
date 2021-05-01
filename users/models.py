from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_resized import ResizedImageField
from multiselectfield import MultiSelectField


class Profile(models.Model):

    gender_choices = [('M', 'MALE'), ('F', 'FEMALE'), ('O', 'OTHER')]
    country_choices = [('india', 'India'), ('america', 'America'), ('china', 'China')]
    intrests_choices = [('c', 'Coding'), ('r', 'Reading'), ('b', 'Binging'), ('g', 'Gaming')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ResizedImageField(size=[300, 300], default='default_profile.jpg', upload_to='profile_pics')
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')
    country = models.CharField(max_length=7, choices=country_choices, default='india')
    float = models.FloatField(null=True, blank=True, default=None)
    intrests = MultiSelectField(choices=intrests_choices, max_choices=4)
    boolean = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
