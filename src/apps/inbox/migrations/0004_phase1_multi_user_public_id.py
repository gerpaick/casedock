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
    InboxItem = apps.get_model("inbox", "InboxItem")
    for item in InboxItem.objects.all():
        item.user_id = first_user_id
        item.public_id = uuid.uuid7()
        item.save(update_fields=["user", "public_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("inbox", "0003_alter_inboxitem_triage_state"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="inboxitem",
            name="public_id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid7,
                editable=False,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="inboxitem",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="inbox_items",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(backfill_user_and_public_id, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="inboxitem",
            name="public_id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid7,
                editable=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="inboxitem",
            name="user",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="inbox_items",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
