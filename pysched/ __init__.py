from datetime import datetime, timedelta
import calendar

""" IMPORTANT!: all dates are expected to be UTC """

# =====================================================================================
# Important facts about UTC datetime covertions:
# https://stackoverflow.com/questions/5067218/get-utc-timestamp-in-python-with-datetime
# =====================================================================================

# ==================================
# Utility methods
# ==================================
def get_week_day(date_time):
	""" all dates are expected to be UTC """
	return calendar.day_name[date_time.weekday()].lower()
	
def get_interval_in_minutes(hour_from, hour_to, max):
	total_minutes = (hour_to - hour_from) * 60
	return total_minutes/max
	
def date_object_to_date(date_object):
	""" all dates are expected to be UTC """
	return datetime(date_object['year'], date_object['month'], date_object['day'])

def get_schedule_slot(date, current_schedule):
	""" all dates are expected to be UTC """
	for slot in current_schedule:
		scheduled_date = date_object_to_date(slot['date'])
		if date == scheduled_date:
			return slot
	return None
	
def is_day_available(date, current_schedule, schedule_settings):
	""" all dates are expected to be UTC """
	now = datetime.utcnow()
	# deal with "today"
	if (now.date() == date):
		if not (now.hour > schedule_settings['fromHour'] and now.hour < schedule_settings['toHour']):
			return False
	# is this a 'good' day?
	week_day = get_week_day(date)
	if not schedule_settings['days'][week_day]:
		return False
	# see if there are existing slots available
	slot = get_schedule_slot(date, current_schedule)
	if slot is None:
		# no slot for this date..so we are good to go!
		return True
	if len(slot['items']) >= schedule_settings['max']:
		# we are maxed out!
		return False
	# if we got here that means that there is room within the given date
	return True
	
def scheduled_time_is_available(date_time, slot, datestamp_field):
	""" all dates are expected to be UTC """
	for item in slot['items']:
		if date_time == item[datestamp_field]:
			return False
	return True

def get_next_time(date, current_schedule, schedule_settings):
	""" all dates are expected to be UTC """
	now = datetime.utcnow()
	# at this point we assume that 'date' has available spots
	found = False
	interval = get_interval_in_minutes(schedule_settings['fromHour'], schedule_settings['toHour'], schedule_settings['max'])
	print 'interval is: ' + str(interval)
	slot = get_schedule_slot(date, current_schedule)
	if slot is None:
		# generate an empty slot
		slot = {
			'date': {
				'year': date.year,
				'month': date.month,
				'day': date.day
				}, 
			'items':[]
		}
	delta = schedule_settings['fromHour']*60
	next_time = date + timedelta(minutes=delta)
	while not found:
		print 'trying: ' + str(next_time)
		if scheduled_time_is_available(next_time, slot, 'scheduled_on') and next_time.hour >= schedule_settings['fromHour'] and next_time.hour <= schedule_settings['toHour'] and next_time > now:
			print 'found it!' 
			found = True
		else:
			next_time = next_time + timedelta(minutes=interval)
	return next_time
	
# ==================================
# Scheduler
# ==================================
def get_schedule_date_time(current_schedule, schedule_settings):
	""" all dates are expected to be UTC """
	now = datetime.utcnow()
	date = datetime(now.year, now.month, now.day)
	schedule_date_time = None
	while schedule_date_time is None:
		if is_day_available(date, current_schedule, schedule_settings):
			schedule_date_time = get_next_time(date, current_schedule, schedule_settings)
		date = date + timedelta(days=1)
	return schedule_date_time
