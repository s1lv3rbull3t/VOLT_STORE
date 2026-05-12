from django.db import migrations, models


def migrate_manager_to_admin(apps, schema_editor):
    User = apps.get_model('shop', 'User')
    User.objects.filter(role='manager').update(role='admin')


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_manager_to_admin, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[('buyer', 'Покупатель'), ('admin', 'Администратор')],
                default='buyer',
                max_length=20,
            ),
        ),
    ]
