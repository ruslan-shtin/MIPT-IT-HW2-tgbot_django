import random
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseNotFound, HttpResponseBadRequest

from . import models

# Create your views here.


class WordSerializator(serializers.ModelSerializer):
    class Meta:
        model = models.Words
        fields = ['pk', 'en_word', 'ru_translation']


class RandomWord(APIView):
    def get(self, *args, **kwargs):
        print('start random')
        all_words = models.Words.objects.all()
        random_word = random.choice(all_words)
        serialized_random_word = WordSerializator(random_word, many=False)
        return Response(serialized_random_word.data)

    def post(self, request, *args, **kwargs):
        new_word = models.Words.objects.create(en_word=request.data["en_word"], ru_translation=request.data["ru_translation"])
        new_word.save()
        serializer = WordSerializator(new_word)
        return Response(serializer.data)


class NextWord(APIView):
    def get(self, request, pk, format=None):
        """
        Parameters
        ----------
        request : TYPE
            DESCRIPTION.
        pk : TYPE
            Primary Key (ID) последнего взятого слова.
        format : TYPE, optional
            DESCRIPTION. The default is None.

        """
        word = models.Words.objects.filter(pk__gt=pk).first()
        if not word:
            return HttpResponseNotFound()
        serialized_word = WordSerializator(word, many=False)
        return Response(serialized_word.data)


class AddWord(APIView):
    def post(self, request, *args, **kwargs):
        new_word = models.Words.objects.create(en_word=request.data["en_word"], ru_translation=request.data["ru_translation"])
        new_word.save()
        serializer = WordSerializator(new_word)
        return Response(serializer.data)
