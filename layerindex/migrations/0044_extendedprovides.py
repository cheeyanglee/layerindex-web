# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-11-05 22:51
from __future__ import unicode_literals

from django.db import migrations, models


def populate_extended_provides(apps, schema_editor):
    Branch = apps.get_model('layerindex', 'Branch')
    LayerBranch = apps.get_model('layerindex', 'LayerBranch')
    Recipe = apps.get_model('layerindex', 'Recipe')
    ExtendedProvide = apps.get_model('layerindex', 'ExtendedProvide')

    for branch in Branch.objects.filter(comparison=False):
        for layerbranch in LayerBranch.objects.filter(branch=branch):
            for recipe in Recipe.objects.filter(layerbranch=layerbranch):
                provides = recipe.provides.split()
                for extend in recipe.bbclassextend.split():
                    if extend == 'native':
                        provides.append('%s-native' % recipe.pn)
                    elif extend == 'nativesdk':
                        provides.append('nativesdk-%s' % recipe.pn)
                for provide in provides:
                    provides, created = ExtendedProvide.objects.get_or_create(name=provide)
                    if created:
                        provides.save()
                    provides.recipes.add(recipe)


class Migration(migrations.Migration):

    dependencies = [
        ('layerindex', '0043_recipe_srcrev'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedProvide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('recipes', models.ManyToManyField(to='layerindex.Recipe')),
            ],
        ),
        migrations.RunPython(populate_extended_provides, reverse_code=migrations.RunPython.noop),
    ]