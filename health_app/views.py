from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            print("yess") # Save the user instance
            UserProfile.objects.create(user=user)  # Create UserProfile linked to the user
            return redirect('login')  
    else:
        form = UserRegistrationForm()
    return render(request, 'todo_app/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'todo_app/login.html'

from django.shortcuts import render
from django.shortcuts import render, redirect

from .models import Exercise




from django.shortcuts import render
from django.http import JsonResponse
import openai

openai.api_key = "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"

messages = [{"role": "system", "content": "You are a health expert that specializes in health advice."}]
responses = [] 

@login_required
def custom_chat_gpt(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})

    responses.append(ChatGPT_reply)
    
    return ChatGPT_reply
from .models import UserHealthData,User

@login_required
def health_tracker_view(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        response = custom_chat_gpt(user_input)
        response_points = response.split('\n')
        print(response_points)
        user_health_data= UserHealthData.objects.create(user=request.user, data=response_points)
        return render(request, "health_app/health_tracker.html", {"response_points": response_points})
    return render(request, "health_app/health_tracker.html")


@login_required
def responses_view(request):
    return render(request, "health_app/responses.html", {"responses": responses})




@login_required
def home(request):
    import json
    import requests
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(
            api_url + query, headers={'X-Api-Key': 'DWuCI3z4Qakky7/FdzHJHg==yRSlXi5uPF9CUECz'})
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'query': 'Enter a valid query'})

import requests
from django.shortcuts import render

@login_required
def activity_calories(request):
    activity = 'cycling'
    api_url = 'https://api.api-ninjas.com/v1/caloriesburned?activity={}'.format(activity)
    response = requests.get(api_url, headers={'X-Api-Key': 'DWuCI3z4Qakky7/FdzHJHg==yRSlXi5uPF9CUECz'})

    if response.status_code == requests.codes.ok:
        data = response.json()
        print(data)
    else:
        data = []

    return render(request, 'activity_calories.html', {'activity_data': data})

from django.shortcuts import render
import json
import requests

from django.shortcuts import render
import json
import requests

@login_required
def calorie_calculator(request):
    total_calories = None

    if request.method == 'POST':
        query = request.POST.get('query')
        food_items = [item.strip() for item in query.split(',')]

        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='

        total_calories = 0
        

        for item in food_items:
            api_request = requests.get(
                api_url + item, headers={'X-Api-Key': 'DWuCI3z4Qakky7/FdzHJHg==yRSlXi5uPF9CUECz'})
            print(f"API URL for {item}: {api_request.url}")  # Check the URL being requested
            print(f"API response for {item}: {api_request.content}") 
            print(f"data{item}:{api_request.content[1]}")
            api_response = api_request.content.decode('utf-8')
            api_data = json.loads(api_response)
            print(api_data)
            total_calories += float(api_data[0].get('calories', 0))
            print(total_calories)
            

    return render(request, 'calorie_calculator.html', {'total_calories': total_calories})

from django.shortcuts import render
import requests
import json

@login_required
def exercise_nutrition(request):
    if request.method == 'POST':
        exercise_name = request.POST.get('exercise_name')
        api_url = f'https://api.api-ninjas.com/v1/exercises?muscle={exercise_name}'
        response = requests.get(api_url, headers={'X-Api-Key': 'DWuCI3z4Qakky7/FdzHJHg==yRSlXi5uPF9CUECz'})

        if response.status_code == requests.codes.ok:
            api_data = json.loads(response.content.decode('utf-8'))
            exercise_info = api_data[0] if api_data else None
        else:
            exercise_info = None

        return render(request, 'exercise_nutrition.html', {'exercise_info': exercise_info})
    return render(request, 'exercise_nutrition.html')

@login_required
def workout_view(request):
    return render(request, 'workout.html')


def index_view1(request):
   return render(request, 'welcome.html')

def index_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'welcome.html',{'user_profile':user_profile})


def aqualog(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'aqualog.html',{'user_profile':user_profile})

@login_required
def homepage(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'homepage.html',{'user_profile':user_profile})

from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.models import User
from .models import UserProfile

@login_required
def view_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'view_profile.html', {'user_profile': user_profile})

@login_required
def edit_profile(request):
    print(request.user)
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})


import openai
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from health_app.models import UserProfile

def is_health_related(reply):
    health_keywords = ["health", "medical", "doctor", "symptom", "illness", "wellness", "nutrition", "diet", "exercise", "healthy", "well-being"]  # Add more relevant keywords

    # Check if any of the health-related keywords are present in the reply
    for keyword in health_keywords:
        if keyword in reply.lower():
            return True
    return False

def chatbot_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        prompts = []
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        
        prompts.extend(conversation)

       
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompts,
            api_key="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",
        )

     
        chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']

       
        health_advice_replies = []
        for reply in chatbot_replies:
            if is_health_related(reply):
                health_advice_replies.append(reply)

        # If no health-related advice is found, provide a friendly message
        if not health_advice_replies:
            health_advice_replies.append("I'm here to provide health-related advice, including topics like diet and nutrition. Feel free to ask any health-related questions.")

        # Handle greetings
        greetings = ["hey", "hi", "hello","heyy"]
        if user_input.lower() in greetings:
            health_advice_replies.insert(0, "Hello! How can I assist you with your health-related questions today?")

        # Append health-related chatbot replies to the conversation
        for reply in health_advice_replies:
            conversation.append({"role": "assistant", "content": reply})

        # Update the conversation in the session
        request.session['conversation'] = conversation
        

        return render(request, 'chat.html', {'user_input': user_input,'user_profile':user_profile, 'chatbot_replies': health_advice_replies, 'conversation': conversation})
    else:
        request.session.clear()
        return render(request, 'chat.html', {'conversation': conversation})
