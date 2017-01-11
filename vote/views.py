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
import requests
from operator import itemgetter


# get token and login
@csrf_exempt
def get_token(request):
    """
    Try to get a token and login
    """
    school_id = request.POST['sid']
    password = request.POST['password']

    # check whether the activity has started
    if datetime.datetime.now() > datetime.datetime(2016, 11, 16, 0):
        return JsonResponse({'info': 0})

    # check whether the user has voted
    if is_vote_today(school_id):
        return JsonResponse({'info': 1})

    # check whether the student who use this student number has been generated the User model
    user_set = User.objects.filter(username=school_id)
    if user_set:
        user = user_set[0]
    else:
        if whu_student_check(school_id, password):
            # authentication succeeded and generate User model
            user = generate_user(school_id, password)
        else:
            # authentication failed and return login failed
            return JsonResponse({'info': 0})

    # check whether there is a valid token, or create new one
    token_set = Token.objects.filter(user_id=user.id)
    if token_set:
        token = token_set[0].key
    else:
        token = create_token(user)
    return JsonResponse({'token': token})


def create_token(user):
    """
    create new token for user
    """
    token = Token.objects.create(user=user)
    print(token.key)
    return token.key


def generate_user(school_id, password):
    """
    generate new user model
    """
    user = User.objects.create_user(
        school_id,
        '',
        password
    )
    return user


def whu_student_check(school_id, password):
    """
    check whether the user is a Wuhan university student
    """
    url = "http://www.whusu.com.cn/check.php?sid=" + school_id + "&password=" + password
    r = requests.get(url)
    if r.text == '1':
        return 1
    else:
        return 0


def is_vote_today(sid):
    """
    check whether the user has voted today
    """
    vote_set = VoteItem.objects.filter(school_id=sid)
    for item in vote_set:
        item_create_time = item.create_time + datetime.timedelta(hours=8)
        item_date = item_create_time.date()
        if item_date == datetime.datetime.now().date():
            return True
    return False


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


# list item
class PhotographicWorkItemViewSet(viewsets.ModelViewSet):
    """
    get photo graphic work item list
    """
    queryset = PhotographicWorkItem.objects.all().order_by('sort')
    serializer_class = PhotographicWorkItemSerializer
    permission_classes = [AllowAny, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('group', 'name')


class PhotoItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = PhotoItem.objects.all()
    serializer_class = PhotoItemSerializer


# vote
class VoteItemCreate(APIView):
    """
    create vote item
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    # def get(self, request, format=None):
    #     vote_item = VoteItem.objects.all()
    #     serializer = VoteItemSerializer(vote_item, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        vote_num_today = count_today_vote(request.data['school_id'])

        if vote_num_today >= 10:
            return JsonResponse({'info': 1})
        if is_same_vote_item_today(request.data['school_id'], request.data['photographic_work_item']):
            return JsonResponse({'info': 2})

        serializer = VoteItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def count_today_vote(sid):
    """
    get the number of votes cast today
    """
    num = 0
    vote_set_for_user = VoteItem.objects.filter(school_id=sid)
    for item in vote_set_for_user:
        if item.create_time.date() == datetime.datetime.now().date():
            # check whether the date of the vote item equal to the date today
            num += 1
    return num


def is_same_vote_item_today(sid, photographic_work_item_id):
    """
    check whether vote for the same item today
    """
    vote_set = VoteItem.objects.filter(school_id=sid, photographic_work_item_id=photographic_work_item_id)
    for item in vote_set:
        if item.create_time.date() == datetime.datetime.now().date():
            return True
    return False


def random_sort(request):
    queryset = PhotographicWorkItem.objects.all()
    for item in queryset:
        item.sort = random.random()
        print(item.sort)
        item.save()
    return None


def sort(request):
    r = requests.get("http://api.whusu.com.cn/p_w_i/?group=1")
    list = r.json()['results']
    while r.json()['next']:
        r = requests.get(r.json()['next'])
        list += r.json()['results']

    row_by_vote = sorted(list, key=itemgetter('vote'))
    i = 0
    for item in row_by_vote[::-1]:
        i += 1
        pwi = PhotographicWorkItem.objects.get(id=item['id'])
        pwi.sort = i
        pwi.save()










