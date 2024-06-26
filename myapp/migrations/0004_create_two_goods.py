# Generated by Django 5.0 on 2024-01-11 13:28

from django.db import migrations


def create_two_goods(apps, schema_editor):
    Goods = apps.get_model('myapp', 'Goods')
    Goods.objects.create(name='First', description="First description",  price=1, quantity=11)
    Goods.objects.create(name='Second', description="Second description", price=2, quantity=22)


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_product_returngoods_purchase'),
    ]

    operations = [
        migrations.RunPython(create_two_goods)
    ]
