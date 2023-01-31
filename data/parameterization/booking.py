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
