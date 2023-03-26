import csv


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