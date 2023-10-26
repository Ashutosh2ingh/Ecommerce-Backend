from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from api.views import RegisterView, LoginView, UserProfileView, UpdateProfileView, ChangePasswordView, LogoutView,ProductListView,ProductDetailView,CreateOrder,RetrieveOrders,ContactCreateView,UpdateBillingView,Commentview,BlogListView,BlogDetailView,TeamView,BannerView,CommentListView,ReviewCreateView,SliderView,ReviewRetrieveView,BlogSidebarView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/profile/update/', UpdateProfileView.as_view(), name='update-user-profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/productslist/', ProductListView.as_view(), name='product-list'),
    path('api/productdetail/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/orders/', CreateOrder.as_view(), name='create_order'),
    path('api/retrieveorder/', RetrieveOrders.as_view(), name='customer-orders'),
    path('api/contact/', ContactCreateView.as_view(), name='contact-create'),
    path('api/billing/update/', UpdateBillingView.as_view(), name='update-billing-profile'),
    path('api/comment/', Commentview.as_view(), name='Create-Comment'),
    path('api/commentlist/', CommentListView.as_view(), name='comment-list'),
    path('api/blogs/', BlogListView.as_view(), name='blog-list'),
    path('api/blogsdetail/<int:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('api/teams/', TeamView.as_view(), name='team-list'),
    path('api/banner/', BannerView.as_view(), name='banner'),
    path('api/products/<int:product_id>/createreview/', ReviewCreateView.as_view(), name='create-review'),
    path('api/products/<int:product_id>/retrievereviews/', ReviewRetrieveView.as_view(), name='retrieve-reviews'),
    path('api/slider/', SliderView.as_view(), name='slider'),
    path('api/blogsidebar/', BlogSidebarView.as_view(), name='blogsidebar'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)