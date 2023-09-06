import json, os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator, NoAuthAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

api_key = os.environ.get('NLU_API_KEY', '')
authenticator = IAMAuthenticator(api_key) if api_key else NoAuthAuthenticator()
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator)

natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/bdec2198-6fb5-4519-b799-6911ab6b0a03')

ftrs = Features(
    entities=EntitiesOptions(sentiment=True, limit=1)
)

def analyze_text(text):
    return natural_language_understanding.analyze(text=text, features=ftrs).get_result()
