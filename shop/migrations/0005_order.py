# Generated by Django 2.2.5 on 2019-09-29 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20190926_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('items_json', models.CharField(max_length=5000)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=5000)),
                ('city', models.CharField(max_length=70)),
                ('state', models.CharField(max_length=70)),
                ('zip_code', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=10)),
            ],
        ),
    ]
