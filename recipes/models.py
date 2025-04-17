from django.core.exceptions import PermissionDenied
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    cooking_instructions = models.TextField(
        verbose_name='Процесс приготовления',
        help_text='Подробное описание шагов приготовления',
        blank=True
    )
    preparation_time = models.IntegerField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='recipes')
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        return self.ratings.aggregate(models.Avg('value'))['value__avg'] or 0
    
    def save(self, *args, **kwargs):
        if self.pk:  # Если объект уже существует
            original = Recipe.objects.get(pk=self.pk)
            if self.author != original.author:
                raise PermissionDenied("Вы не можете изменить автора рецепта.")
        super().save(*args, **kwargs)

# ... остальные модели без изменений ...
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author.username}'
    
class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Поле user теперь необязательное
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Поле для хранения session_key
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('recipe', 'user', 'session_key')

    # class Meta:
    #     unique_together = ('recipe', 'user')  

# class Rating(models.Model):
#     recipe = models.ForeignKey(Recipe, related_name='ratings', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

#     class Meta:
#         unique_together = ('recipe', 'user')

#     def __str__(self):
#         return f'Оценка {self.value} от {self.user.username}'