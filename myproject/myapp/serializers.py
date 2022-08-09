from rest_framework import serializers
from .models import *

class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model =Movie
        fields='__all__'

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('movie', 'content', 'created_at', 'update_at')