from django.contrib import admin

from .models import Document, DocumentChunk
from services.document_service import DocumentService

from django.core.exceptions import ValidationError


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing existing object
            return ("extracted_text", "file", "title", )
        return ()
    
    def get_exclude(self, request, obj=None):
        if obj is None:  # creating
            return ("extracted_text", "content", "slug", )
        return ("slug", )
    

    def save_model(self, request, obj, form, change):
        
        if Document.objects.exclude(pk=obj.pk).filter(title=obj.title).exists():
            raise ValidationError("A document with this title already exists.")
        super().save_model(request, obj, form, change)

        if not change:
            DocumentService.process_document(obj)
            
        else:
            DocumentService.update_document(obj)
            
    def delete_model(self, request, obj):
        DocumentService.delete_document(obj.id)  # your cleanup logic
        super().delete_model(request, obj)
        
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            DocumentService.delete_document(obj.id)
        queryset.delete()
            



@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    

    readonly_fields = [field.name for field in DocumentChunk._meta.fields]

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
    

