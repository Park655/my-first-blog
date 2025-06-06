# Generated by Django 5.2 on 2025-05-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='EffectCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='supplement',
            name='effect',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='side_effect',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='supplement',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='supplements', to='blog.effectcategory'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
