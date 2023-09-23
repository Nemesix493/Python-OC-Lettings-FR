from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oc_lettings_site', '0001_initial'),
        ('profiles', '0001_initial')
    ]

    operations = [
        migrations.RunSQL(
            '''
            -- SQL statements to copy data from the original table to the new table in the new app
            INSERT INTO profiles_profile (id, user_id, favorite_city)
            SELECT id, user_id, favorite_city
            FROM oc_lettings_site_profile;
            ''',
        ),
    ]