# Generated by Django 5.0.7 on 2024-08-10 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_feargreedindex_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feargreedindex',
            name='image',
            field=models.ImageField(upload_to='main/home/feargreed/'),
        ),
    ]
