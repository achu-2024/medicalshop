# Generated by Django 4.2.7 on 2024-01-13 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_passwordreset'),
    ]

    operations = [
        migrations.CreateModel(
            name='msg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
    ]
