from rest_framework import serializers
from django.conf import settings
from django.db.models import Avg,Sum
from .models import Products,Customers,OrderItems,Orders,Size,ProductImage,ProductVariations,Tag,Categories,ProductReviews,Contact,Comment,Blog,Team,Banner,Slider,BlogSideBar
from django.utils import timezone

# Create your serializers here.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['username', 'email', 'password','first_name','last_name','country','street_address','city','state','zip','phone']
        
    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Username should only contain alphabets and numbers.")
        return value

    def validate_password(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Password should only contain alphabets and numbers.")
        return value

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name should only contain alphabets.")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name should only contain alphabets.")
        return value
    
    def validate_country(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Country should only contain alphabets.")
        return value
    
    def validate_city(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("City should only contain alphabets.")
        return value
    
    def validate_state(self, value):
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError("State should only contain alphabets.")
        return value
    
    def validate_street_address(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Street Address should only contain alphabets and numbers.")
        return value
    
    def validate_phone(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("Phone number should only contain digits.")
        return value
    
    def validate_zip(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("Zip number should only contain digits.")
        return value


# Category Serializer   
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


# Size Serializer
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('name', 'stock')


# Tag Serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


# Product Image Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('url',)


# Product Review Serializer
class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviews
        fields = ('rating',)


# Product Variation Serializer
class ProductVariationSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='attribute.attribute_name')
    image = serializers.ImageField(source='image_url')
    size = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariations
        fields = ('color','image', 'size')

    def get_size(self, obj):
        sizes = Size.objects.filter(variation=obj)
        return SizeSerializer(sizes, many=True).data


# Product Serializer 
class ProductSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(source='product_id')
    name=serializers.CharField(source='product_name')
    offerEnd=serializers.DateTimeField(source='offer_end')
    shortDescription=serializers.CharField(source='short_description')
    fullDescription=serializers.CharField(source='full_description')
    variation=ProductVariationSerializer(source='variations',many=True)  
    category = serializers.StringRelatedField(many=True)
    tag = serializers.StringRelatedField(source='tags',many=True)
    image = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    saleCount = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ('id', 'sku', 'name', 'price', 'discount', 'offerEnd', 'new', 'rating', 'saleCount', 'category', 'tag', 'variation', 'image', 'shortDescription', 'fullDescription')
    
    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            base_url = request.build_absolute_uri(settings.MEDIA_URL)
            return [f"{base_url}{str(image.url)}" for image in obj.image_url.all()]
        return []
    
    def get_rating(self, obj):
        average = ProductReviews.objects.filter(product=obj).aggregate(Avg('rating'))['rating__avg']
        return round(average) if average is not None else None
    
    def get_saleCount(self, obj):
        # Calculate the total quantity sold for the product
        saleCount = OrderItems.objects.filter(product_variation__product=obj).aggregate(Sum('quantity'))['quantity__sum']
        return saleCount if saleCount is not None else 0


#Order Items Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields =  ['product_variation', 'size_name', 'quantity']


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Orders
        fields = ['customer','order_items']


# Contact us Serializer
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate_name(self, value):
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError("Name should only contain alphabets and Space.")
        return value
    

# Blog Serializer
class BlogSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name', read_only=True)
    class Meta:
        model = Blog
        fields='__all__'


# Team Serializer
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Team
        fields='__all__'


# Team Serializer
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banner
        fields='__all__'


# Create Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviews
        fields = ('name', 'email', 'rating', 'review_text', 'rating')


# Create Slider Serializer
class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Slider
        fields = '__all__'


# Create BlogSidebar Serializer
class BlogSidebarSerializer(serializers.ModelSerializer):
    class Meta:
        model= BlogSideBar
        fields = '__all__'



        