from ..models import Letting, Address


def get_letting():
    address = Address.objects.create(
        number=10,
        street="avenue des champs élysées",
        city="Paris",
        state=75,
        zip_code=75008,
        country_iso_code="FRA"
    )
    letting = Letting.objects.create(
        title='title_test',
        address=address
    )
    return letting, address
