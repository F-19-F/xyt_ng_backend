# Generated by Django 4.0.5 on 2022-07-08 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edubackend', '0013_alter_educlass_xnm'),
    ]

    operations = [
        migrations.RenameField(
            model_name='educlass',
            old_name='xnm',
            new_name='xn',
        ),
    ]