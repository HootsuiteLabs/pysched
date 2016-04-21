# pysched
Scheduling helper. Find the next available time slot given a set of sheduled items and predefined settings.

## Usage
```
import pysched
pysched.get_schedule_date_time(schedule, settings, datetime_field_name)
# 2016-04-21 09:00:00
```
- See conventions below for the expected structure of `schedule` and `settings`
- `datestamp_field_name` is the object property name (within the current schedule object shown below) that contains the shceduled UTC datetime for existing scheduled items.

## Conventions
1.- All dates are expected to be UTC

2.- Settings are expected to have the following format
```
{
	'max': 5,
	'fromHour': 9,
	'toHour': 17,
	'days': {
		'monday': True,	
		'tuesday': True,
		'wednesday': True,
		'thursday': True,
		'friday': True,
		'saturday': False,
		'sunday': False
	}
}
```
  - `max` is the max amount of items to be scheduled each day.
  - `fromHour` is the hour from which pysched will start sheduling items in a day.
  - `toHour`is the hour where pysched stops scheduling items in a day.
  - `days` the week days where pysched will be scheduling items for.

3.- The current scheduled items will be expected to have the following format:
```
[
	{
		'date': {
			'day': 20,
			'month': 4,
			'year': 2016
		},
		'items': [
			{'title': 'item1', 'scheduled_on': datetime(2016,4,20,9,0,0)},
			{'title': 'item2', 'scheduled_on': datetime(2016,4,20,10,0,0)},
			{'title': 'item3', 'scheduled_on': datetime(2016,4,20,11,0,0)},
			{'title': 'item4', 'scheduled_on': datetime(2016,4,20,12,0,0)}
		]
	},
	{
		'date': {
			'day': 21,
			'month': 4,
			'year': 2016
		},
		'items': [
			{'title': 'item6', 'scheduled_on': datetime(2016,4,21,10,0,0)},
			{'title': 'item7', 'scheduled_on': datetime(2016,4,21,11,0,0)},
			{'title': 'item8', 'scheduled_on': datetime(2016,4,21,12,0,0)}
		]
	}
]
```
