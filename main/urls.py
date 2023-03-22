from django.urls import path, include
from . import views

app_name = "main_api"

urlpatterns = [
   
    path('create/offense', views.OffenseView.as_view(), name='create-offense'), #post
    
    
    
    path('delete/offense', views.OffenseView.as_view(), name='delete-offense'), #delete
    

    
    path('get/offense', views.OffenseView.as_view(), name='get-offense'), #get
    

    path('complete/punishment', views.UpdateOffenseView.as_view(), name='complete-punishment'), #post
    
    path('student/search/<query>', views.OffenseSsearch.as_view(), name='offense-search'), #post


    path('report', views.GetOffenseReport.as_view(), name='offense-report'), #get
]