from datetime import datetime, date, timedelta
from ics import Calendar
import requests, os

from dotenv import load_dotenv



class Glenda:

    url = 'https://cloud.timeedit.net/chalmers/web/b1/ri6Qt8881n604ZQQ8QZ6t9BZ5By45038Q7B94QY6055Z1ZC5A92dDF435B5B0E7539D7C0CEB1F5.ics'
    calendar_list = list(Calendar(requests.get(url).text).timeline)

    
    @classmethod
    def structure_by_day(cls) -> list:

        """
        - Loop through list and process data (slicing, spliting, adding)
        - Storing data in individual variables
        - Structure courses into days
        - Return list: raw schedule of courses by day
        """

        calendar_list = cls.calendar_list

        class_info = []


        for event in calendar_list:
            if  "Rubrik" not in str(event.name): #Tentaanmälan and Omtenta have "Rubrik" in their name

                course_name, class_activity = str(event.name).split(". ")[1].split(", ") #Split coursename and course activity/code
                date, start_time = str(event.begin)[:-9].split("T") 
                _, end_time = str(event.end)[:-9].split("T")
                location = f"Sal: {str(event.location)}" #Add "Venue" string

                class_info.append([course_name, class_activity, date, start_time, end_time, location])

            else:
                print(str(event.name), "!!!", str(event.begin))
                tenta = str(event.name)


                print(tenta)
                print(date)
                print(start_time)





        courses = []

        for class_ in class_info: 

            if len(courses) == 0: # If first course of the day, append it inside a list for that day
                courses.append([class_])

            elif courses[-1][0][2] == class_[2]: # Append rest of course for the same day (if they share the same date) 
                courses[-1].append(class_)
            
            else:
                courses.append([class_]) # Else appends to new list representing next day


        return courses

    @classmethod
    def summarize_algorithm(cls, lesson):
            
            """
            - Processes data into more readable format
            - Translates english day name in swedish
            - Translate month index to swedish name
            
            """
            
            day_translations = {"Friday": "Fredag", "Thursday": "Torsdag", "Wednesday": "Onsdag", "Tuesday":"Tisdag", "Monday": "Måndag"}
            months = {"01": "Januari", "02": "Februari", "03": "Mars", "04": "April", "05": "Maj", "06": "Juni", "08": "Augusti", "09": "September", "10": "Oktober", "11": "November", "12": "December"}

            course_name = "Haskell" if "funktionell" in lesson[0] else "Diskret Matematik" if "Diskret" in lesson[0] else lesson[0][10:]
            activity = lesson[1][11:] if "Aktivitet" in lesson[1] else " "
            date_string = lesson[2]
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
            day_of_week = date_object.strftime("%A")
            swedish_day = day_translations[day_of_week]
            swedish_month = months[date_string[5:7]]
    


            start_h, start_m = lesson[3].split(":")
            end_h, end_m= lesson[4].split(":")
            time_interval = f"{int(start_h)+2}:{start_m}-{int(end_h)+2}:{end_m}"
            location = lesson[5]

            return date_string, swedish_day, swedish_month, time_interval, course_name, location, activity 


    @classmethod
    def summarize(cls, n=25):

        """
        - Loop through raw schedule
        - Formats string data into more readble and understandable summarized form
        - Organize into dictionary with share date as key and summary of courses as value
        - Return list of dictionaries
        """

        course_schedule = cls.structure_by_day()

        daily_summaries = []

        for lessons in course_schedule[:]:

            for ii,lesson in enumerate(lessons):

                date_string, day_of_week, month, time_interval, course_name, location, activity = cls.summarize_algorithm(lesson)
                
                summary_list = [day_of_week, month, course_name, time_interval, location, activity]

                if ii == 0:
                    daily_summaries.append({date_string:[summary_list]})
                else:
                    daily_summaries[-1][date_string].append(summary_list)


        return daily_summaries  

    @classmethod
    def get_schedule(cls, target_date):
        """ 
        - applies summarize function to schedule events
        - organizes into list of lists, by date
        """
        todays_date = target_date

        schedule_list = cls.summarize()

        summarized_schedule = []

        for schedule in schedule_list:
            for (schedule_date, day_schedule) in schedule.items():

                if schedule_date == todays_date:
                    summarized_schedule.append(schedule[schedule_date])
#                    print(schedule_date)
                    summarized_schedule.insert(0, f"{schedule_date}")

        return summarized_schedule 
                    


    @classmethod
    def summarize_schedule(cls, target_date= str(date.today())):

        """
        - Gets schedule
        - Presents it
        """

        schedule_data = cls.get_schedule(target_date)

        summarization = []

        for school_day in schedule_data[1:]:

            day_header = f"{school_day[0][0]} {schedule_data[0][8:]}e {school_day[0][1]}\n"

            summarization.append(day_header)
    
            
            for courses in school_day:                
                for course_info in courses[2:]:
                    summarization.append(course_info)

        return "\n".join(summarization)

    @classmethod
    def next_test(cls):

        """
        Return date of next test, or responds if more than 1 month away
        """

        schedule_data = cls.summarize()


        for courses in schedule_data:
            for date, day in courses.items():
                        for course in day:
                            if "Tentamen" in course:
                                return date, course
                            else:
                                return "Mer än 1 månad bort"


    @classmethod
    def get_tomorrows_schedule(cls):

        today = date.today()
        tomorrow = today + timedelta(days=1)
        str_tomorrow = str(tomorrow)

        tomorrows_schedule = cls.summarize_schedule(str_tomorrow) 

        return tomorrows_schedule



         
    @classmethod
    def kelvin_to_celsius(cls, kelvin):

        celsius = round(kelvin - 273.15, 1)

        return celsius

    @classmethod
    def get_weather_report(cls):
        load_dotenv()
        weather_token = os.getenv('WEATHER_TOKEN')
        BASE_URL = "https://api.openweathermap.org/data/3.0/weather?"
        city = 'Gothenburg'
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}"
        response = requests.get(url).json()

        current_temp = cls.kelvin_to_celsius(response['main']['temp'])
        feels_like = cls.kelvin_to_celsius(response['main']['feels_like'])
        max_temp = cls.kelvin_to_celsius(response['main']['temp_max'])
        min_temp = cls.kelvin_to_celsius(response['main']['temp_min'])
        hudimity = response['main']['humidity']
        weather_descript = response['weather'][0]['description']
        wind_speed = float(round(response['wind']['speed'],1)) #wind speed
        sunrise = response['sys']['sunrise']
        sunset = response['sys']['sunset']
        timestamp = datetime.fromtimestamp(sunset)
        sunset = timestamp.strftime('%Y-%m-%d %H:%M:%S')


        weather_data = {'vind': wind_speed, 'soluppgång':sunrise, 'solnedgång':sunset[11:-3],
                        'temperatur':current_temp, 'upplevelse':feels_like, 'max_temp':max_temp,
                        'min_temp':min_temp, 'luftfukt':hudimity, 'beskrivning':weather_descript} 

        weather_report = f"""Dagens väder: Göteborg 
        
Max/min temperatur...............{weather_data['max_temp']}C / {weather_data['min_temp']}C
Nuvar. luftfukt/vindstyrka........{weather_data['luftfukt']}% / {weather_data['vind']}m/s
Solnedgång...............................{weather_data['solnedgång']}
    """

        print (weather_report)
        return weather_report


