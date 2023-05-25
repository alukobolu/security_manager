from django.urls import path, include
from . import views

app_name = "main_api"

urlpatterns = [
    path('', views.Welcome.as_view(), name='welcome'), #get

    path('create/offense', views.OffenseView.as_view(), name='create-offense'), #post
    
    path('get/offense', views.OffenseView.as_view(), name='get-offense'), #get
    
    path('delete/offense', views.OffenseView.as_view(), name='delete-offense'), #delete
    
    path('get/expulsion', views.GetExpulsion.as_view(), name='get-expulsion'), #get

    path('get/suspension', views.GetSuspension.as_view(), name='get-suspension'), #get
    
    path('get/offense', views.OffenseView.as_view(), name='get-offense'), #get
    

    path('update/offense', views.UpdateOffenseView.as_view(), name='update-offense'), #post
    path('get/offense-form/<offense_id>', views.UpdateOffenseView.as_view(), name='get-update-offense'), #get
    
    path('student/search/<query>', views.OffenseSsearch.as_view(), name='offense-search'), #post


    path('report', views.GetOffenseReport.as_view(), name='offense-report'), #get
]