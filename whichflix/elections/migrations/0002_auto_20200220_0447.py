# Generated by Django 3.0.3 on 2020-02-20 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("users", "0002_device"), ("elections", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="election", name="initiator_id"),
        migrations.RemoveField(model_name="election", name="initiator_type"),
        migrations.AddField(
            model_name="participant",
            name="device",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="users.Device",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="participant",
            name="is_initiator",
            field=models.BooleanField(default=False),
        ),
    ]
