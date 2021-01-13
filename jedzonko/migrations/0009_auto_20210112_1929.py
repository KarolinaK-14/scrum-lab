# Generated by Django 2.2.6 on 2021-01-12 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0008_auto_20210111_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='recipes',
            field=models.ManyToManyField(through='jedzonko.RecipePlan', to='jedzonko.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipeplan',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Recipe'),
        ),
    ]
