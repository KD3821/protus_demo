# Generated by Django 4.2.10 on 2024-05-13 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthLoginSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_id', models.IntegerField(blank=True, null=True, verbose_name='ID токена')),
                ('session_id', models.CharField(max_length=30, verbose_name='ID сессии')),
                ('confirmation_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='ID подтверждения')),
                ('user_uuid', models.CharField(blank=True, max_length=50, null=True, verbose_name='PROTUS uuid')),
                ('expire_date', models.DateTimeField(verbose_name='Действительна до')),
                ('finalized_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата авторизации')),
                ('is_finalized', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Protus LoginSession',
                'verbose_name_plural': 'Protus LoginSessions',
            },
        ),
        migrations.CreateModel(
            name='ProtusAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_uuid', models.CharField(max_length=50, verbose_name='PROTUS uuid')),
                ('token', models.CharField(max_length=300, verbose_name='PROTUS Access')),
                ('expires_at', models.DateTimeField(verbose_name='Годен до')),
                ('scope', models.CharField(max_length=100, verbose_name='Scope')),
            ],
            options={
                'verbose_name': 'AccessToken',
                'verbose_name_plural': 'AccessTokens',
            },
        ),
        migrations.CreateModel(
            name='ProtusPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_uuid', models.CharField(max_length=50, verbose_name='ID платежа')),
                ('user_uuid', models.CharField(max_length=50, verbose_name='PROTUS uuid')),
                ('service_id', models.CharField(max_length=50, verbose_name='ID услуги')),
                ('service_name', models.CharField(max_length=100, verbose_name='Название услуги')),
                ('invoice_number', models.CharField(max_length=50, verbose_name='Номер инвойса')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Сумма')),
                ('status', models.CharField(choices=[('initialized', 'в обработке'), ('succeeded', 'оплачен'), ('failed', 'отклонен')], default='initialized', max_length=15, verbose_name='Статус платежа')),
                ('payload', models.JSONField(blank=True, null=True, verbose_name='Payload')),
                ('initialized_at', models.DateTimeField(verbose_name='Время инициализации')),
                ('finalized_at', models.DateTimeField(blank=True, null=True, verbose_name='Время оплаты')),
                ('protus_note', models.CharField(blank=True, max_length=100, null=True, verbose_name='Пометка PROTUS')),
            ],
            options={
                'verbose_name': 'Protus Платеж',
                'verbose_name_plural': 'Protus Платежи',
            },
        ),
        migrations.CreateModel(
            name='ProtusRefreshToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_uuid', models.CharField(max_length=50, verbose_name='PROTUS uuid')),
                ('token', models.CharField(max_length=300, verbose_name='PROTUS Refresh')),
                ('revoked', models.BooleanField(default=False)),
                ('access_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refresh', to='protus.protusaccesstoken', verbose_name='Access')),
            ],
            options={
                'verbose_name': 'RefreshToken',
                'verbose_name_plural': 'RefreshTokens',
            },
        ),
    ]
