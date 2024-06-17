from . import jalali
from django.utils import timezone

# number converter function 
def persian_number_converter(mystr):
        """" converts english numbers to persian """
        numbers = {
            '0':'o',
            '1':'۱',
            '2':'۲',
            '3':'۳',
            '4':'۴',
            '5':'۵',
            '6':'۶',
            '7':'۷',
            '8':'۸',
            '9':'۹',
        }
        for e, p in numbers.items():
            mystr = mystr.replace (e, p)
        # this loop replace the english numbers to persian
        return mystr

# date to jalaji 
def jalali_converter(time):
    """" converts Gregorain to jalali, diplays months instead of their numbers"""
    time = timezone.localtime(time)
    # uses the server local time, specified in settings.py 
    jmonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    # this is for display each month instead of its assigned number 
    time_to_str = '{},{},{}'.format(time.year, time.month, time.day)
    time_to_list = list (jalali.Gregorian(time_to_str).persian_tuple())
    # converts the output to list because tuple is immutable and can NOT change
    for index, month in enumerate(jmonths):
        if time_to_list[1] == index+1 :
            time_to_list[1] = month
            break
    # this loop will set the first index to 1  instead of 0
    output = '{} {} {}, ساعت {}:{}'.format(
        time_to_list[2], 
        time_to_list[1],
        time_to_list[0], 
        time.hour,
        time.minute
    )
    # using string formating for displaying output in the wanted format
    return persian_number_converter(output) 