# Generated by Django 3.2.15 on 2022-10-16 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carbooking', '0006_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='user',
            new_name='client',
        ),
    ]