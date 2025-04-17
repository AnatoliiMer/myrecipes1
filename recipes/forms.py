from django import forms
from .models import Recipe, Ingredient, Comment, Rating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_instructions', 'preparation_time', 
                 'cooking_time', 'servings', 'categories', 'image']
        labels = {
            'title': 'Название рецепта',
            'description': 'Описание',
            'cooking_instructions': 'Процесс приготовления',
            'preparation_time': 'Время подготовки (мин)',
            'cooking_time': 'Время готовки (мин)',
            'servings': 'Количество порций',
            'categories': 'Категории',
            'image': 'Изображение',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Опишите рецепт...'}),
            'cooking_instructions': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Подробно опишите шаги приготовления...'
            }),
            'preparation_time': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Например, 15'}),
            'cooking_time': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Например, 30'}),
            'servings': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Например, 4'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# ... остальные формы без изменений ...

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']
        labels = {
            'name': 'Название ингредиента',
            'quantity': 'Количество',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Например, мука'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'Например, 200 г'}),
        }

IngredientFormSet = forms.inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, extra=1, can_delete=True
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Текст комментария',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите ваш комментарий...'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        labels = {
            'value': 'Оценка',
        }
        widgets = {
            'value': forms.NumberInput(attrs={'min': 1, 'max': 5, 'placeholder': 'От 1 до 5'}),
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}),
        }