from django.contrib import admin

from .models import QuestionAnswerHistory

from services.rag_service import RagService



@admin.register(QuestionAnswerHistory)
class QAHistoryAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing existing object
            return ("question", "answer", "retrieved_chunks", "created_at", )
        return ()
    
    def get_exclude(self, request, obj=None):
        if obj is None:  # creating
            return ("created_at", "retrieved_chunks", "answer", )
        return ()
    
    def save_model(self, request, obj, form, change):
        
        RagService().ask(obj.question)
