# Generated by Django 4.1.7 on 2023-03-11 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mushroomIdentifyer', '0007_mushroom_latin_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mushroom',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
