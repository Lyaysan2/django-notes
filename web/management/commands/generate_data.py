import random
from datetime import timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from web.models import Note, User, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date = now()
        user = User.objects.first()
        tags = Tag.objects.filter(user=user)

        notes = []

        for day_index in range(400):
            current_date -= timedelta(days=1)

            for updated_index in range(randint(0, 5)):
                updated_at = current_date + timedelta(hours=randint(0, 10))
                notes.append(Note(
                    title=f'title {day_index}-{updated_index}',
                    text=f'text {day_index}-{updated_index}',
                    created_at=current_date,
                    updated_at=updated_at,
                    user=user
                ))

        saved_notes = Note.objects.bulk_create(notes)

        note_tags = []
        for note in saved_notes:
            count_of_tags = randint(0, len(tags))
            for tag_index in range(count_of_tags):
                note_tags.append(
                    Note.tags.through(note_id=note.id, tag_id=tags[tag_index].id)
                )
        Note.tags.through.objects.bulk_create(note_tags)
