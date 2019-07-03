from django.urls import path, include

urlpatterns = [
    path('', include('pharm_app.urls'))
]
