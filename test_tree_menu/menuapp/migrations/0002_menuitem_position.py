# Generated by Django 4.1.7 on 2023-04-30 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='position',
            field=models.PositiveIntegerField(default=0, help_text='Determine item position on curremt level.'),
        ),
    ]