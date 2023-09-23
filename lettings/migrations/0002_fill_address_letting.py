from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oc_lettings_site', '0001_initial'),
        ('lettings', '0001_initial')
    ]

    operations = [
        migrations.RunSQL(
            '''
            -- SQL statements to copy data from the original table to the new table in the new app
            INSERT INTO lettings_Address (id, number, street, city, state, zip_code, country_iso_code)
            SELECT id, number, street, city, state, zip_code, country_iso_code
            FROM oc_lettings_site_address;
            ''',
        ),
        migrations.RunSQL(
            '''
            -- SQL statements to copy data from the original table to the new table in the new app
            INSERT INTO lettings_letting (id, title, address_id)
            SELECT id, title, address_id
            FROM oc_lettings_site_letting;
            '''
        ),
    ]