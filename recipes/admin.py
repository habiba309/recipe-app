from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Recipe, Ingredient, Favorite


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display  = ['name', 'course', 'created_at']
    list_filter   = ['course']
    search_fields = ['name']
    inlines       = [IngredientInline]


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets    = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


admin.site.register(Favorite)
