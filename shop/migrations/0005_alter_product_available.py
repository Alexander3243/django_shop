# Generated by Django 4.1.3 on 2022-12-12 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_contacts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.IntegerField(default=0),
        ),
    ]