# Generated by Django 5.1.2 on 2024-10-19 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productvariation_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariation',
            name='color',
            field=models.CharField(help_text='only letters and spaces, without accents (Ex.: blue and pink)', max_length=20, verbose_name='Cor'),
        ),
    ]
