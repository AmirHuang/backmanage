from django.test import TestCase

# Create your tests here.

# import re
# #
# #
# # p = '^[A-Z]\d{5}$'
# # if not re.match(p, 'A00000'):
# #     print(22)
# # else:
# #     print(66)

from django.db.transaction import atomic

with atomic():
    try:
        a = 1 / 0
    except:
        pass