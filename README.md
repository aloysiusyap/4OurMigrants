# 4OurMigrants
Backend service for the 4OurMigrants chatbot. Connected to Google Dialogflow via webhooks

The chatbot is created using Google DialogFlow and is integrated with telegram.

This backend uses the python flask framework to connect Google Dialogflow with:
1. Atlas MongoDB
2. Google BigQuery
3. Third party APIs (e.g. yelp.com)


In order to run the code, ensure you have the relevant API Keys in a .env file. 
