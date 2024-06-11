from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import AddReviewForm, OrderForm
from .models import CategoryProducts, Products, Review
from django.db.models import Q
from .filters import ProductFilter
from django.core.paginator import Paginator

class ProductListView(View):
    def get(self, request):
        products = Products.objects.all().order_by('-id')
        categories = CategoryProducts.objects.all()
        search_post = request.GET.get('search')

        product_filter = ProductFilter(request.GET, queryset=products)
        products = product_filter.qs

        if search_post:
            products = products.filter(
                Q(name__icontains=search_post) |
                Q(description__icontains=search_post) |
                Q(price__icontains=search_post) |
                Q(category__name__icontains=search_post)
            )
            if not products.exists():
                messages.warning(request, 'No products found.')

        paginator = Paginator(products, 8)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'categories': categories,
            'filter': product_filter,
        }
        return render(request, 'product/product_list.html', context=context)

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        reviews = Review.objects.filter(product=product).order_by('-id')
        context = {
            'product': product,
            'reviews': reviews,
            'current_user': request.user,
        }
        return render(request, 'product/product_detail.html', context=context)

class AddReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = Products.objects.get(pk=pk)
        add_review_form = AddReviewForm()
        context = {
            'product': product,
            'add_review_form': add_review_form
        }
        return render(request, 'product/product_detail.html', context=context)

    def post(self, request, pk):
        product = Products.objects.get(pk=pk)
        add_review_form = AddReviewForm(request.POST)
        if add_review_form.is_valid():
            review = add_review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully.')
            return redirect('products:product-detail', pk=pk)
        else:
            messages.error(request, 'Error adding review. Please check the form.')
            context = {
                'product': product,
                'add_review_form': add_review_form
            }
            return render(request, 'product/product_detail.html', context=context)

class UpdateReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        form = AddReviewForm(instance=review)
        return render(request, 'review/update_review.html', {'form': form, 'review': review})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        form = AddReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.') 
            return redirect('products:product-detail', pk=review.product_id)
        else:
            messages.error(request, 'Error updating review. Please check the form.')
        return render(request, 'review/update_review.html', {'form': form, 'review': review})


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        is_user = review.user == request.user
        return render(request, 'review/delete_review.html', {'review': review, 'is_user': is_user})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.user != request.user:
            messages.error(request, "You are not authorized to delete this review.")
            return redirect('products:product-detail', pk=review.product.pk)
        
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('products:product-detail', pk=review.product.pk)
    
class CategoryListView(View):
    def get(self, request):
        category = CategoryProducts.objects.all()
        return render(request, 'product/category_list.html', {'category': category})
    
class CategoryDetailView(View):
    def get(self, request, pk):
        category = get_object_or_404(CategoryProducts, pk=pk)
        products = Products.objects.filter(category=category)
        context = {
            'category': category,
            'products': products,
        }
        return render(request, 'product/category_detail.html', context=context)
    


class OrderProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        form = OrderForm(request.POST)
        order = form.save(commit=False)
        order.product = product
        order.user = request.user
        order.save()
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('products:product-detail', pk=pk)
    
