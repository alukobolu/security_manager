from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from accounts.models import *
from django.db.models import Count
from django.db.models.functions import TruncMonth
import datetime

#Pagination default
paginator = PageNumberPagination()
paginator.page_size = 20

from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views import View
# Create your views here.
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.shortcuts import resolve_url
from django.views import View
from django.shortcuts import redirect

class Welcome(View):
    permission_classes = [AllowAny]
    def get(self,request):
        template_name = 'welcomepage.html'
        return render(request, template_name)

# Create your views here.
class OffenseView(View):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        instance                    = Offenses()
        instance.offense             = request.POST["offense"]
        instance.name              = request.POST["name"]
        instance.matric            = request.POST["matric"]
        instance.department        = request.POST["department"]
        instance.punishment        = request.POST["punishment"]
        if request.POST.get("completed") ==True:
            instance.completed          = True
        # instance.pardon             = request.POST["pardon"]
        if request.POST.get("ongoing") ==True:
            instance.ongoing          = True
        instance.created_at         = datetime.datetime.today()
        instance.save()
        data = "Successfully created"
        messages.success(request, data)
        template_name = 'offenderadded.html'
        return render(request, template_name)


    def delete(self,request):
        offense_id = request.data["offense_id"]
        offense = Offenses.objects.get(offense_id = offense_id)
        offense.delete()
        data = "Successfully created"
        messages.success(request, data)
        return redirect('/main/get/offense')

    def get(self,request):
        content = []
        offenses = Offenses.objects.all()
        data = {}
        data["data"] = offenses
        template_name = 'offenders_list.html'
        return render(request, template_name, data)

class UpdateOffenseView(View):
    permission_classes = [IsAuthenticated]

    def get(self,request,offense_id):
        data = {}
        if offense_id != "none":
            offense = Offenses.objects.get(offense_id = offense_id)
            data['offense_id'] = offense.offense_id
            data['offense'] = offense.offense
            data['pardon'] = offense.pardon
            data['name'] = offense.name
            data['matric'] = offense.matric
            data['department'] = offense.department
            data['punishment'] = offense.punishment
            data['ongoing'] = offense.ongoing
            data['completed'] = offense.completed
            data['created_at'] = offense.created_at
            template_name = 'statusupdate.html'
        else:
            template_name = 'index.html'
        return render(request, template_name,data)

    def post(self,request):
        offense_id = request.POST["offense_id"]
        offense = Offenses.objects.get(offense_id = offense_id)
        offense.offense           = request.POST["offense"]
        offense.name              = request.POST["name"]
        offense.matric            = request.POST["matric"]
        offense.department        = request.POST["department"]
        offense.punishment        = request.POST["punishment"]
        offense.completed         = request.POST["completed"]
        offense.pardon             = request.POST["pardon"]
        offense.ongoing            = request.POST["ongoing"]
        offense.save()
        data = "done"
        messages.success(request, data)
        return redirect('/main/get/offense')

class OffenseSsearch(View):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,query):
        content = []
        offenses = Offenses.objects.filter(Q(name__icontains = query)|Q(matric__icontains = query)|Q(department__icontains = query))
        for offense in offenses:
            data = {}
            data['offense_id'] = offense.offense_id
            data['offense'] = offense.offense
            data['pardon'] = offense.pardon
            data['name'] = offense.name
            data['matric'] = offense.matric
            data['department'] = offense.department
            data['punishment'] = offense.punishment
            data['ongoing'] = offense.ongoing
            data['completed'] = offense.completed
            data['created_at'] = offense.created_at
            content.append(data)
        
        context = {}
        context["report"] = content
        template_name = 'offenders_list.html'
        return render(request, template_name, context)

class GetExpulsion(View):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        query ="expulsion"
        content = []
        offenses = Offenses.objects.filter(punishment__icontains = query)
        for offense in offenses:
            data = {}
            data['offense_id'] = offense.offense_id
            data['offense'] = offense.offense
            data['pardon'] = offense.pardon
            data['name'] = offense.name
            data['matric'] = offense.matric
            data['department'] = offense.department
            data['punishment'] = offense.punishment
            data['ongoing'] = offense.ongoing
            data['completed'] = offense.completed
            data['created_at'] = offense.created_at
            content.append(data)
        
        context = {}
        context["list"] = content
        template_name = 'expulsion_list.html'
        return render(request, template_name, context)

class GetSuspension(View):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        query ="suspension"
        content = []
        offenses = Offenses.objects.filter(punishment__icontains = query)
        for offense in offenses:
            data = {}
            data['offense_id'] = offense.offense_id
            data['offense'] = offense.offense
            data['pardon'] = offense.pardon
            data['name'] = offense.name
            data['matric'] = offense.matric
            data['department'] = offense.department
            data['punishment'] = offense.punishment
            data['ongoing'] = offense.ongoing
            data['completed'] = offense.completed
            data['created_at'] = offense.created_at
            content.append(data)
        
        context = {}
        context["list"] = content
        template_name = 'suspension_list.html'
        return render(request, template_name, context)


class GetOffenseReport(View):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        content = []
        months = Offenses.objects.annotate(month=TruncMonth('created_at')).values('month',).order_by().values('month',).distinct()
        # print(offenses1)
        for amonth in months:
            data = {}
            data["month"] = amonth["month"]
            month = amonth["month"].month
            offenses1 = Offenses.objects.filter(created_at__month = month).annotate(total=Count('offense_id'))
            print(offenses1)
            data["content"] = []
            off = set()
            for offens in offenses1:
                off.add(offens.offense)
            for o in off:
                num = 0
                for f in offenses1:
                    if f.offense == o:
                        num = num + f.total
                data1 = {}
                data1["offense"] = o
                data1['total'] = num
                data["content"].append(data1)

            # for offens in offenses1:
            #     data1 = {}
            #     data1["offense"] = offens.offense
            #     data1['total'] = offens.total
            #     data["content"].append(data1)
            content.append(data)

        context = {}
        context["report"] = content
        template_name = 'monthly_report.html'
        return render(request, template_name,context)
