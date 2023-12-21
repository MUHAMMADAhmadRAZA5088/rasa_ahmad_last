import requests
import openai
import re

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
from typing import Any, Text, Dict, List


class DatabaseCallAction(Action):
    def name(self) -> Text:
        return "do_db_call"

    def run(self, dispatcher: 
            CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        time = tracker.get_slot("availability")
        amount = tracker.get_slot("amount")
        location = tracker.get_slot("location")

        url = 'http://127.0.0.1:5000/receive_location'  # Replace with your Flask server URL
        response = requests.post(url, json={"location":location,"amount":amount,"time":time})
        dispatcher.utter_message(text=f"Yes! These are some houses in the {location} that may match what you’re looking for …")
        flask_response = response.json()
        message_from_flask = flask_response.get("message", "No message from Flask.")
        dispatcher.utter_message(message_from_flask)
        return []
    
class LargeHhouse(Action):
    def name(self) -> Text:
        return "large_house"

    def run(self, dispatcher: 
            CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        time = tracker.get_slot("availability")
        amount = tracker.get_slot("amount")
        location = tracker.get_slot("location")

        if time and amount and location:
            url = 'http://127.0.0.1:5000//SQFT'  # Replace with your Flask server URL
            user_message = tracker.latest_message.get('text')

            value = ['k','$']
            changing = []
            for currency in value:
                if currency in user_message.lower():
                    changing.append(currency)
            if changing:
                matches = re.findall(r'(\d+[k$])', user_message.lower())
                amount = matches[-1]
                response = requests.post(url, json={"location":location,"amount":amount,"time":time})
                dispatcher.utter_message(text=f" After searching for everything this would be the largest house in LA for that budget")
                flask_response = response.json()
                message_from_flask = flask_response.get("message", "No message from Flask.")
                dispatcher.utter_message(message_from_flask)
                return {'amount':amount}

            else:
                response = requests.post(url, json={"location":location,"amount":amount,"time":time})
                dispatcher.utter_message(text=f"This house is the largest compared to the others in terms of square feet")
                flask_response = response.json()
                message_from_flask = flask_response.get("message", "No message from Flask.")
                dispatcher.utter_message(message_from_flask)
                
                
                    
        else:
           dispatcher.utter_message(text=f"First you tell me which location you want to see the plot") 
        return []
    

class Validateproperty(FormValidationAction):
    def name(self) -> Text:
        return "validate_get_availability_form"
    
    def validate_availability(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if '2023' in slot_value:
            return {"availability": slot_value}
        return {"availability": None}
    
    # def validate_amount(
    #     self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     massage = tracker.latest_message.get('text')
    #     if slot_value == "Null":
    #         return {"amount": 50}
             

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
    
    # Get user message from Rasa tracker
        user_message = tracker.latest_message.get('text')
        print(user_message)

    # def get_chatgpt_response(self, message):

        # Replace 'YOUR_API_KEY' with your actual API key
        api_key = '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'

        openai.api_key = api_key

        # Example prompt
        prompt = user_message

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens = 50 # Adjust based on your needs
            
        )

    # Extract the generated text from the response
        generated_text = response.choices[0].text
        dispatcher.utter_message(generated_text)
                # Revert user message which led to fallback.
        return [UserUtteranceReverted()]

