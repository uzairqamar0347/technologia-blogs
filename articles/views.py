from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article, Category

def article_list(request):
    articles_list = Article.objects.all().order_by('-pub_date')
    
    # Check if there are any articles at all
    if articles_list.exists():
        featured_article = articles_list.first()
        # Exclude the featured article from the paginated list
        paginator = Paginator(articles_list.exclude(id=featured_article.id), 10)
    else:
        # If there are no articles, set featured_article to None
        featured_article = None
        paginator = Paginator([], 10) # Empty paginator
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'articles/article_list.html', {
        'featured_article': featured_article,
        'page_obj': page_obj,
        'articles': page_obj.object_list,
        'categories': categories
    })
    
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})

def category_list(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    articles_list = Article.objects.filter(category=category).order_by('-pub_date')
    
    paginator = Paginator(articles_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'articles/category_list.html', {
        'category': category, 
        'articles': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories
    })