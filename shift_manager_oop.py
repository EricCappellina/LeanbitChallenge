################
#    IMPORT    #
################

import json
from datetime import datetime, timedelta


###############
#    CLASS    #
###############
class Tractus:
    def __init__(self, input_data_file_path, italian_holidays):
        """
        initialization function for the Tractus class, which takes as inputs the input file path and
        a list in which all the italian national holidays are stored in string format.
        The initialization consists in reading the input file data and transform the italian national holidays
        in datetime format
        """
        self.input_data_file_path = input_data_file_path
        self.italian_holidays = [datetime.strptime(date, "%Y-%m-%d") for date in italian_holidays]

        json_file = open(self.input_data_file_path)
        self.data = json.load(json_file)

        # Initialize the list to store availability data
        self.availabilities = []

        self.output_data = None

    def calculate_workdays_and_holidays(self, since, until):
        """function that takes as inputs:
        since: beginning date in string format
        until: ending date in string format

        and the output will be the number of workdays, weekend days and holidays
        """
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

    def is_local_holiday_a_workday(self, since, until, local_holiday):
        """
        Function that takes as inputs:
        since: beginning date in string format
        until: ending date in string format
        local_holiday: date in which the local holiday takes place

        The output will be a boolean value: True if the local holiday corresponds to a workday else False
        """
        since_date = datetime.strptime(since, "%Y-%m-%d")
        until_date = datetime.strptime(until, "%Y-%m-%d")
        local_holiday_date = datetime.strptime(local_holiday, "%Y-%m-%d")

        if (since_date <= local_holiday_date <= until_date) & \
                (local_holiday_date.weekday() < 5) & \
                (local_holiday_date not in self.italian_holidays):
            return True

        return False

    def is_birthday_a_workday(self, since, until, birthday):
        """
        Function that takes as inputs:
        since: beginning date in string format
        until: ending date in string format
        birthday: date in which the birthday is celebrated

        The output will be a boolean value: True if the birthday corresponds to a workday else False
        """
        since_date = datetime.strptime(since, "%Y-%m-%d")
        until_date = datetime.strptime(until, "%Y-%m-%d")
        birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
        birthday_date = birthday_date.replace(year=since_date.year)

        if (since_date <= birthday_date <= until_date) & \
                (birthday_date.weekday() < 5) & \
                (birthday_date not in self.italian_holidays):
            return True

        return False

    def fill_availabilities(self):
        """
        function that is responsible for writing, for each developer, all the workdays, weekend days and holidays
        given the period (with the help of 3 functions previously defined:
                          is_local_holiday_a_workday
                          is_birthday_a_workday
                          calculate_workdays_and_holidays)
        """
        for period in self.data['periods']:

            for developer in self.data['developers']:
                workdays, weekend_days, holidays = self.calculate_workdays_and_holidays(period['since'],
                                                                                        period['until'])

                birthday_bool = self.is_birthday_a_workday(period['since'], period['until'], developer['birthday'])

                # adjust the number of workdays and holidays
                workdays -= int(birthday_bool)
                holidays += int(birthday_bool)

                for local_holiday in self.data['local_holidays']:
                    local_holiday_bool = self.is_local_holiday_a_workday(period['since'], period['until'],
                                                                         local_holiday['day'])
                    # adjust the number of workdays and holidays
                    workdays -= int(local_holiday_bool)
                    holidays += int(local_holiday_bool)

                total_days = (datetime.strptime(period['until'], "%Y-%m-%d") -
                              datetime.strptime(period['since'], "%Y-%m-%d")).days + 1
                availability = {
                    'developer_id': developer['id'],
                    'period_id': period['id'],
                    'total_days': total_days,
                    'workdays': workdays,
                    'weekend_days': weekend_days,
                    'holidays': holidays,
                }
                self.availabilities.append(availability)

    def create_output_file(self, output_file_path):
        """function that takes as input the output file path.
           The output will be the creation of the json file in the specified folder path
        """
        # Create output.json
        self.output_data = {'availabilities': self.availabilities}
        with open(output_file_path, 'w') as output_file:
            json.dump(self.output_data, output_file, indent=2)
        print('The JSON output file has been generated successfully')
