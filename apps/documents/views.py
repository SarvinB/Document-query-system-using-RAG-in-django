from rest_framework import viewsets

from .models import Document
from .serializers import DocumentSerializer

from services.document_service import DocumentService

from django.db import transaction

from rest_framework.response import Response

from django.db import IntegrityError

class DocumentViewSet(viewsets.ModelViewSet):

    queryset = Document.objects.all()

    serializer_class = DocumentSerializer
    
    lookup_field = "slug"

    def perform_create(self, serializer):
        
        try:

            document = serializer.save()

            DocumentService.process_document(document)
            
        except IntegrityError:
            return Response(
                {"title": "Document with this title already exists."},
                status=200
            )

    def destroy(self, request, *args, **kwargs):

        document = self.get_object()

        DocumentService.delete_document(document.id)

        return Response({"status": "deleted"})
    
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        document = serializer.save()
        DocumentService.process_document(document)

    def perform_update(self, serializer):
        
        document = serializer.save()
                
        DocumentService.update_document(document)