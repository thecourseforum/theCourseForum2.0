# Generated by Django 4.1.2 on 2022-10-30 20:44

from django.db import migrations, models
import django.utils.timezone
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('tcf_website', '0007_merge_20221030_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('mod_date', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('author', models.CharField(max_length=50)),
                ('thumbnail_image', models.ImageField(default='placeholder.jpeg', upload_to='')),
                ('body', markdownx.models.MarkdownxField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]