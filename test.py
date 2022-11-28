from datetime import datetime

date_time_str = '180919 015519'

date_time_obj = datetime.strptime(date_time_str, r'%d/%m/%y %H:%M:%S')


print("The type of the date is now",  type(date_time_obj))
print("The date is", date_time_obj)
