from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,OrderSerializer,ProductSerializer,ContactSerializer,CommentSerializer,BlogSerializer,TeamSerializer,BannerSerializer,ReviewSerializer,SliderSerializer,BlogSidebarSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate,login
from api.models import Products,Customers,Orders, OrderItems, ProductVariations,Size,Blog,Team,Banner,Comment,ProductReviews,Slider,BlogSideBar
import re
from django.utils import timezone

# Create your views here.

# Register User View
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user = Customers.objects.create_user(
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                country=user_data['country'],
                street_address=user_data['street_address'],
                city=user_data['city'],
                state=user_data['state'],
                zip=user_data['zip'],
                phone=user_data['phone']
            )
            return Response({
                'status':200,
                'message':'User Registered Successfully',
            })
        return Response({
            'status':400,
            'message':'Something went wrong',
            'data':serializer.errors
        })


# User Login View
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email=request.data.get('email')
        password=request.data.get('password')

        user=authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            token,created=Token.objects.get_or_create(user=user)
            return Response({
                'status':200,
                'message':'token created',
                'user_id':user.customer_id,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'email':user.email,
                'token':token.key
            })
        return Response({'message':'Invalid credentials'})


# Access Profile View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user=request.user
        profile={
            "user_id":user.customer_id,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email,
            "country":user.country,
            "street_address":user.street_address,
            "city":user.city,
            "state":user.state,
            "zip":user.zip,
            "phone":user.phone,
        }
        return Response(profile)
    

# Update Profile View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UpdateProfileView(APIView):

    def validate_alphabetic(self, value):
        return re.match(r'^[a-zA-Z]+$', value)
     
    def put(self, request, *args, **kwargs):
        user=request.user
        data=request.data

        first_name=data.get('first_name',user.first_name)
        last_name=data.get('last_name',user.last_name)

        if not self.validate_alphabetic(first_name):
            return Response({
                "status": 400,
                "message": "Invalid first name format. Only alphabetic characters are allowed."
            })
        
        if not self.validate_alphabetic(last_name):
            return Response({
                "status": 400,
                "message": "Invalid last name format. Only alphabetic characters are allowed."
            })

        user.first_name=first_name
        user.last_name=last_name
        user.save()

        return Response({
            "status":200,
            "message":"profile updated successfully",
            'user_id':user.customer_id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
        })


# Change Password View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ChangePasswordView(APIView):

    def validate_password(self, value):
        return re.match(r'^[a-zA-Z0-9]+$', value)
    
    def put(self, request, *args, **kwargs):
        user=request.user
        data=request.data

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not check_password(old_password, user.password):
            return Response({"message": "Old password is incorrect"}, status=400)
        
        if not self.validate_password(new_password):
            return Response({
                "status":400,
                "message": "Invalid password format, It will only take alphabets and numbers."
            })

        user.set_password(new_password)
        user.save()

        return Response({
            "status":200,
            "message": "Password changed successfully",
        })
    

# Logout View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response({"message": "Logout successful"})


#Create Products List View  
class ProductListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


#Product Detail View
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_id'


# #Create Order View
class CreateOrder(APIView):
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.validated_data['customer']
            order_items_data = serializer.validated_data['order_items']
            order = Orders(customer=customer)
            order.save()

            total_amount = 0
            for item_data in order_items_data:
                product_variation = item_data['product_variation']
                size_name = item_data['size_name']
                quantity = item_data['quantity']

                try:
                    product_variation_obj = ProductVariations.objects.get(pk=product_variation.variation_id)
                except ProductVariations.DoesNotExist:
                    return Response({
                        "status": 400,
                        "message": "Product variation not found"
                    })

                try:
                    size = Size.objects.get(product=product_variation_obj.product, variation=product_variation_obj,name=size_name)
                except Size.DoesNotExist:
                    return Response({
                        "status": 400,
                        "message": f"Size {size_name} not found for the product variation"
                    })

                if size.stock < quantity:
                    return Response({
                        "status": 400,
                        "message": f"Insufficient stock for size {size_name}"
                    })

                item_price = product_variation_obj.product.price * quantity

                order_item = OrderItems(
                    order=order,
                    product_variation=product_variation_obj,
                    size_name=size_name,
                    quantity=quantity,
                    item_price=item_price
                )
                order_item.save()

                size.stock -= quantity
                size.save()

                total_amount += item_price

            order.total_amount = total_amount
            order.save()

            return Response({
                "status": 200,
                "message": "Order created successfully"
            })
        return Response({
            "status": 400,
            "error": serializer.errors,
            "message": "Something went wrong"
        })
    

# Retrieve Order View
class RetrieveOrders(APIView):
    def get(self, request, format=None):
        customer_id = request.query_params.get('customer_id')

        if not customer_id:
            return Response({
                "status": 400,
                "message": "Please provide a customer_id query parameter."
            })

        try:
            orders = Orders.objects.filter(customer__customer_id=customer_id)
            serialized_orders = []
            for order in orders:
                serialized_orders.append({
                    "order_id": order.order_id,
                    "order_date": order.order_date,
                    "total_amount": float(order.total_amount),
                    "order_status": order.order_status,
                })

            return Response({
                "status":200,
                "Orders":serialized_orders,
                })

        except Orders.DoesNotExist:
            return Response({
                "status":400,
                "message": f"No orders found for customer with customer_id {customer_id}."  
            })


# Contact us View
class ContactCreateView(APIView):
    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status':200,
                'data':serializer.data
            })
        return Response({
            'status':400,
            'error':serializer.errors
        })
    

# Update Billing View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UpdateBillingView(APIView):

    def validate_alphabetic(self, value):
        return re.match(r'^[a-zA-Z]+$', value)
    
    def validate_alphabetic_with_spaces(self, value):
        return re.match(r'^[a-zA-Z\s]+$', value)
    
    def validate_alphanumeric_with_spaces(self, value):
        return re.match(r'^[a-zA-z0-9\s]+$',value)
    
    def put(self, request, *args, **kwargs):
        user=request.user
        data=request.data

        first_name=data.get('first_name',user.first_name)
        last_name=data.get('last_name',user.last_name)
        country=data.get('country',user.country)
        street_address=data.get('street_address',user.street_address)
        city=data.get('city',user.city)
        state=data.get('state',user.state)
        zip=data.get('zip',user.zip)
        phone=data.get('phone',user.phone)

        if not self.validate_alphabetic(first_name):
            return Response({
                "status": 400,
                "message": "Invalid first name format. Only alphabetic characters are allowed."
            })
        
        if not self.validate_alphabetic(last_name):
            return Response({
                "status": 400,
                "message": "Invalid last name format. Only alphabetic characters are allowed."
            })
        
        if not self.validate_alphabetic_with_spaces(country):
            return Response({
                "status": 400,
                "message": "Invalid Country format. Only alphabetic characters are allowed."
            })
        
        if not self.validate_alphabetic_with_spaces(city):
            return Response({
                "status": 400,
                "message": "Invalid City format. Only alphabetic characters are allowed."
            })
        
        if not self.validate_alphabetic_with_spaces(state):
            return Response({
                "status": 400,
                "message": "Invalid State format. Only alphabetic characters are allowed."
            })
        
        if not self.validate_alphanumeric_with_spaces(street_address):
            return Response({
                "status": 400,
                "message": "Invalid Street Address format. Only alphabetic characters are allowed."
            })

        user.first_name=first_name
        user.last_name=last_name
        user.country=country
        user.city=city
        user.state=state
        user.street_address=street_address
        user.zip=zip
        user.phone=phone
        user.save()

        return Response({
            "status":200,
            "message":"profile updated successfully",
            'user_id':user.customer_id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'country':user.country,
            'city':user.city,
            'state':user.state,
            'street_address':user.street_address,
            'zip':user.zip,
            'phone':user.phone,
            'email':user.email,
        })


# Comment View
class Commentview(APIView):
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

# Comment Detail
class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Blog View
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


# Blog Detail
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'blog_id' 


# Team View
class TeamView(generics.ListAPIView):
    queryset=Team.objects.all()
    serializer_class=TeamSerializer


# Banner View
class BannerView(generics.ListAPIView):
    queryset=Banner.objects.all()
    serializer_class=BannerSerializer


# Product Review View
class ReviewCreateView(generics.CreateAPIView):
    queryset = ProductReviews.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id') or self.request.data.get('product_id')
        if product_id:
            try:
                product = Products.objects.get(product_id=product_id)
                serializer.save(product=product)
            except Products.DoesNotExist:
                return Response({
                    "status":400,
                    "message": "Product not found."
                })
        else:
            return Response({
                "status":404,
                "message": "Product ID is required."
            })
        

#Retrieve Product Review
class ReviewRetrieveView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        try:
            product = Products.objects.get(product_id=product_id)
            return ProductReviews.objects.filter(product=product)
        except Products.DoesNotExist:
            return Response({
                "status":400,
                "message": "Product not found."
            })
        

# Slider View
class SliderView(generics.ListAPIView):
    queryset=Slider.objects.all()
    serializer_class=SliderSerializer


# BlogSidebar View
class BlogSidebarView(generics.ListAPIView):
    queryset=BlogSideBar.objects.all()
    serializer_class=BlogSidebarSerializer