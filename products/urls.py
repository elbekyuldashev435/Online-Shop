from django.urls import path
from .views import CategoryDetailView, OrderProductView, CategoryListView, ProductDetailView, ProductListView, AddReviewView, UpdateReviewView, DeleteReviewView

app_name = 'products'

urlpatterns = [
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # Ensure this name matches
    path('add-review/<int:pk>/', AddReviewView.as_view(), name='add-review'),
    path('update-review/<int:pk>/', UpdateReviewView.as_view(), name='update-review'),
    path('delete-review/<int:pk>/', DeleteReviewView.as_view(), name='delete-review'),
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('category-detail/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('product/<int:pk>/order/', OrderProductView.as_view(), name='product-order'),  # Updated name
]
