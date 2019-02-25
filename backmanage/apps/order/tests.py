from django.test import TestCase

# Create your tests here.
# import datetime
#
# year = datetime.datetime.today().year
# month = datetime.datetime.today().month
# day = datetime.datetime.today().day
# date_from = datetime.datetime(year, month, day, 0, 0, 0)
# date_to = datetime.datetime(year, month, day, 23, 59, 59)

from time import strftime

time_str = strftime('%Y%m%d')
print(time_str)