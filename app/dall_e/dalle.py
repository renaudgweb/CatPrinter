from openai import OpenAI
import sys
import base64
from configparser import ConfigParser

# Load configuration from a file
config = ConfigParser()
config.read('../config/config.ini')

OPENAI_API_KEY = config.get('OpenAI_api', 'OPENAI_API_KEY')
HOME_PATH = config.get('Paths', 'HOME_PATH')

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_response(input_text):
    response = client.images.generate(
        model="dall-e-2",
        prompt=input_text,
        n=1,
        size="512x512",
        response_format="b64_json"
    )

    image = response.data[0]
    imgData = base64.b64decode(image.b64_json)

    with open(f'{HOME_PATH}/app/dall_e/dalle.png', 'wb') as f:
        f.write(imgData)


user_input = sys.argv[1]
generate_response(user_input)
