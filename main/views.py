from django.shortcuts import render
from .utils.ai import AI
from django.http import JsonResponse
import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

def main(request):
    AI.createRecommendationInstance()
    response = AI.getMostPopularBooksByCategories()  
    items = []
    book_images = ['images/book_image.png', 'images/book_image1.png', 'images/book_image2.png', 'images/book_image3.png']

    if response:
        for book in response:
            
            items.append({
                'title': book.get('Title', 'No Title'), 
                'description': book.get('Description', 'No Description'), 
                'category': book.get('Category', 'No Category'), 
                'price':10,
                'image': random.choice(book_images),
                'button_text': 'Order Now', 
            })


    return render(request, "index.html", {'books': items})


def popular(request):
    response = AI.getMostPopularBooksByCategories()  
    items = []
    book_images = ['images/book_image.png', 'images/book_image1.png', 'images/book_image2.png', 'images/book_image3.png']

    if response:
        for book in response:
            items.append({
                'title': book.get('Title', 'No Title'), 
                'description': book.get('Description', 'No Description'), 
                'category': book.get('Category', 'No Category'),
                'image': random.choice(book_images),
                'price':10,
                'button_text': 'Order Now', 
            })
    return render(request, "popular.html", {'books': items})

def get_books(request):
    if request.method == "POST":
        data = json.loads(request.body)  # POST isteğinden gelen veriyi al
        title = data.get('title', '')  # Kitap başlığını al
        
        # Kitapları başlığa göre filtrele
        books = AI.recommend(title)
        
        # Kitapları JSON formatında döndür
        book_data = []
        for book in books:
            book_data.append({
                'title': book,
                'description': "book.description",
                'category': "book.category",
            })
        
        return JsonResponse({'books': book_data})

    return JsonResponse({'error': 'Invalid method'}, status=400)

def get_book_info(request, book_name):
    resp = AI.getBookInfo(book_name)

    book = {
                'title': resp.get('Title', 'No Title'), 
                'description': resp.get('Description', 'No Description'), 
                'category': resp.get('Category', 'No Category'), 
            }
    return render(request, 'bookinfo.html', {'book': book})

def recommend(request):

    return render(request, "recommend.html")

@csrf_exempt
def recommendApi(request):
    if request.method == "GET":
        name = request.GET.get('name', '')
    
        books = AI.recommend(name) 
        book_data = []
        for book in books:
            book_data.append({
                'title': book,
                'description': "book.description",
                'category': "book.category",
            })
        
        return JsonResponse({'book': book_data[0]})

    return JsonResponse({'error': 'Invalid HTTP method. Use GET.'}, status=400)