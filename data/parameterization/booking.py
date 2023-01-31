from utils.helpers import get_booking_data

booking_data = get_booking_data()

partialupdate = [
    ['firstname', None, None, None, None, None, None, 'Update firstname'],
    [None, 'lastname', None, None, None, None, None, 'Update lastname'],
    [None, None, 'totalprice', None, None, None, None, 'Update totalprice'],
    [None, None, None, 'depositpaid', None, None, None, 'Update depositpaid'],
    [None, None, None, None, 'checkin', None, None, 'Update checkin'],
    [None, None, None, None, None, 'checkout', None, 'Update checkout'],
    [None, None, None, None, None, None, 'additionalneeds', 'Update additionalneeds'],
]  # данные для теста test_partial_update_booking_success

bookingids = [
    [None, None, None, None, None, 'Get ids without get-parameters'],
    ['firstname', None, None, None, 'Get ids with get-parameter: firstname'],
    [None, 'lastname', None, None, 'Get ids with get-parameter: lastname'],
    [None, None, 'checkin', None, 'Get ids with get-parameter: checkin'],
    [None, None, None, 'checkout', 'Get ids with get-parameter: checkout'],
    ['firstname', 'lastname', None, None, 'Get ids with get-parameters: firstname, lastname'],
    [None, None, 'checkin', 'checkout', 'Get ids with get-parameters: checkin, checkout'],
    ['firstname', 'lastname', 'checkin', 'checkout', 'Get ids with all get-parameters'],
]  # данные для теста test_get_booking_ids_success

requiredparameters = [
    [None, booking_data['lastname'], booking_data['totalprice'], booking_data['depositpaid'], booking_data['checkin'],
     booking_data['checkout'], 'Create booking without firstname'],
    [booking_data['firstname'], None, booking_data['totalprice'], booking_data['depositpaid'], booking_data['checkin'],
     booking_data['checkout'], 'Create booking without lastname'],
    [booking_data['firstname'], booking_data['lastname'], None, booking_data['depositpaid'], booking_data['checkin'],
     booking_data['checkout'], 'Create booking without totalprice'],
    [booking_data['firstname'], booking_data['lastname'], booking_data['totalprice'], None, booking_data['checkin'],
     booking_data['checkout'], 'Create booking without depositpaid'],
    [booking_data['firstname'], booking_data['lastname'], booking_data['totalprice'], booking_data['depositpaid'], None,
     booking_data['checkout'], 'Create booking without checkin'],
    [booking_data['firstname'], booking_data['lastname'], booking_data['totalprice'], booking_data['depositpaid'],
     booking_data['checkin'], None, 'Create booking without checkout'],
    [None, None, None, None, None, None, 'Create booking without all required parameters'],
]  # данные для теста test_create_booking_without_required_parameters
