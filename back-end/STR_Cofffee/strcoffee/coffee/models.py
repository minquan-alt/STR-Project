from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    host        = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    name        = models.CharField(max_length=200)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True)
    description = models.TextField(null=True, blank=True) # phần mô tả null, blank này thể hiện chức năng để trống
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)
    price       = models.DecimalField(max_digits=5, decimal_places=3, default=0.0)
    image       = models.CharField(max_length=3000, default='default_image.png')
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name
    
class Remarkable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
