from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey
from datetime import datetime


# Validators


def validate_savour(savour):
    if savour <= -1 or savour >= 100:
        raise ValidationError("Value is not in range 0 to 99")


def validate_tags(tags):
    if len(tags) > 10:
        raise ValidationError("Max number of tags is 10")


def validate_past_date(date):
    now = datetime.now()
    if now > date:
        raise ValidationError(u'date cannot be future')


def validate_gender(gender):
    if not (gender == "u" or gender == "m" or gender == "f"):
        raise ValidationError(u'%s is not a valid gender' % gender)


def validate_difficult(difficult):
    if difficult <= 0 or difficult >= 4:
        raise ValidationError("Difficult must be in range 1 to 3")


class Cook(models.Model):
    display_name = models.CharField(max_length=50, blank=False)
    modification_date = models.BigIntegerField(null=True)
    main_language = models.CharField(max_length=50, validators=["""validate_main_language"""])
    avatar = models.ImageField(upload_to='avatars/', null=True)
    website = models.URLField(null=True)
    gender = models.CharField(max_length=1, validators=[validate_gender], null=True)
    birth_date = models.DateField(null=True)
    location = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(User, related_name="cook", unique=True)
    karma = models.IntegerField(default=6)
    username = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return str(self.display_name)

    def get_recipes(self):
        return Recipe.objects.filter(author=self.user)


class Recipe(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    main_image = models.ImageField(upload_to="images/recipe/", null=False)
    modification_date = models.DateTimeField(auto_now_add=True, null=True)
    ingredients = models.CharField(blank=False, max_length=200)
    serves = models.CharField(max_length=50, blank=False)
    language = models.CharField(max_length=50, blank=False)
    temporality = models.CharField(null=True, max_length=50)
    nationality = models.CharField(max_length=50, null=True)
    special_conditions = models.CharField(null=True, max_length=100)
    notes = models.TextField(null=True)
    difficult = models.IntegerField(null=True, validators=[validate_difficult])
    food_type = models.CharField(max_length=50, null=True)
    tags = models.CharField(null=True, validators=[validate_tags], max_length=100)
    is_published = models.BooleanField()
    parent = ForeignKey('self', null=True, blank=True)
    cook = models.ForeignKey(Cook, related_name='recipes_cook', default='')

    def __str__(self):
        return self.title

    def get_child_recipes(self):
        return Recipe.objects.filter(parent=self.id)


class Tastes(models.Model):

   salty = models.IntegerField(validators=[validate_savour])
   sour = models.IntegerField(validators=[validate_savour])
   bitter = models.IntegerField(validators=[validate_savour])
   sweet = models.IntegerField(validators=[validate_savour])
   spicy = models.IntegerField(validators=[validate_savour])
   recipe = models.ForeignKey(Recipe, related_name='tastes_recipe', default='')

   def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.salty, self.sour, self.bitter,
                                           self.sweet, self.spicy)


class Step(models.Model):
    text = models.TextField(blank=False)
    image = models.ImageField(upload_to="images/recipe/", null=True)
    recipe = models.ForeignKey(Recipe, related_name='steps_recipe', default='')


class Picture(models.Model):
    image = models.ImageField(upload_to="images/", null=False)
    step = models.ForeignKey(Step, related_name='pictures_step', default='')


class Comment(models.Model):
    text = models.TextField(blank=False)
    create_date = models.BigIntegerField()
    user_own = ForeignKey(User, related_name='user', default='', null=False)
    is_banned = models.BooleanField(default=False)
    recipe = models.ForeignKey(Recipe, related_name='comments_recipe', default='')

    def __str__(self):
        return self.text


class Vote(models.Model):
    date = models.DateField(validators=[validate_past_date])
    user = ForeignKey(User)
    recipe = models.ForeignKey(Recipe, related_name='votes_recipe', default='')

    def __eq__(self, other):
        return self.user is other.user and self.date == other.date


class Savour(models.Model):
    salty = models.IntegerField(validators=[validate_savour])
    sour = models.IntegerField(validators=[validate_savour])
    bitter = models.IntegerField(validators=[validate_savour])
    sweet = models.IntegerField(validators=[validate_savour])
    spicy = models.IntegerField(validators=[validate_savour])
    recipe = models.ForeignKey(Recipe, related_name='savours_recipe', default='')

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.salty, self.sour, self.bitter, self.sweet, self.spicy)


