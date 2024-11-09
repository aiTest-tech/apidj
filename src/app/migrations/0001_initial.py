# Generated by Django 5.1.3 on 2024-11-09 08:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='audio_files/')),
                ('source', models.TextField()),
                ('edit_source', models.TextField(blank=True, null=True)),
                ('sentiment_analysis', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RatingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(max_length=100)),
                ('audio_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.audiorecord')),
            ],
        ),
    ]
