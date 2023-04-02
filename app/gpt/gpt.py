import openai
import sys

openai.api_key = "API-KEY-HERE"


def generate_response(input_text):
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[{"role": "user", "content": input_text}]
	)

	return response.choices[0].message.content

user_input = sys.argv[1]
response = generate_response(user_input)
f = open("/home/your/path/catprinter/app/gpt/gpt.txt", "w")
f.write(response.replace(";", ","))
f.close()
