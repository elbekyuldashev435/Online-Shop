from django.forms import ModelForm

from products.models import Review, Order


class AddReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'star_given']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'number']