from datetime import date, timedelta

d = [date(2010, 2, 23), date(2010, 2, 24), date(2010, 2, 25),
         date(2010, 2, 26), date(2010, 3, 1), date(2010, 3, 2)]
date_set = set(d[0] + timedelta(x) for x in range((d[-1] - d[0]).days))
missing = sorted(date_set - set(d))
print(missing)
