# Generated by Django 3.1.5 on 2021-01-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzalabapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pizza',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
