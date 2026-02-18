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
