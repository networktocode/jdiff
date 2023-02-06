# Generated by Django 3.2.16 on 2023-02-01 10:33

from django.db import migrations, models
import django.db.models.deletion
import nautobot.core.fields
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("ipam", "0009_alter_vlan_name"),
        ("lb_models", "0002_vippoolresponse"),
    ]

    operations = [
        migrations.CreateModel(
            name="VIPHealthMonitor",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "slug",
                    nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.CharField(max_length=100)),
                ("type", models.CharField(max_length=50)),
                ("url", models.CharField(max_length=50)),
                ("send", models.CharField(max_length=50)),
                ("receive", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="VIPPoolMember",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "slug",
                    nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.CharField(max_length=100)),
                ("protocol", models.CharField(max_length=20)),
                ("port", models.SmallIntegerField()),
                ("fqdn", models.CharField(max_length=50)),
                ("member_args", models.JSONField()),
                (
                    "ipv4_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="ipam.ipaddress",
                    ),
                ),
                (
                    "ipv6_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="ipam.ipaddress",
                    ),
                ),
                (
                    "monitor",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="lb_models.viphealthmonitor"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
