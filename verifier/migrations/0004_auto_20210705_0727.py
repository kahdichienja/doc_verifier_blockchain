# Generated by Django 3.0 on 2021-07-05 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifier', '0003_auto_20210705_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentblockmodel',
            name='profile_url',
            field=models.FileField(upload_to='profiles'),
        ),
    ]
