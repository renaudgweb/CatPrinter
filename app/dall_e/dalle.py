from openai import OpenAI
import sys
import base64

client = OpenAI(api_key="API-KEY-HERE")


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

    with open("/home/your/path/catprinter/app/dall_e/dalle.png", 'wb') as f:
        f.write(imgData)


user_input = sys.argv[1]
generate_response(user_input)
