# Generated by Django 3.1.4 on 2021-01-11 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0006_auto_20210110_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='recipes',
            field=models.ManyToManyField(through='jedzonko.RecipePlan', to='jedzonko.Recipe'),
        ),
    ]
