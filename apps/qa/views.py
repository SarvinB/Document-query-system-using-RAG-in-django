from rest_framework.views import APIView

from rest_framework.response import Response

from .serializers import AskSerializer

from services.rag_service import RagService


class AskView(APIView):

    def post(self, request):

        serializer = AskSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]


        rag = RagService()

        result = rag.ask(question)

        return Response(result)

    # def post(self, request):

    #     serializer = AskSerializer(data=request.data)

    #     serializer.is_valid(raise_exception=True)

    #     question = serializer.validated_data["question"]

    #     rag = RagService()

    #     result = rag.ask(question)

    #     return Response(result)