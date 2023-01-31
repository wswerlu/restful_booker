validauth = [
    [True, 'Auth via token'],
    [False, 'Auth via basic auth'],
]  # данные для тестов test_check_auth_in_update_booking_with_auth_token

invalidauth = [
    ['invalid_token', None, None, 'Invalid auth token'],
    [None, 'invalid_login', 'invalid_pass', 'Invalid basic auth credentials'],
]  # данные для тестов test_delete_booking_with_invalid_auth_data
