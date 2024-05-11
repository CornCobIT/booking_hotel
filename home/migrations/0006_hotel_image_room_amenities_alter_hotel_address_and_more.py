# Generated by Django 5.0.4 on 2024-05-10 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_hotel_amenities_remove_hotel_hotel_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='image',
            field=models.ImageField(default=None, upload_to='hotel_img'),
        ),
        migrations.AddField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(to='home.amenities'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='phone_number',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='roomimages',
            name='images',
            field=models.ImageField(upload_to='room_img'),
        ),
    ]