# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-09 05:39
from __future__ import unicode_literals

from django.db import migrations, models


def forwards(apps, schema_editor):
    change_foreign_keys(apps, schema_editor,
                        "auth", "User",
                        "weblate_auth", "User")


def backwards(apps, schema_editor):
    change_foreign_keys(apps, schema_editor,
                        "weblate_auth", "User",
                        "auth", "User")


def change_foreign_keys(apps, schema_editor, from_app, from_model_name, to_app, to_model_name):
    FromModel = apps.get_model(from_app, from_model_name)
    ToModel = apps.get_model(to_app, to_model_name)

    fields = FromModel._meta.get_fields(include_hidden=True)

    for rel in fields:
        if not hasattr(rel, 'field') or not isinstance(rel.field, models.ForeignKey):
            continue
        fk_field = rel.field

        f_name, f_field_name, pos_args, kw_args = fk_field.deconstruct()

        # fk_field might have been the old or new one. We need to fix things up.
        old_field_kwargs = kw_args.copy()
        old_field_kwargs['to'] = FromModel
        old_field = fk_field.__class__(*pos_args, **old_field_kwargs)
        old_field.model = fk_field.model

        new_field_kwargs = kw_args.copy()
        new_field_kwargs['to'] = ToModel
        new_field = fk_field.__class__(*pos_args, **new_field_kwargs)
        new_field.model = fk_field.model

        if fk_field.model._meta.auto_created:
            # If this is a FK that is part of an M2M on the model itself,
            # we've already dealt with this, by virtue of the data migration
            # that populates the auto-created M2M field.
            if fk_field.model._meta.auto_created in [ToModel, FromModel]:
                continue

            # In this case (FK fields that are part of an autogenerated M2M),
            # the column name in the new M2M might be different to that in the
            # old M2M. This makes things much harder, and involves duplicating
            # some Django logic.

            # Build a correct ForeignKey field, as it should
            # have been on FromModel
            old_field.name = from_model_name.lower()
            old_field.column = "{0}_id".format(old_field.name)

            # build a correct ForeignKey field, as it should
            # be on ToModel
            new_field.name = to_model_name.lower()
            new_field.column = "{0}_id".format(new_field.name)
        else:
            old_field.name = fk_field.name
            old_field.column = fk_field.column
            new_field.name = fk_field.name
            new_field.column = fk_field.column

        print(to_model_name, old_field_kwargs, new_field_kwargs)
        schema_editor.alter_field(fk_field.model, old_field, new_field, strict=True)



class Migration(migrations.Migration):

    dependencies = [
        ('weblate_auth', '0006_autogroup'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards, atomic=False),
    ]
