from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import CustomUser, Recipe, Ingredient, Favorite
from .forms import SignUpForm, SignInForm, RecipeForm
from .decorators import admin_required

FILTER_CHOICES = [
    ('all',        'All'),
    ('appetizers', 'Appetizers'),
    ('main course','Main Course'),
    ('dessert',    'Dessert'),
]

# ─────────────────────────── Auth ────────────────────────────

def signin_view(request):
    if request.user.is_authenticated:
        return redirect('admin_home' if request.user.role == 'admin' else 'home')

    form = SignInForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email    = form.cleaned_data['email']
        password = form.cleaned_data['password']
        try:
            user_obj = CustomUser.objects.get(email=email)
            user     = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_home' if user.role == 'admin' else 'home')
            else:
                messages.error(request, 'Invalid email or password.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'auth/signin.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = CustomUser(
            username=form.cleaned_data['username'],
            email   =form.cleaned_data['email'],
            role    =form.cleaned_data['role'],
        )
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.username}! Your account has been created.')
        return redirect('admin_home' if user.role == 'admin' else 'home')

    return render(request, 'auth/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('signin')


# ─────────────────────────── User pages ──────────────────────

@login_required(login_url='signin')
def home_view(request):
    recipes = Recipe.objects.prefetch_related('ingredients').order_by('-created_at')
    return render(request, 'home.html', {'recipes': recipes})


@login_required(login_url='signin')
def recipes_list_view(request):
    recipes       = Recipe.objects.prefetch_related('ingredients').all()
    course_filter = request.GET.get('course', 'all')
    search_query  = request.GET.get('search', '').strip()

    if course_filter and course_filter != 'all':
        recipes = recipes.filter(course__iexact=course_filter)

    if search_query:
        recipes = recipes.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__name__icontains=search_query)
        ).distinct()

    fav_ids = set(
        Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
    )

    return render(request, 'recipes/list.html', {
        'recipes':        recipes,
        'course_filter':  course_filter,
        'search_query':   search_query,
        'fav_ids':        fav_ids,
        'filter_choices': FILTER_CHOICES,
    })


@login_required(login_url='signin')
def recipe_detail_view(request, pk):
    recipe      = get_object_or_404(Recipe.objects.prefetch_related('ingredients'), pk=pk)
    is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    return render(request, 'recipes/detail.html', {
        'recipe':      recipe,
        'is_favorite': is_favorite,
    })


@login_required(login_url='signin')
def toggle_favorite_view(request, pk):
    if request.method != 'POST':
        return redirect('recipes_list')
    recipe       = get_object_or_404(Recipe, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        fav.delete()
        messages.info(request, f'"{recipe.name}" removed from favorites.')
    else:
        messages.success(request, f'"{recipe.name}" added to favorites!')
    return redirect(request.POST.get('next') or 'recipes_list')


@login_required(login_url='signin')
def favorites_view(request):
    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related('recipe')
        .prefetch_related('recipe__ingredients')
        .order_by('-created_at')
    )
    return render(request, 'recipes/favorites.html', {'favorites': favorites})




@login_required(login_url='signin')
@admin_required
def admin_home_view(request):
    recipes = Recipe.objects.prefetch_related('ingredients').order_by('-created_at')
    return render(request, 'admin_home.html', {'recipes': recipes})


@login_required(login_url='signin')
@admin_required
def dashboard_view(request):
    recipes = Recipe.objects.prefetch_related('ingredients').order_by('-created_at')
    return render(request, 'dashboard/index.html', {'recipes': recipes})


def _save_recipe_with_ingredients(request, form):
    """Save recipe and process ingredient_name[] / ingredient_quantity[] lists."""
    recipe = form.save()
    recipe.ingredients.all().delete()
    names = request.POST.getlist('ingredient_name')
    qtys  = request.POST.getlist('ingredient_quantity')
    pairs = [(n.strip(), q.strip()) for n, q in zip(names, qtys) if n.strip()]
    for name, qty in pairs:
        Ingredient.objects.create(recipe=recipe, name=name, quantity=qty)
    return recipe, pairs


@login_required(login_url='signin')
@admin_required
def add_recipe_view(request):
    form = RecipeForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        names = request.POST.getlist('ingredient_name')
        qtys  = request.POST.getlist('ingredient_quantity')
        pairs = [(n.strip(), q.strip()) for n, q in zip(names, qtys) if n.strip()]

        if form.is_valid():
            if not pairs:
                messages.error(request, 'At least one ingredient is required.')
            else:
                recipe, _ = _save_recipe_with_ingredients(request, form)
                messages.success(request, f'Recipe "{recipe.name}" added successfully!')
                return redirect('dashboard')

        ingredients_data = list(zip(names, qtys)) or [('', '')]
        return render(request, 'dashboard/recipe_form.html', {
            'form':             form,
            'title':            'Add Recipe',
            'ingredients_data': ingredients_data,
        })

    return render(request, 'dashboard/recipe_form.html', {
        'form':             form,
        'title':            'Add Recipe',
        'ingredients_data': [('', '')],
    })


@login_required(login_url='signin')
@admin_required
def edit_recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    form   = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)

    if request.method == 'POST':
        names = request.POST.getlist('ingredient_name')
        qtys  = request.POST.getlist('ingredient_quantity')
        pairs = [(n.strip(), q.strip()) for n, q in zip(names, qtys) if n.strip()]

        if form.is_valid():
            if not pairs:
                messages.error(request, 'At least one ingredient is required.')
            else:
                recipe, _ = _save_recipe_with_ingredients(request, form)
                messages.success(request, f'Recipe "{recipe.name}" updated successfully!')
                return redirect('dashboard')

        ingredients_data = list(zip(names, qtys)) or [('', '')]
        return render(request, 'dashboard/recipe_form.html', {
            'form':             form,
            'recipe':           recipe,
            'title':            'Edit Recipe',
            'ingredients_data': ingredients_data,
        })

    ingredients_data = [(i.name, i.quantity) for i in recipe.ingredients.all()] or [('', '')]
    return render(request, 'dashboard/recipe_form.html', {
        'form':             form,
        'recipe':           recipe,
        'title':            'Edit Recipe',
        'ingredients_data': ingredients_data,
    })


@login_required(login_url='signin')
@admin_required
def delete_recipe_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        name = recipe.name
        recipe.delete()
        messages.success(request, f'Recipe "{name}" deleted.')
    return redirect('dashboard')
