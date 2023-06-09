# Generated by Django 4.2 on 2023-04-16 23:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('size', models.DecimalField(decimal_places=3, max_digits=10)),
                ('number_of_pages', models.IntegerField()),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='sentence',
            name='pdf_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdf_manager.file'),
        ),
        migrations.DeleteModel(
            name='PDF_File',
        ),
    ]
