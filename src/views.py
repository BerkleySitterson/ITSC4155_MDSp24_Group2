from django.http import HttpResponse
from django.views import View

# This file is used to set up the views/routes for the application. This is where you define functions or classes that handle HTTP requests and return responses.

# Functional View Example:

def my_view(request):
    return HttpResponse('Hello, World!')

# Class-based View Example:

class MyView(View):
    def get(self, request, *args):
        return HttpResponse("Hello, world!")

    def post(self, request, *args):
        return HttpResponse("Hello, world!")
    
# The above example shows different ways of handling HTTP requests. The first example is a functional view, which is a simple function that takes a request object and returns a response.
# The second example is a class-based view, which is a class that defines methods for handling different HTTP methods (e.g., GET, POST, etc.). 