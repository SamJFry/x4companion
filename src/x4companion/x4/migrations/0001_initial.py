# Generated by Django 5.1.4 on 2024-12-18 21:50

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
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HabitatModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('capacity', models.IntegerField()),
                ('species', models.CharField(max_length=50)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='x4.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='SaveGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='x4.savegame')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('population', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='x4.savegame')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='x4.sector')),
            ],
        ),
        migrations.CreateModel(
            name='Habitat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='x4.habitatmodule')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='x4.station')),
            ],
        ),
        migrations.AddConstraint(
            model_name='habitatmodule',
            constraint=models.UniqueConstraint(fields=('name', 'capacity', 'species'), name='Global unique'),
        ),
        migrations.AddConstraint(
            model_name='sector',
            constraint=models.UniqueConstraint(fields=('name', 'game'), name='No duplicate sectors'),
        ),
        migrations.AddConstraint(
            model_name='station',
            constraint=models.UniqueConstraint(fields=('name', 'game'), name='No duplicate stations'),
        ),
        migrations.AddConstraint(
            model_name='habitat',
            constraint=models.UniqueConstraint(fields=('module', 'station'), name='Unique Habitats'),
        ),
    ]
