# Generated by Django 3.1.5 on 2021-01-22 08:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_allergen', models.BooleanField(default=False)),
                ('has_lactose', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('AP', 'Awaiting Payment'), ('PR', 'Payment Received'), ('PU', 'Payment Updated'), ('CO', 'Completed'), ('RP', 'Refunded Partially'), ('RE', 'Refunded'), ('CA', 'Cancelled'), ('FA', 'Failed'), ('EX', 'Expired')], default='AP', max_length=2)),
                ('payment_method', models.CharField(choices=[('CASH', 'CASH'), ('CARD', 'CARD')], default='', max_length=4)),
                ('delivery_address', models.CharField(max_length=150)),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('price', models.PositiveIntegerField()),
                ('ingredients', models.ManyToManyField(related_name='pizzas', to='pizzalabapp.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='pizzalabapp.order')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='pizzalabapp.pizza')),
            ],
        ),
    ]
