class Date: pass

names = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
'Sep', 'Oct', 'Nov', 'Dec' ]

short = ['Sep', 'Apr', 'Jun', 'Nov']

months = {}
for name in names:
    if name == 'Feb':
        months[name] = 28
    elif name in short:
        months[name] = 30
    else:
        months[name] = 31

lengths = [length for (name, length) in months.items()]
print lengths

def cumulative_sum(t):
    u = []
    total = 0
    for x in t:
        total += x
        u.append(total)
    return u

roll = [0] + cumulative_sum(lengths)
print roll

def make_date(day=1, month=1, year=2000):
    date = Date()
    date.day = day
    date.month = month
    date.year = year
    return date

def print_date(d):
    print '%d/%d/%d' % (d.month, d.day, d.year)

def print_date_european(d):
    print '%d/%d/%d' % (d.day, d.month, d.year)

def days_since_2000(d):
    days = (d.year - 2000) * 365
    days += roll[d.month-1]
    days += d.day - 1
    return days

today = make_date(2, 12, 2004)
print_date(today)
print days_since_2000(today)

