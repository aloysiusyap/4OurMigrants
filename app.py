import os
import json
from pymongo import MongoClient 
from pandas.io import gbq
from flask import Flask, request, make_response
from dotenv import load_dotenv

from Conversations import conversations
from DataRequests import yelp, visitsingapore
from Games import game, search

load_dotenv()

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    sessionID = req.get("responseId")
    result = req.get("queryResult")
    intent = result.get("intent").get("displayName")

    # creating new group for sports
    if intent == "Default Welcome Intent - Play Sports - Create Group":
        parameters = result.get("parameters")
        name = parameters.get("name")
        contact = parameters.get("contact")
        sport = parameters.get("sport")
        date = parameters.get("date")
        # time = parameters.get("time") ## changing time to string because join game only offers date and sport 

        output = result.get("outputContexts")[0]
        location = output.get("parameters").get("location.original")
        time = output.get("parameters").get("time.original")

        new_game = game.Game(name, contact, sport, location, date, time)
        new_game.broadcastGame()
        return response(webhook_response="Game has been broadCasted!", text="")
    
    # joining an existing group for sports 
    if intent == "Default Welcome Intent - Play Sports - Join Group":
        parameters = result.get("parameters")
        sport = parameters.get("sports")
        date = parameters.get("date")

        results = search.Search(sport, date)
        webhook_response = results.search_game()
        
        return response(webhook_response=webhook_response, text = "")

    # save user's input if input does not match any intents
    if intent == "Default Fallback Intent":
        log = conversations.Log()
        query_text = result.get("queryText")
        fulfillment_text = result.get("fulfillmentText")
        db = configureDataBase()

        log.saveConversations(sessionID, query_text, fulfillment_text, intent, db)
        return response(fulfillment_text, '')

    if intent == "Default Fallback Intent":
        event = visitsingapore.SearchEvents().search_events(searchType='Keyword', searchValues='arts')
        return event

def configureDataBase():
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    client = MongoClient(f"mongodb+srv://{username}:{password}@4ourmigrant.kyc4ohq.mongodb.net/?retryWrites=true&w=majority")
    return client.get_database('4OurMigrant')

def response(webhook_response, text):
    return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            webhook_response
                        ]

                    }
                },
                {
                    "text": {
                        "text": [
                            text
                        ]

                    }
                }
            ]
        }



if __name__ == '__main__':
    app.run(debug=False, port=5001)