# Generated by Django 5.0.4 on 2024-05-11 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_room_evaluate_room_room_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='hotel_id',
            new_name='hotel',
        ),
    ]