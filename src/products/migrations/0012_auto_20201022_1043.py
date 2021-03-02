# Generated by Django 2.2 on 2020-10-22 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20201022_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='variation',
        ),
        migrations.AddField(
            model_name='product',
            name='variation',
            field=models.ManyToManyField(blank=True, to='products.Variation'),
        ),
    ]
