from config.config import HOME_PATH, OPENAI_API_KEY
from openai import OpenAI
import sys

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_response(input_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "I'm a kitty helpful assistant."},
            {"role": "user", "content": input_text}
        ]
    )

    return response.choices[0].message.content


user_input = sys.argv[1]
response = generate_response(user_input)
f = open(HOME_PATH + "CatPrinter/app/gpt/gpt.txt", "w")
f.write(response.replace(";", ","))
f.close()
