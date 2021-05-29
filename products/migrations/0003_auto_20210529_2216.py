# Generated by Django 2.2.17 on 2021-05-29 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210528_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(choices=[('self', 'Self-pickup'), ('delivery', 'Delivery (7$)')], max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'New order'), ('in_progress', 'Order in progress'), ('is_ready', 'Order is ready'), ('completed', 'Order completed')], default='new', max_length=100),
        ),
    ]