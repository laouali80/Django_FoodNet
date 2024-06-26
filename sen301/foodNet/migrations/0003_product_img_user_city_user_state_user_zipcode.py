# Generated by Django 5.0.4 on 2024-04-11 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodNet', '0002_category_remove_user_agreement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ImageField(default='foodnet/assets/default.jpg', upload_to='images'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='zipcode',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
