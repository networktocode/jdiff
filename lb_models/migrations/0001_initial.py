# Generated by Django 3.2.18 on 2023-02-17 19:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import nautobot.core.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dcim', '0014_location_status_data_migration'),
        ('ipam', '0008_prefix_vlan_vlangroup_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='VIPCertificate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='serial_number', unique=True)),
                ('issuer', models.CharField(max_length=50)),
                ('version_number', models.CharField(max_length=50)),
                ('serial_number', models.CharField(max_length=30, unique=True)),
                ('signature', models.CharField(max_length=50, unique=True)),
                ('signature_algorithm', models.CharField(max_length=20)),
                ('signature_algorithm_id', models.CharField(max_length=30, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('subject_name', models.CharField(max_length=50)),
                ('subject_pub_key', models.CharField(max_length=100)),
                ('subject_pub_key_algorithm', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VIPHealthMonitor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(max_length=50, null=True)),
                ('url', models.URLField(max_length=50, null=True)),
                ('send', models.CharField(max_length=50, null=True)),
                ('string', models.CharField(max_length=100, null=True)),
                ('code', models.SmallIntegerField(null=True)),
                ('receive', models.CharField(max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VIPPoolMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('protocol', models.CharField(max_length=20)),
                ('port', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)])),
                ('fqdn', models.CharField(max_length=200)),
                ('member_args', models.JSONField(blank=True, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ipam.ipaddress')),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lb_models.viphealthmonitor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VIPPool',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lb_models.vippoolmember')),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lb_models.viphealthmonitor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VIP',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('fqdn', models.CharField(max_length=200)),
                ('protocol', models.CharField(max_length=20)),
                ('port', models.SmallIntegerField(null=True)),
                ('method', models.CharField(max_length=50)),
                ('owner', models.CharField(max_length=50)),
                ('vip_args', models.JSONField(blank=True, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ipam.ipaddress')),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lb_models.vipcertificate')),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='dcim.device')),
                ('interface', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='dcim.interface')),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lb_models.vippool')),
                ('vlan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='ipam.vlan')),
                ('vrf', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='ipam.vrf')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
