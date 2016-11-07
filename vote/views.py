from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import VoteItem, PhotographicWorkItem, PhotoItem
from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
import datetime
# Create your views here.


# serializers
class PhotographicWorkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotographicWorkItem
        fields = ('name', 'group', 'vote')


class VoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteItem
        fields = ('school_id', 'photographic_work_item', 'create_time')


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
    return True


def get_token(request):
    school_id = request.POST['sid']
    password = request.POST['password']

    if whu_student_check(school_id, password):
        user = generate_user(school_id, password)
        token = create_token(user)
        return JsonResponse({'token': token})
    else:
        return JsonResponse({'info': 'cant pass whu_student_check'})


# API view
class VoteItemCreate(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        vote_item = VoteItem.objects.all()
        serializer = VoteItemSerializer(vote_item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        vote_num_today = count_today_vote(request.data['school_id'])

        if vote_num_today >= 12:
            return Response({'info': 'vote limit'}, status=status.HTTP_400_BAD_REQUEST)
        if is_same_vote_item_today(request.data['school_id'], request.data['photographic_work_item']):
            return Response({'info': 'already vote for this item'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VoteItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotographicWorkItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PhotographicWorkItem.objects.all()
    serializer_class = PhotographicWorkItemSerializer


class PhotoItemViewSet(viewsets.ReadOnlyModelViewSet):
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


def tt(request):
    print(VoteItem.objects.get(id=1).create_time.date())
    return HttpResponse('dasdas')











