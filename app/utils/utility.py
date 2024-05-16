from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import string, requests, random
from app.models import CustomUser

def call_flask_API(request):
    try:
        # URL of flask-API to register Observers
        flask_api_url = "http://127.0.0.1:5000/api/users/add-user-json"

        response = request.post(flask_api_url, json=request)
        print(response)
        if response.status_code == 200:
            return JsonResponse({'message': 'Observation Successful!'}, status=200)
        else:
            return JsonResponse({'error': 'Observer registration failed.'}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_username():

    rand_key = string.ascii_letters + string.digits

    while True:
        # generate 10 random strings
        random_key = ''.join(random.choices(rand_key, k=10))

        # check if key is not in database
        if not CustomUser.objects.filter(user_id=random_key).exists():
            return random_key