from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import VoteItem, PhotographicWorkItem, PhotoItem
from rest_framework import viewsets, serializers, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
import datetime
import requests
import re
import random
# Create your views here.


# serializers
class PhotographicWorkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotographicWorkItem
        fields = ('id', 'name', 'group', 'vote', 'photos', 'sort')


class VoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteItem
        fields = ('school_id', 'photographic_work_item', 'create_time', 'group')


class PhotoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoItem
        fields = ('photographic_work_item', 'path')


# auth
def create_token(user):
    token = Token.objects.create(user=user)
    print(token.key)
    return token.key


def generate_user(school_id, password):
    user = User.objects.create_user(
        school_id,
        '',
        password
    )
    return user


def whu_student_check(school_id, password):
    url = "http://www.whusu.com.cn/check.php?sid=" + school_id + "&password=" + password
    r = requests.get(url)
    if r.text == '1':
        return 1
    else:
        return 0


@csrf_exempt
def get_token(request):
    school_id = request.POST['sid']
    password = request.POST['password']

    user_set = User.objects.filter(username=school_id)
    if is_vote_today(school_id):
        return JsonResponse({'info': 1})

    if user_set:
        user = user_set[0]
    else:
        if whu_student_check(school_id, password):
            user = generate_user(school_id, password)
        else:
            return JsonResponse({'info': 0})

    user_id = user.id
    token_set = Token.objects.filter(user_id=user_id)
    if token_set:
        print('have')
        token = token_set[0].key
    else:
        print('none')
        token = create_token(user)
    return JsonResponse({'token': token})


# API view
class VoteItemCreate(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, format=None):
        vote_item = VoteItem.objects.all()
        serializer = VoteItemSerializer(vote_item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # vote_num_today = count_today_vote(request.data['school_id'])

        # if vote_num_today >= 10:
        #     return JsonResponse({'info': 1})
        if is_same_vote_item_today(request.data['school_id'], request.data['photographic_work_item']):
            return JsonResponse({'info': 2})

        serializer = VoteItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotographicWorkItemViewSet(viewsets.ModelViewSet):
    queryset = PhotographicWorkItem.objects.all().order_by('sort')
    serializer_class = PhotographicWorkItemSerializer
    permission_classes = [AllowAny, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('group', 'name')


class PhotoItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = PhotoItem.objects.all()
    serializer_class = PhotoItemSerializer


def count_today_vote(sid):
    num = 0
    vote_set_for_user = VoteItem.objects.filter(school_id=sid)
    for item in vote_set_for_user:
        if item.create_time.date() == datetime.datetime.now().date():
            num += 1
    return num


def is_same_vote_item_today(sid, photographic_work_item_id):
    vote_set = VoteItem.objects.filter(school_id=sid, photographic_work_item_id=photographic_work_item_id)
    for item in vote_set:
        if item.create_time.date() == datetime.datetime.now().date():
            return True
    return False


def is_vote_today(sid):
    vote_set = VoteItem.objects.filter(school_id=sid)
    for item in vote_set:
        item_create_time = item.create_time + datetime.timedelta(hours=8)
        item_date = item_create_time.date()
        if item_date == datetime.datetime.now().date():
            return True
    return False


def tt(request):
    qset = VoteItem.objects.filter(school_id='2014301500228').order_by('-id')
    vo = qset[0]
    st = vo.create_time+datetime.timedelta(hours=8)
    std = st.date()
    st2 = datetime.datetime.now().date()
    return HttpResponse(std)


def random_sort(request):
    queryset = PhotographicWorkItem.objects.all()
    for item in queryset:
        item.sort = random.random()
        print(item.sort)
        item.save()
    return None











