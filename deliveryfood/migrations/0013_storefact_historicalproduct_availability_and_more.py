# Generated by Django 5.1.3 on 2025-01-20 15:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryfood', '0012_remove_historicalprofile_user_remove_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreFact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Факт о магазине',
                'verbose_name_plural': 'Факты о магазине',
            },
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='availability',
            field=models.CharField(choices=[('available', 'Доступно'), ('unavailable', 'Недоступно')], default=1, max_length=12, verbose_name='Доступность'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='availability',
            field=models.CharField(choices=[('available', 'Доступно'), ('unavailable', 'Недоступно')], default=1, max_length=12, verbose_name='Доступность'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='BestSeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_count', models.IntegerField(verbose_name='Количество продаж')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='deliveryfood.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Хит продаж',
                'verbose_name_plural': 'Хиты продаж',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField(verbose_name='Текст отзыва')),
                ('rating', models.IntegerField(verbose_name='Рейтинг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliveryfood.product', verbose_name='Товар')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliveryfood.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Отзыв о товаре',
                'verbose_name_plural': 'Отзывы о товарах',
            },
        ),
        migrations.CreateModel(
            name='StoreReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField(verbose_name='Текст отзыва')),
                ('rating', models.IntegerField(verbose_name='Рейтинг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliveryfood.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Отзыв о магазине',
                'verbose_name_plural': 'Отзывы о магазине',
            },
        ),
    ]