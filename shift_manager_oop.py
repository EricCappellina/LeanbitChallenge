import json
from datetime import datetime, timedelta


class ShiftManager:
    def __init__(self, input_data_file_path, italian_holidays):
        self.input_data_file_path = input_data_file_path
        self.italian_holidays = [datetime.strptime(date, "%Y-%m-%d") for date in italian_holidays]

        json_file = open(self.input_data_file_path)
        self.data = json.load(json_file)

        # Initialize the list to store availability data
        self.availabilities = []

        self.output_data = None

    # Function to calculate workdays and holidays in a date range
    def calculate_workdays_and_holidays(self, since, until):
        workdays = 0
        weekend_days = 0
        holidays = 0

        current_date = datetime.strptime(since, "%Y-%m-%d")
        until_date = datetime.strptime(until, "%Y-%m-%d")

        while current_date <= until_date:
            # Check if the current date is a weekend (Saturday or Sunday)
            if current_date.weekday() >= 5:
                weekend_days += 1
            else:
                # Check if the current date is a holiday in Italy else is a workday
                if current_date in self.italian_holidays:
                    holidays += 1
                else:
                    workdays += 1

            # Move to the next day
            current_date += timedelta(days=1)

        return workdays, weekend_days, holidays

    def fill_availabilities(self):
        for period in self.data['periods']:
            workdays, weekend_days, holidays = self.calculate_workdays_and_holidays(period['since'], period['until'])
            total_days = (datetime.strptime(period['until'], "%Y-%m-%d") -
                          datetime.strptime(period['since'], "%Y-%m-%d")).days + 1
            availability = {
                'period_id': period['id'],
                'total_days': total_days,
                'workdays': workdays,
                'weekend_days': weekend_days,
                'holidays': holidays,
            }
            self.availabilities.append(availability)

        # Create output.json
        self.output_data = {'availabilities': self.availabilities}
        with open(r'C:\Users\denis\OneDrive\Documenti\GitHub\ruby-challenge\level1\my_output.json', 'w') as output_file:
            json.dump(self.output_data, output_file, indent=2)
