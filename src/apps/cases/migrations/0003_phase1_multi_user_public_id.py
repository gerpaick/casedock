from __future__ import annotations

import uuid_utils.compat as uuid
from django.conf import settings
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def backfill_user_and_public_id(
    apps: migrations.state.StateApps, schema_editor: BaseDatabaseSchemaEditor
) -> None:
    User = apps.get_model("core", "User")
    if not User.objects.exists():
        return
    first_user_id = User.objects.earliest("id").id
    Case = apps.get_model("cases", "Case")
    SpecDocument = apps.get_model("cases", "SpecDocument")
    PrivateNote = apps.get_model("cases", "PrivateNote")
    for case in Case.objects.all():
        case.user_id = first_user_id
        case.public_id = uuid.uuid7()
        case.save(update_fields=["user", "public_id"])
    for spec in SpecDocument.objects.all():
        spec.user_id = first_user_id
        spec.public_id = uuid.uuid7()
        spec.save(update_fields=["user", "public_id"])
    for note in PrivateNote.objects.all():
        note.user_id = first_user_id
        note.public_id = uuid.uuid7()
        note.save(update_fields=["user", "public_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0002_case_stale_ack_count_case_stale_acked_at"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="case",
            name="public_id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid7,
                editable=False,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="specdocument",
            name="public_id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid7,
                editable=False,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="privatenote",
            name="public_id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid7,
                editable=False,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="cases",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="specdocument",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="spec_documents",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="privatenote",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="private_notes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(backfill_user_and_public_id, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="case",
            name="public_id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid7,
                editable=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="specdocument",
            name="public_id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid7,
                editable=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="privatenote",
            name="public_id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid7,
                editable=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="user",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="cases",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="specdocument",
            name="user",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="spec_documents",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="privatenote",
            name="user",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="private_notes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="case",
            name="slug",
            field=models.SlugField(max_length=255),
        ),
        migrations.AddConstraint(
            model_name="case",
            constraint=models.UniqueConstraint(
                fields=("user", "slug"),
                name="uniq_case_slug_per_user",
            ),
        ),
    ]
