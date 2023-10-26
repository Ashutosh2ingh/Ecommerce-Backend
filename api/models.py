from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import datetime 
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.

# User Manager Model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# Customer Model
class Customers(AbstractUser):
    username = None 
    customer_id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True) 
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    country = models.CharField(max_length=255,default='')
    street_address=models.CharField(max_length=255,default='')
    city = models.CharField(max_length=255,default='')
    state = models.CharField(max_length=255,default='')
    zip = models.IntegerField(default=None)
    phone = models.IntegerField(default=None)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name


# Categories Model
class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


# Tag Model
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Product Model
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    sku= models.CharField(max_length=255, unique=True, null=True)
    product_name = models.CharField(max_length=255)
    category = models.ManyToManyField(Categories)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    new = models.BooleanField(default=False) 
    offer_end = models.DateTimeField(null=True)
    tags = models.ManyToManyField(Tag)
    short_description = models.TextField(null=True)
    full_description = models.TextField(null=True)
    stock_quantity = models.IntegerField(null=True)

    def __str__(self):
        return self.product_name


# Product Image Model
class ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, null=True, blank=True, on_delete=models.CASCADE, related_name='image_url')
    name = models.CharField(max_length=255)
    url = models.ImageField(upload_to='images/',max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.url)


# Product Attribute Model
class ProductAttributes(models.Model):
    attribute_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    attribute_name = models.CharField(max_length=255)

    def __str__(self):
        return self.attribute_name


# Product Variation Model
class ProductVariations(models.Model):
    variation_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variations')
    attribute = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE)
    variation_value = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to='images/',max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.variation_id)


# Size Model 
class Size(models.Model):
    id=models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    variation = models.ForeignKey(ProductVariations, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=10)
    stock = models.IntegerField()

    def __str__(self):
        return self.name


# Payment Method Model   
class PaymentMethods(models.Model):
    payment_method_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_expiry = models.DateField()
    card_holder_name = models.CharField(max_length=255)


# Order Model
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now, verbose_name="Order Date")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    order_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
        ]
    )

    def __str__(self):
        return str(self.order_id)


# Order Items Model
class OrderItems(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariations, on_delete=models.CASCADE)
    size_name = models.CharField(max_length=10, default=None)
    quantity = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)


# Shipments Model
class Shipments(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    shipping_date = models.DateTimeField()
    estimated_arrival_date = models.DateTimeField()
    shipping_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Shipped', 'Shipped'),
            ('In Transit', 'In Transit'),
            ('Delivered', 'Delivered'),
        ]
    )
    tracking_number = models.CharField(max_length=255)


# Product Reviews Model
class ProductReviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default=None)
    email=models.EmailField(max_length=255, unique=True, null=True)
    rating = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now=True)


# Payments Model
class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)


# Contact us Model
class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name


# Blog Model
class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content=models.TextField()
    discription = RichTextField(null=True)
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField()
    category = models.ForeignKey(Categories, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs/', max_length=255, null=True, blank=True)   


# Comment Model
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    message = models.TextField()
    date = models.DateField(auto_now=True)


# Team Member Model
class Team(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    position=models.CharField(max_length=255)
    image=models.ImageField(upload_to='team_member/',max_length=255,null=True,blank=True)


# Banner Model
class Banner(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    price=models.IntegerField()
    image=models.ImageField(upload_to='banner/',max_length=255, null=True, blank=True)


# Slider Model
class Slider(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image = models.ImageField(upload_to='slider/', max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, default=None)


# Blog Sidebar Model
class BlogSideBar(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blogsidebar/', max_length=255, null=True, blank=True)
    link = models.CharField(max_length=255, default=None)


