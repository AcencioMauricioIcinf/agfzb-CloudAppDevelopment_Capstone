import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

authenticator = IAMAuthenticator('hpuzF87CSyiErL57hkWAmnmtc0-nvd62R8uxwIFQgT54')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator)

natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/bdec2198-6fb5-4519-b799-6911ab6b0a03')

ftrs = Features(
    entities=EntitiesOptions(sentiment=True, limit=1)
)

def analyze_text(text):
    return natural_language_understanding.analyze(text=text, features=ftrs).get_result()
