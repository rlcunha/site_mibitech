from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("<h1>Hello, World!</h1><p>Django application running with Docker Swarm, Traefik, and Nginx.</p>")