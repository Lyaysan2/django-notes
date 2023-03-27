import csv

from web.models import Note, Tag


def filter_notes(notes_qs, filters: dict):
    if filters['search']:
        notes_qs = notes_qs.filter(text__icontains=filters['search'])

    if filters['start_date']:
        notes_qs = notes_qs.filter(updated_at__gte=filters['start_date'])

    if filters['end_date']:
        notes_qs = notes_qs.filter(updated_at__lte=filters['end_date'])

    return notes_qs


def export_notes_csv(notes_qs, response):
    writer = csv.writer(response)
    writer.writerow(("title", "text", "created_at", "updated_at", "tags"))

    for note in notes_qs:
        writer.writerow((
            note.title, note.text, note.created_at, note.updated_at,
            " ".join([n.name for n in note.tags.all()])
        ))

    return response


def import_notes_from_csv(file, user_id):
    strs_from_file = (row.decode() for row in file)
    reader = csv.DictReader(strs_from_file)

    notes = []
    note_tags = []
    for row in reader:
        notes.append(Note(
            title=row['title'],
            text=row['text'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            user_id=user_id
        ))
        note_tags.append(row['tags'].split(" ") if row['tags'] else [])

    saved_notes = Note.objects.bulk_create(notes)

    tags_map = dict(Tag.objects.all().values_list("name", "id"))
    tags = []
    for note, tags_item in zip(saved_notes, note_tags):
        for tag in tags_item:
            tag_id = tags_map[tag]
            tags.append(
                Note.tags.through(note_id=note.id, tag_id=tag_id)
            )
    Note.tags.through.objects.bulk_create(tags)
