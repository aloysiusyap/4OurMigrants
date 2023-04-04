import pandas as pd
import datetime
from pandas.io import gbq

def convertDate(d):
    d = d.split("+")[0]
    new_date = datetime.datetime.strptime(d,"%Y-%m-%dT%H:%M:%S")
    return new_date.date()

class Search:
    def __init__(self, sport, date) -> None:
        self.sport = sport
        self.date = convertDate(date)

    def search_game(self):
        query = f"SELECT * FROM `ourmigrants-381919.game_schedules.schedule` WHERE SPORT = '{self.sport}' AND DATE = '{self.date}' LIMIT 3"
        df = gbq.read_gbq(query, project_id = "ourmigrants-381919")
        
        if not df.empty:
            data = df.to_dict('index')
            webhook_response = "*** List of available Games ***\n"
            for k, v in data.items():
                organiser = v['Organiser']
                contact = v['Contact']
                sport = v['Sport']
                location = v['Location']
                date = v['Date']
                time = v['Time']

                webhook_response += f"Sport:\t {sport} \n"
                webhook_response += f"Date:\t {date} \n"
                webhook_response += f"Time:\t {time} \n"
                webhook_response += f"Location:\t {location} \n"
                webhook_response += f"Contact:\t {contact} \n\n"
        else:
            webhook_response = "No matching games. Try searching for another game or time. Alternatively you can create your own game!"

        return webhook_response