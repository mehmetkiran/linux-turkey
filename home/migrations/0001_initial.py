from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContacUsModel',
            fields=[
                ('contacID', models.AutoField(primary_key=True, serialize=False, verbose_name='Sorun ID')),
                ('name', models.CharField(max_length=250, verbose_name='Isim')),
                ('email', models.EmailField(max_length=250, verbose_name='E-mail')),
                ('website', models.CharField(blank=True, max_length=250, verbose_name='Web Site')),
                ('message', models.TextField(verbose_name='Mesaj')),
            ],
        ),
    ]
