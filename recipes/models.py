from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role  = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)

    def is_admin_user(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.username} ({self.role})"


class Recipe(models.Model):
    COURSE_CHOICES = [
        ('appetizers', 'Appetizers'),
        ('main course', 'Main Course'),
        ('dessert', 'Dessert'),
    ]
    name         = models.CharField(max_length=200)
    course       = models.CharField(max_length=20, choices=COURSE_CHOICES)
    description  = models.TextField()
    image        = models.ImageField(upload_to='recipes/')
    instructions = models.TextField(help_text="Enter each step on a new line.")
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def get_instructions_list(self):
        return [line.strip() for line in self.instructions.split('\n') if line.strip()]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    recipe   = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name     = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.quantity})"


class Favorite(models.Model):
    user       = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    recipe     = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} → {self.recipe.name}"
