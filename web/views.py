import datetime

from django.shortcuts import render, redirect, get_object_or_404

from web.forms import RegistrationForm, AuthForm, NoteForm, TagForm, NoteFilterForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db.models import Count, F, Max, Min, Q, Sum
from django.db.models.functions import TruncDate

from web.models import Note, Tag

User = get_user_model()


@login_required
def main_view(request):
    notes = Note.objects.all().filter(user=request.user).order_by('-updated_at')

    filter_form = NoteFilterForm(request.GET)
    filter_form.is_valid()
    filters = filter_form.cleaned_data

    if filters['search']:
        notes = notes.filter(text__icontains=filters['search'])

    if filters['start_date']:
        notes = notes.filter(updated_at__gte=filters['start_date'])

    if filters['end_date']:
        notes = notes.filter(updated_at__lte=filters['end_date'])

    total_count = notes.count()
    notes = notes.prefetch_related("tags").select_related("user").annotate(
        tags_count=Count("tags"),
        spent_time=now() - F("updated_at")
    )

    page_number = request.GET.get("page", 1)
    paginator = Paginator(notes, per_page=10)

    return render(request, 'web/main.html', {
        "notes": paginator.get_page(page_number),
        "form": NoteForm(),
        "filter_form": filter_form,
        "total_count": total_count
    })


def analytics_view(request):
    overall_stat = Note.objects.aggregate(
        count=Count("id"),
        max_date=Max("created_at"),
        min_date=Min("created_at")
    )
    days_stat = (
        Note.objects
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(
            count=Count("id")
        )
            .order_by('-date')
    )

    return render(request, "web/analytics.html", {
        "overall_stat": overall_stat,
        'days_stat': days_stat
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
            print(form)
            print(form.cleaned_data)

    return render(request, 'web/registration.html', {'form': form, 'is_success': is_success})


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, 'Введены неверные данные')
            else:
                login(request, user)
                return redirect('main')
    return render(request, 'web/auth.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main')


@login_required
def note_edit_view(request, id=None):
    note = get_object_or_404(Note, user=request.user, id=id) if id is not None else None
    if note is not None:
        note.updated_at = now()
    else:
        note = Note(created_at=now(), updated_at=now())
    form = NoteForm(instance=note)
    if request.method == 'POST':
        form = NoteForm(data=request.POST, files=request.FILES, instance=note, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'web/note_form.html', {'form': form})


@login_required
def note_delete_view(request, id):
    note = get_object_or_404(Note, user=request.user, id=id)
    note.delete()
    return redirect('main')


def _list_editor_view(request, model_cls, form_cls, template_name, url_name):
    items = model_cls.objects.filter(user=request.user)
    form = form_cls()
    if request.method == 'POST':
        form = form_cls(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect(url_name)
    return render(request, f"web/{template_name}.html", {"items": items, "form": form})


@login_required
def tags_view(request):
    return _list_editor_view(request, Tag, TagForm, "tags", "tags")


@login_required
def tags_delete_view(request, id):
    tag = get_object_or_404(Tag, user=request.user, id=id)
    tag.delete()
    return redirect('tags')
