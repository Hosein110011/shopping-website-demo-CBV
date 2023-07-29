from django.shortcuts import render
from django.views import View
from .models import Product, Category
from django.shortcuts import get_object_or_404
from orders.forms import CartAddForm
from utils import UserPassesTest
from django.views.decorators.csrf import csrf_exempt





class HomeView(UserPassesTest, View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available = True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products':products, 'categories':categories})
    
  
class ProductDetailView(UserPassesTest, View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, 'home/detail.html', {'product':product, 'form':form})
    

# class BucketHome(UserPassesTest,View):
#     template_name = 'home/bucket.html'
    
#     def get(self, request):
#         objects = all_bucket_objects_task()
#         print('='*90)
#         print(objects)
#         return render(request, self.template_name, {'objects':objects})










