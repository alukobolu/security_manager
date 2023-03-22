from django.shortcuts import render
from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import *
from accounts.models import *
from django.db.models import Count
from django.db.models.functions import TruncMonth
import datetime

#Pagination default
paginator = PageNumberPagination()
paginator.page_size = 20


class OffenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        instance                    = Offenses()
        instance.offense             = request.data["offense"]
        instance.name              = request.data["name"]
        instance.matric            = request.data["matric"]
        instance.department        = request.data["department"]
        instance.punishment        = request.data["punishment"]
        instance.completed          = request.data["completed"]
        instance.pardon             = request.data["pardon"]
        instance.ongoing          = request.data["ongoing"]
        instance.created_at         = datetime.datetime.today()
        instance.save()
        data = {}
        data['success'] = "Successfully created"
        return Response(data=data)

    def delete(self,request):
        offense_id = request.data["offense_id"]
        offense = Offenses.objects.get(offense_id = offense_id)
        offense.delete()
        data = {}
        data['success'] = "Deleted Successfully"
        return Response(data=data)

    def get(self,request):
        content = []
        offenses = Offenses.objects.all()
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
        
        context = paginator.paginate_queryset(content, request)
        page_response = paginator.get_paginated_response(context)
        return page_response

class UpdateOffenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        offense_id = request.data["offense_id"]
        offense = Offenses.objects.get(offense_id = offense_id)
        offense.offense           = request.data["offense"]
        offense.name              = request.data["name"]
        offense.matric            = request.data["matric"]
        offense.department        = request.data["department"]
        offense.punishment        = request.data["punishment"]
        offense.completed         = request.data["completed"]
        offense.pardon             = request.data["pardon"]
        offense.ongoing            = request.data["ongoing"]
        offense.save()
        data = {}
        data['success'] = "Successfully"
        return Response(data=data)

class OffenseSsearch(APIView):
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
        
        context = paginator.paginate_queryset(content, request)
        page_response = paginator.get_paginated_response(context)
        return page_response

class GetOffenseReport(APIView):
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
            for offens in offenses1:
                data1 = {}
                data1["offense"] = offens.offense
                data1['total'] = offens.total
                data["content"].append(data1)
            content.append(data)

        context = paginator.paginate_queryset(content, request)
        page_response = paginator.get_paginated_response(context)
        return page_response
