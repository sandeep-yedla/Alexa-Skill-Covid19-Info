# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests
import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Covid Info by Sandeep Yedla. I'm here to provide information about coronavirus in the US. What would you like to know?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class getusainfoHandler(AbstractRequestHandler):
    """Handler for National Cases Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("getusainfo")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        url = "https://covidtracking.com/api/v1/us/current.json";
        response = requests.get(url)
        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            speak_output = "There are {} positive cases in USA as of yesterday , {} are currently hospitalized, and {} are currently in ICU. We have lost {} people to COVID-19 so far.".format(
                parsed_json[0]["positive"], parsed_json[0]["hospitalizedCurrently"], parsed_json[0]["inIcuCurrently"], parsed_json[0]["death"],)
        else:
            speak_output = "Sorry, covid 19 API is down"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like any other information?")
                .response
        )

class getdeathinfoHandler(AbstractRequestHandler):
    """Handler for National Cases Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("getdeathinfo")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        url = "https://covidtracking.com/api/v1/us/current.json";
        response = requests.get(url)
        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            speak_output = "There have been {} deaths due to COVID-19 so far. We lost {} yesterday".format(parsed_json[0]["death"], parsed_json[0]["deathIncrease"])
        else:
            speak_output = "Sorry, covid 19 API is down"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like any other information?")
                .response
        )

class getstatesinfoHandler(AbstractRequestHandler):
    """Handler for State Cases Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("getstatesinfo")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        url = "https://covidtracking.com/api/v1/states/current.json"
        response = requests.get(url)
        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            toCheck = slots["unitedstate"].value.lower()
            us_state_abbrev = {
    'alabama': 'AL',
    'alaska': 'AK',
    'american Samoa': 'AS',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'district of Columbia': 'DC',
    'florida': 'FL',
    'georgia': 'GA',
    'guam': 'GU',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'nebraska': 'NE',
    'nevada': 'NV',
    'new hampshire': 'NH',
    'new jersey': 'NJ',
    'new mexico': 'NM',
    'new york': 'NY',
    'north carolina': 'NC',
    'north dakota': 'ND',
    'northern mariana islands':'MP',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'puerto rico': 'PR',
    'rhode island': 'RI',
    'south carolina': 'SC',
    'south dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'vermont': 'VT',
    'virgin islands': 'VI',
    'virginia': 'VA',
    'washington': 'WA',
    'west virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY'
}
            for key in us_state_abbrev:
                if toCheck == key:
                    yay = us_state_abbrev[key]
                    break
            index = -1
            for i in range(len(parsed_json)):
                if parsed_json[i]["state"] == yay:
                    index = i
                    break
            if index == -1:
                speak = "I had trouble getting COVID info about " + toCheck + "."
            else:
                speak = "{} new cases have been reported till yesterday in {}. {} are currently hospitalized and {} have died.".format(parsed_json[index]["positive"], toCheck, parsed_json[index]["hospitalizedCurrently"], parsed_json[index]["death"])
        speech = speak + " Feel free to ask me about another state."
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can get COVID-19 info from me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(getusainfoHandler())
sb.add_request_handler(getdeathinfoHandler())
sb.add_request_handler(getstatesinfoHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()



