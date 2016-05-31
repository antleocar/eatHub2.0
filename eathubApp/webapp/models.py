from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


# Validators

def validate_savour(savour):
    if savour <= -1 or savour >= 100:
        raise ValidationError("Value is not in range 0 to 99")


class Tastes(models.Model):

   salty = models.IntegerField(validators=[validate_savour])
   sour = models.IntegerField(validators=[validate_savour])
   bitter = models.IntegerField(validators=[validate_savour])
   sweet = models.IntegerField(validators=[validate_savour])
   spicy = models.IntegerField(validators=[validate_savour])
