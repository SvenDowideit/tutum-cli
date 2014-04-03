from tabulate import tabulate
import datetime


def tabulate_result(data_list, headers):
    print tabulate(data_list, headers, stralign="left")


def humanize_date_difference_from_now(target_datetime):
    now = datetime.datetime.utcnow()
    dt = target_datetime - datetime.datetime.utcnow()
    offset = dt.seconds + (dt.days * 60*60*24)
    delta_s = offset % 60
    offset /= 60
    delta_m = offset % 60
    offset /= 60
    delta_h = offset % 24
    offset /= 24
    delta_d = offset

    if delta_d > 1:
        if delta_d > 6:
            date = now + datetime.timedelta(days=-delta_d, hours=-delta_h, minutes=-delta_m)
            return date.strftime('%A, %Y %B %m, %H:%I')
        else:
            wday = now + datetime.timedelta(days=-delta_d)
            return wday.strftime('%A')
    if delta_d == 1:
        return "Yesterday"
    if delta_h > 0:
        return "%dh%dm ago" % (delta_h, delta_m)
    if delta_m > 0:
        return "%dm%ds ago" % (delta_m, delta_s)
    else:
        return "%ds ago" % delta_s