from rest_framework import serializers


class AskSerializer(serializers.Serializer):

    question = serializers.CharField()