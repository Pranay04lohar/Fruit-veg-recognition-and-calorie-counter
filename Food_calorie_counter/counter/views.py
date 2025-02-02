# from django.shortcuts import render
# import json
# import requests

# # Create your views here.
# def home(request):
#           # for better understanding see python json and requests modules
          

#           if request.method == "POST":
#                     query = request.POST['query'] # Retrieve the query from the POST data   
#                     api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
#                     api_request = requests.get(api_url+query, headers = ({'X-Api-Key': '/sC8HY71YyfJauqkfrxMrw==iVb36DrKfhki81AC'}))
                    

#                     # serialization--> using json.dumps() converting python object into json
#                     # deserialization --> using json.loads() converting json to python obj
#                     try:
#                               api = json.loads(api_request.content)
#                               print(api_request.content)
#                               #print(type(api))
                              

#                     except Exception as e:
#                               api = "oops! There was an error"
#                               print(e)
#                     return render(request,'home.html',{'api':api})

#           else:
#                     return render(request,'home.html',{'query':'Enter a valid query'})




import json
import requests
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

def home(request):
    query = ""  # Initialize the query variable
    api = None   # Initialize the API data
    uploaded_image_url = request.POST.get('uploaded_image_url', '')


    if request.method == "POST":
        # Handle the file upload
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_image_url = fs.url(filename)  # This should be set if the image is uploaded
            request.session['uploaded_image_url'] = uploaded_image_url  # Save it in session
            print(f"Image uploaded successfully: {uploaded_image_url}")  # This should print the URL if file upload is successful


        # Check if the query comes from the form submission
        query = request.POST.get('query', '').strip()

    # If no query in the form, check if it's coming from the GET URL parameter (image upload redirect)
    if not query:
        query = request.GET.get('query', '').strip()  # Get query from the GET URL parameter

    print(f"Query Sent to API: {query}")  # Debugging
    print(f"Image URL: {uploaded_image_url}")  # Debugging

    if query:  # Proceed if we have a query
        api_url = f'https://api.calorieninjas.com/v1/nutrition?query={query}'
        headers = {'X-Api-Key': '/sC8HY71YyfJauqkfrxMrw==iVb36DrKfhki81AC'} 

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            api = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Calorie API HTTP Error: {e}")
            api = {"error": "Invalid request to Calorie API"}
        except requests.RequestException as e:
            print(f"Request Exception: {e}")
            api = {"error": "API request failed"}
    print(f"Image URL: {uploaded_image_url}") 
    return render(request, 'home.html', {'uploaded_image_url': uploaded_image_url, 'api': api, 'query': query})





def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)  # Path to the uploaded file

        return JsonResponse({'image_url': uploaded_file_url})

    return render(request, 'home.html')









