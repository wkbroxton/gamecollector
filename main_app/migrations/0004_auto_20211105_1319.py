# Generated by Django 3.2.8 on 2021-11-05 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_play_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='play',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='play',
            name='time',
            field=models.CharField(choices=[('M', 'Morning'), ('A', 'Afternoon'), ('E', 'Evening')], default='M', max_length=1, verbose_name='Time of Day Played'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.game')),
            ],
        ),
    ]