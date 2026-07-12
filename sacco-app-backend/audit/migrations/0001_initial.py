from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("timestamp", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("action", models.CharField(db_index=True, max_length=50)),
                ("user_identifier", models.CharField(db_index=True, max_length=200)),
                ("details", models.TextField(blank=True)),
            ],
            options={"ordering": ["-timestamp"]},
        ),
        migrations.AddIndex(
            model_name="auditlog",
            index=models.Index(fields=["action", "timestamp"], name="audit_audit_action_9f3a1b_idx"),
        ),
        migrations.AddIndex(
            model_name="auditlog",
            index=models.Index(fields=["user_identifier", "timestamp"], name="audit_audit_user_id_2c4d5e_idx"),
        ),
    ]
