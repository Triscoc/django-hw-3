from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LostTable(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lost_items')
    # The name of the lost item
    name = models.CharField(max_length=50)
    # The location where the item is found
    location = models.CharField(max_length=50)
    # The description of the item (colors, brand, etc..)
    description = models.TextField(blank=True, null=True)
    # A boolean whether the item is returned or not
    is_returned = models.BooleanField(default=False)
    # What time the item is found, defaults to datetime(now)
    found_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.location} - {self.found_date:%Y-%m-%d %H:%M}"
