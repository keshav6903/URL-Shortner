# # TODO: Implement utility functions here
# # Consider functions for:
# # - Generating short codes
# # - Validating URLs
# # - Any other helper functions you need


import string
import random
import validators

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def validate_url(url):
    return validators.url(url) is True