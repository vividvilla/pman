import re


def is_valid_name(name):
	regex = re.compile(r"^(?!_$)(?![-])(?!.*[_-]{2})[a-z0-9_-]+(?<![-])$", re.X)
	if not re.match(regex, name):
		return False
	return True
