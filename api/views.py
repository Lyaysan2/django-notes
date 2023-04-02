from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from api.serializers import NoteSerializer
from web.models import Note


@api_view(["GET"])
@permission_classes([])
def main_view(request):
    return Response({"status": "ok"})


@api_view(["GET"])
def notes_view(request):
    notes = Note.objects.all().select_related("user").prefetch_related("tags")
    serializers = NoteSerializer(notes, many=True)
    return Response(serializers.data)
