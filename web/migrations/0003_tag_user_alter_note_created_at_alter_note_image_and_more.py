# Generated by Django 4.1.5 on 2023-03-07 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0002_note_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='note',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='note',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='notes/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(to='web.tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.CharField(max_length=256, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='note',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования'),
        ),
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Название тега'),
        ),
    ]
