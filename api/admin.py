from django.contrib import admin
from .models import Categories, Products, ProductAttributes, ProductVariations, Customers, PaymentMethods, Orders, OrderItems, Shipments, ProductReviews, Payments,Tag,ProductImage,Size,Contact,Blog,Comment,Team,Banner,Slider,BlogSideBar

# Register your models here.

# Register Categories
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name')


# Register product
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'sku', 'product_name', 'price')


# Register Product Attribute
@admin.register(ProductAttributes)
class ProductAttributesAdmin(admin.ModelAdmin):
    list_display = ('attribute_id', 'product', 'attribute_name')


# Register Product Variations
@admin.register(ProductVariations)
class ProductVariationsAdmin(admin.ModelAdmin):
    list_display = ('variation_id', 'product', 'attribute', 'variation_value')


# Register Customer 
@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'email')


# Register Payment Methods
@admin.register(PaymentMethods)
class PaymentMethodsAdmin(admin.ModelAdmin):
    list_display = ('payment_method_id', 'customer', 'card_number', 'card_expiry', 'card_holder_name')


# Register Orders
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'order_date', 'total_amount', 'order_status')


# Register Order Items
@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order_item_id', 'order', 'product_variation', 'quantity', 'item_price')


# Register Shipments
@admin.register(Shipments)
class ShipmentsAdmin(admin.ModelAdmin):
    list_display = ('shipment_id', 'order', 'shipping_date', 'estimated_arrival_date', 'shipping_status')


# Register Product Reviews
@admin.register(ProductReviews)
class ProductReviewsAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'product', 'name', 'email', 'rating', 'review_date')


# Register Payments
@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin): 
    list_display = ('payment_id', 'order', 'payment_method', 'payment_date', 'payment_amount')


# Register Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name')


# Register Product Image
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image_id','name','url')


# Register Size
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('product','variation','name','stock')


# Register Contact us 
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=('contact_id','name','email')


# Register Blog 
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=('blog_id','title','author','published_date')


# Register Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('comment_id','name','message','date')


# Register Team
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display=('id','name','position')


# Register Banner
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display=('id','title','price')


# Register Slider
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subtitle', 'image', 'url')


# Register BlogSideBar
@admin.register(BlogSideBar)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'image', 'link')