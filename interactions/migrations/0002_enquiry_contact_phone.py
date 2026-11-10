from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='contact_phone',
            field=models.CharField(
                default='',
                help_text='Phone number where the landlord can reach you.',
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]
