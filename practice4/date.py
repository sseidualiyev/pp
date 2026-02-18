from datetime import datetime, timedelta
current_date = datetime.now()
new_date = current_date - timedelta(days=5)
print(new_date)

from datetime import datetime, timedelta
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

from datetime import datetime
now = datetime.now().replace(microsecond=0)
print(now)

from datetime import datetime
date1_str = input()
date2_str = input()
date1 = datetime.fromisoformat(date1_str)
date2 = datetime.fromisoformat(date2_str)
difference_seconds = abs((date2 - date1).total_seconds())
print(int(difference_seconds))
