# Generated by Django 4.2.8 on 2024-03-27 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcf_website', '0011_review_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='email',
            field=models.CharField(blank=True, default='', null=True),
        ),
    ]
