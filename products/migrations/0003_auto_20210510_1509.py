# Generated by Django 3.2 on 2021-05-10 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_ant_formicary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ant',
            name='name',
        ),
        migrations.RemoveField(
            model_name='formicary',
            name='name',
        ),
    ]