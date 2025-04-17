from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Recipe, Rating, Category
from .forms import RecipeForm, IngredientFormSet, CommentForm, RatingForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib import messages

def recipe_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    recipes = Recipe.objects.all()
    if query:
        recipes = recipes.filter(Q(title__icontains=query))
    if category_id:
        recipes = recipes.filter(categories__id=category_id)
    paginator = Paginator(recipes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'recipes/recipe_list.html', {'page_obj': page_obj, 'categories': categories})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST, instance=Recipe())
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            formset.instance = recipe
            formset.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
        formset = IngredientFormSet(instance=Recipe())
    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset})

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.user != recipe.author:
        return redirect('recipe_detail', pk=recipe.pk)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSet(request.POST, instance=recipe)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('recipe_detail', pk=recipe.pk)
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSet(instance=recipe)
    
    return render(request, 'recipes/recipe_form.html', {'form': form, 'formset': formset, 'recipe': recipe})

def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Проверяем, авторизован ли пользователь
    if not request.user.is_authenticated:
        messages.warning(request, 'Для комментария необходимо авторизоваться.')  # Добавляем сообщение
        return redirect('recipe_detail', pk=recipe.pk)  # Перенаправляем на страницу рецепта

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user  # Авторизованный пользователь
            comment.save()
            messages.success(request, 'Ваш комментарий успешно добавлен!')  # Сообщение об успехе
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = CommentForm()
    
    return render(request, 'recipes/add_comment.html', {'form': form, 'recipe': recipe})

def add_rating(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            session_key = request.session.session_key  # Используем сессию для неавторизованных пользователей

            # Проверяем, не поставил ли уже пользователь оценку
            if user:
                rating, created = Rating.objects.get_or_create(
                    recipe=recipe,
                    user=user,
                    defaults={'value': form.cleaned_data['value']}
                )
            else:
                rating, created = Rating.objects.get_or_create(
                    recipe=recipe,
                    session_key=session_key,  # Используем session_key для неавторизованных пользователей
                    defaults={'value': form.cleaned_data['value']}
                )

            if not created:
                rating.value = form.cleaned_data['value']
                rating.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RatingForm()
    return render(request, 'recipes/add_rating.html', {'form': form, 'recipe': recipe})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')
    else:
        form = SignUpForm()
    return render(request, 'recipes/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('recipe_list')
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('recipe_list')