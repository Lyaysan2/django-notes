from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.serializers import NoteSerializer, TagSerializer
from web.models import Note, Tag


@api_view(["GET"])
@permission_classes([])
def main_view(request):
    return Response({"status": "ok"})


class NoteModelViewSet(ModelViewSet):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.all().select_related("user").prefetch_related("tags").filter(user=self.request.user)


class TagModelViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.all().filter(user=self.request.user)
