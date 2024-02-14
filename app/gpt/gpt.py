from openai import OpenAI
import sys
from configparser import ConfigParser

# Load configuration from a file
config = ConfigParser()
config.read('../config/config.ini')

OPENAI_API_KEY = config.get('OpenAI_api', 'OPENAI_API_KEY')
HOME_PATH = config.get('Paths', 'HOME_PATH')

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_response(input_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "I'm a kitty helpful assistant."},
            {"role": "user", "content": input_text}
        ]
    )

    return response.choices[0].message.content


user_input = sys.argv[1]
response = generate_response(user_input)
f = open(f'{HOME_PATH}/app/gpt/gpt.txt', 'w')
f.write(response.replace(";", ","))
f.close()
