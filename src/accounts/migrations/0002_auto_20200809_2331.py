# Generated by Django 3.0.8 on 2020-08-09 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='language',
            field=models.CharField(choices=[('de', 'German'), ('en', 'English')], default='en', max_length=255),
        ),
    ]