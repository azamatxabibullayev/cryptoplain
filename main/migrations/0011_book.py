# Generated by Django 5.1 on 2024-08-17 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_indicator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pdf_file', models.FileField(upload_to='main/books/')),
                ('book_type', models.CharField(choices=[('normal', 'Normal'), ('standart', 'Standart'), ('pro', 'Pro')], max_length=30)),
            ],
            options={
                'db_table': 'book',
            },
        ),
    ]
