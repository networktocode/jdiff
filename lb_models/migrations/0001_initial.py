# Generated by Django 3.2.18 on 2023-03-28 08:51

import django.core.serializers.json
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import nautobot.core.fields
import nautobot.extras.models.mixins
import taggit.managers
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('ipam', '0008_prefix_vlan_vlangroup_location'),
        ('extras', '0047_enforce_custom_field_slug'),
        ('dcim', '0014_location_status_data_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('_custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('issuer', models.CharField(blank=True, max_length=50, null=True)),
                ('version_number', models.CharField(blank=True, max_length=50, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=30, null=True)),
                ('name', models.CharField(max_length=50)),
                ('key', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, nautobot.extras.models.mixins.DynamicGroupMixin, nautobot.extras.models.mixins.NotesMixin),
        ),
        migrations.CreateModel(
            name='HealthMonitor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('_custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(max_length=20)),
                ('lrtm', models.BooleanField(blank=True, null=True)),
                ('secure', models.BooleanField(blank=True, null=True)),
                ('url', models.URLField(blank=True, max_length=50, null=True)),
                ('send', models.CharField(blank=True, max_length=50, null=True)),
                ('string', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(max_length=50)),
                ('httprequest', models.CharField(max_length=50)),
                ('receive', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, nautobot.extras.models.mixins.DynamicGroupMixin, nautobot.extras.models.mixins.NotesMixin),
        ),
        migrations.CreateModel(
            name='ServiceGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('_custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(max_length=20)),
                ('td', models.SmallIntegerField()),
                ('sslprofile', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, nautobot.extras.models.mixins.DynamicGroupMixin, nautobot.extras.models.mixins.NotesMixin),
        ),
        migrations.CreateModel(
            name='Vserver',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('_custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('fqdn', models.CharField(max_length=200)),
                ('protocol', models.CharField(max_length=20)),
                ('port', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)])),
                ('method', models.CharField(max_length=50)),
                ('owner', models.CharField(max_length=50)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ipam.ipaddress')),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lb_models.certificate')),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='dcim.device')),
                ('interface', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='dcim.interface')),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lb_models.servicegroup')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('vlan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='ipam.vlan')),
                ('vrf', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='ipam.vrf')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, nautobot.extras.models.mixins.DynamicGroupMixin, nautobot.extras.models.mixins.NotesMixin),
        ),
        migrations.CreateModel(
            name='ServiceGroupBinding',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('_custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='name', unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('protocol', models.CharField(max_length=20)),
                ('port', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(65535), django.core.validators.MinValueValidator(1)])),
                ('fqdn', models.CharField(max_length=200)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ipam.ipaddress')),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lb_models.healthmonitor')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, nautobot.extras.models.mixins.DynamicGroupMixin, nautobot.extras.models.mixins.NotesMixin),
        ),
        migrations.AddField(
            model_name='servicegroup',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lb_models.servicegroupbinding'),
        ),
        migrations.AddField(
            model_name='servicegroup',
            name='monitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lb_models.healthmonitor'),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('_custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('slug', nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from='customer_id', unique=True)),
                ('customer_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('fqdn', models.CharField(max_length=50)),
                ('oe', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('class_type', models.CharField(max_length=20)),
                ('accessibility', models.CharField(max_length=20)),
                ('test_url', models.URLField()),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='dcim.site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, nautobot.extras.models.mixins.DynamicGroupMixin, nautobot.extras.models.mixins.NotesMixin),
        ),
    ]
