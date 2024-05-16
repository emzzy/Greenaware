from app.models import CustomUser
from app.utils.utility import call_flask_API, generate_username
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        try:
            
            # generate user id here 
            id_user = generate_username()
            
            data = {key: request.POST.get(key) for key in request.POST}

            print(data)

            email = data.get('email_address')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            user_role = "observer" if data.get('user_role') == 'on' else 'user'
            password = data.get('password')

            # If user role is 'observer', trigger registration to ezternal API
            if user_role == 'observer':
                data['user_id'] = id_user
                print(data)
                response = call_flask_API(data)
                print(response)
                if response.status_code == 200:
                    # successfull registration on external API
                    messages.success(request, 'Account Created Successfully')
                    return redirect('login')
                else:
                    messages.error(request, 'failed to register user in external API')
                    return redirect('register')

            # creating the user
            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                user_role=user_role,
                password=password,
                email=email
            )

            if user_role != 'observer':
                login(request, user)

            # Redirect to login page after successful registration
            return redirect('login')
                    
        except Exception as e:
            print(e)
            messages.error(request, f'Error: {e}')
            return redirect('register')
    else:
        return render(request, 'authentication/register.html')


@csrf_exempt
def user_login(request):
    if request.method != 'POST':
        return redirect("")

    try:
        data = {key: request.POST.get(key) for key in request.POST}

        print(data)
        email = data.get('email_address')
        password = data.get('password')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect("/login")

        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, 'Invalid email or password.')
            return redirect("/login")

        if not user.is_active:
            messages.error(request, "Your account is not active.")
            return redirect("/login")

        # Log in the user
        login(request, user)
        
        # Redirect user to appropriate dashboard based on user role
        if user.user_role == 'observer':
            return redirect('/observer_dashboard')
        else:
            return redirect('/user_dashboard')

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred. Please try again later.')
        return redirect("/login")

