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
