from datetime import date

def age_verification(birthday):
	today = date.today()
	year_diff = today.year - birthday.year

	if year_diff < 13:
		print("less than 13 years")
		return False

	else:
		month_diff = today.month - birthday.month
		if month_diff < 0:
			print("turning 13 this year")
			return False
		else:
			day_diff = today.day - birthday.day 
			if day_diff < 0:
				print("turning 13 this month")
				return False
			else:
				return True


birthday = date.fromisoformat('2007-12-13')
print(birthday.day)
print(date.today().day)
age_verification(birthday)

if not age_verification(birthday):
	print("you are not 13!!")
	print("you are not 13!!")
	print("you are not 13!!")
else:
	print("you are 13!!")
	print("you are 13!!")
	print("you are 13!!")

