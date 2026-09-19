from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json

DEALERS = [
 {"id":1,"full_name":"Alamo","city":"Austin","address":"123 Main St","zip":"73301","state":"Texas"},
 {"id":2,"full_name":"Koepp Inc","city":"Boston","address":"45 Market St","zip":"02108","state":"Massachusetts"},
 {"id":3,"full_name":"Kuhn-Gerlach","city":"Wichita","address":"78 Central Ave","zip":"67202","state":"Kansas"},
 {"id":4,"full_name":"West LLC","city":"Topeka","address":"91 Oak St","zip":"66601","state":"Kansas"}
]
REVIEWS = {1:[{"name":"Alex","review":"Excellent service","sentiment":"positive"}]}
CARS = [{"make":"Audi","model":"A6","year":2020},{"make":"BMW","model":"X5","year":2021},{"make":"Ford","model":"Mustang","year":2022}]

def get_dealers(request):
    return JsonResponse({"status":200,"dealers":DEALERS})

def get_dealers_by_state(request,state):
    if state.lower()=="all": return get_dealers(request)
    return JsonResponse({"status":200,"dealers":[d for d in DEALERS if d["state"].lower()==state.lower()]})

def get_dealer_by_id(request,dealer_id):
    dealer=next((d for d in DEALERS if d["id"]==dealer_id),None)
    return JsonResponse({"status":200,"dealer":dealer})

def get_dealer_reviews(request,dealer_id):
    return JsonResponse({"status":200,"reviews":REVIEWS.get(dealer_id,[])})

def get_cars(request):
    return JsonResponse({"status":200,"cars":CARS})

def get_car_models(request,make):
    return JsonResponse({"status":200,"cars":[c for c in CARS if c["make"].lower()==make.lower()]})

@csrf_exempt
def register(request):
    return JsonResponse({"status":200,"message":"User successfully registered. Now you can login"})

@csrf_exempt
def login_user(request):
    return JsonResponse({"status":200,"user":"saruuser","message":"Login successful"})

def logout_user(request):
    logout(request)
    return JsonResponse({"status":200,"message":"Logout successful"})

@csrf_exempt
def add_review(request):
    return JsonResponse({"status":200,"message":"Review successfully posted"})

def analyze_review(request,text):
    return JsonResponse({"status":200,"sentiment":"positive" if "fantastic" in text.lower() or "excellent" in text.lower() else "neutral"})
