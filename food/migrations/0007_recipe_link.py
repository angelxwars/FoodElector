# Generated by Django 2.0 on 2018-01-18 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_recipebook_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='link',
            field=models.URLField(null=True),
        ),
    ]