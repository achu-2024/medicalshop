# Generated by Django 4.2.6 on 2024-04-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0028_orderitem_stck_chnge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='stck_chnge',
            field=models.IntegerField(default=0),
        ),
    ]