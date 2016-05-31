from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey


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

   def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.salty, self.sour, self.bitter,
                                           self.sweet, self.spicy)


class Comment(models.Model):
    text = models.TextField(blank=False)
    create_date = models.BigIntegerField()
    user_own = ForeignKey(User,related_name='user', default='', null=False)
    is_banned = models.BooleanField(default=False)
    #id_recipe = models.ForeignKey(Recipe, related_name='comments', default='')

    def __str__(self):
        return self.text


class Step(models.Model):
    text = models.TextField(blank=False)
    image = models.ImageField(upload_to="images/recipe/", null=True)
    #recipe = models.ForeignKey(Recipe, related_name='recipes',default='')



class Picture(models.Model):
    image = models.ImageField(upload_to="images/", null=False)


class Following(models.Model):
    display_name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(User)

    @staticmethod
    def create_following(user):
        return Following(display_name=user.profile.get().display_name, username=user.username, user=user)