from django.db import models

# Create your models here.

class TodoList(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='todo_list_owner', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']
    

class Todo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(blank=True, default=False)
    title = models.CharField(max_length=100, blank=True, default='')
    todo_list = models.ForeignKey(TodoList, related_name='todos', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='todo_owner', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']


