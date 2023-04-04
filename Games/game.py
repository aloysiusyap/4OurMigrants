import pandas as pd
import datetime

def convertDate(d):
    d = d.split("+")[0]
    new_date = datetime.datetime.strptime(d,"%Y-%m-%dT%H:%M:%S")
    return new_date.date()

class Game:
    def __init__(self, organiser, contact, sport, location, date, time) -> None:
        self.organiser = organiser
        self.contact = contact
        self.sport = sport
        self.location = location
        self.date = date
        self.time = time

    def broadcastGame(self):
        new_dict = {'Organiser':self.organiser, 'Contact':self.contact, 'Sport':self.sport, 'Location':self.location, 'Date':self.date, 'Time':self.time}
        new_game = pd.DataFrame(data=[new_dict])
        new_game['Date'] = new_game['Date'].apply(convertDate)
        new_game.to_gbq(destination_table='ourmigrants-381919.game_schedules.schedule', project_id='ourmigrants-381919', if_exists='append')

    def gameDetails(self):
        output = f"Sport:\t {self.sport} \n"
        output += f"Date:\t {self.date} \n"
        output += f"Time:\t {self.time} \n"
        output += f"Location:\t {self.location} \n"
        output += f"Contact:\t {self.contact} \n\n"
        return output
    