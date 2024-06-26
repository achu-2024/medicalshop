# Generated by Django 4.2.7 on 2023-11-29 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_cart_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('price', models.IntegerField()),
                ('description', models.CharField(max_length=1000)),
                ('features', models.CharField(max_length=1000)),
                ('discount', models.IntegerField()),
                ('category', models.CharField(choices=[('a', 'Diabetescare'), ('b', 'Healthcare'), ('c', 'Painrelief'), ('d', 'Ayurveda'), ('e', 'Homeopathy'), ('f', 'Dermacare'), ('g', 'Oralcare'), ('h', 'Babycare'), ('i', 'Adultcare'), ('j', 'Vitamins'), ('k', 'Sports'), ('l', 'Family'), ('m', 'Supports'), ('n', 'Weight')], default='a', max_length=100)),
                ('image', models.ImageField(upload_to='images/product')),
            ],
        ),
    ]
