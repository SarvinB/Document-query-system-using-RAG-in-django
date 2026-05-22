from rest_framework import serializers

from .models import Document

from services.document_service import DocumentService


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        read_only_fields = ("extracted_text",)
        fields = "__all__"