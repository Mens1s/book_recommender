from django.shortcuts import render
from .utils.ai import AI
from django.http import JsonResponse
import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

class Statik:
    static_var = "ahmet"

    @classmethod
    def get_static_var(cls):
        return cls.static_var

    @classmethod
    def set_static_var(cls, value):
        cls.static_var = value

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

def scanbook(request):
    return render(request, "scanbook.html")

def recommend_book(request):
    res = {'book': Statik.get_static_var()}
    Statik.set_static_var("ahmet")
    return JsonResponse(res)

@csrf_exempt
def esp(request):
    if request.method == "GET":
        print(request.GET)
        name = request.GET.get('name', 'ahmet')
        print(name)
        Statik.set_static_var(name)
    
    return JsonResponse({'name': Statik.get_static_var()})

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
        
        books = AI.recommend(title)
        book_data = []
        
        i = 1
        for book in books:
            resp = AI.getBookInfoForRecommendedBook(book)
            
            updatedBook = {
                'title': resp.get('Title', 'No Title'), 
                'description': resp.get('Description', 'No Description'), 
                'category': resp.get('Category', 'No Category'), 
                'coverImage': "images/h"+str(i)+".jpg",
                'author': resp.get('Author', 'No Author'),
                'rating': resp.get('Rating', 'No Rating')
            }

            if len(updatedBook['description']) > 200:
                updatedBook['description'] = updatedBook['description'][:200] + "..."
            
            if "harry" not in updatedBook['title'].lower():
                updatedBook['coverImage'] = "images/s"+str(i)+".jpeg"
            
            if updatedBook['title'] == "No Title":
                continue
            book_data.append(updatedBook)
            i += 1
            if i == 5:
                i = 1
        print(len(book_data))
        return JsonResponse({'books': book_data})

    return JsonResponse({'error': 'Invalid method'}, status=400)

def get_book_info(request, book_name):
    resp = AI.getBookInfoForRecommendedBook(book_name)

    book = {
                'title': resp.get('Title', 'No Title'), 
                'description': resp.get('Description', 'No Description'), 
                'category': resp.get('Category', 'No Category') +"    "+ resp.get('Rating', 'No Rating'), 
            }
    return render(request, 'bookinfo.html', {'book': book})

def getBookNameFromRfid(id):
    # This parts gets book from db
    # But for now we will use a static list
    # Because there is no enough rfid tags
    bookList = {
        "1": "Harry Potter and the Philosopher's Stone",
        "2": "Harry Potter and the Chamber of Secrets",
        "3": "1984",
        "4":"The Great Gatsby",
    }
    return bookList.get(id, "No Book Found")

def recommend(request):

    return render(request, "recommend.html")

@csrf_exempt
def recommendApi(request):
    if request.method == "GET":
        id = request.GET.get('id', '')
        name = getBookNameFromRfid(id)
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