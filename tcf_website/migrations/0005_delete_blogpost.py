# Generated by Django 4.0.3 on 2022-04-03 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcf_website', '0004_blogpost_subtitle'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogPost',
        ),
    ]