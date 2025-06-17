import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key='meow',
    base_url='https://localhost:8080/'
)

prompt = [
    {
        "role": "system",
        "content": "You are a helpful assistant that answers questions about Pokemon."
    }
]

def loop():
    # Ask the user for input
    input_text = input("> ")

    # Check if the input is a command to exit
    if input_text.lower() in ["exit", "quit", "stop"]:
        print("Goodbye!")
        exit()

    # Add the user input to the prompt
    prompt.append({"role": "user", "content": input_text})

    # Call the OpenAI API to get a response
    streamedResponse = client.chat.completions.create(
        model="qwen",
        messages=prompt,
        stream=True
    )

    # Printing this way helps with the streaming response
    response = ""
    for chunk in streamedResponse:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end='', flush=True)
    print()  # Print a newline after the response

    # Add the assistant's response to the prompt
    prompt.append({"role": "assistant", "content": response})
    


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Hello, I'm bork. I'm a sausage entrepeneur, but I can also help you with Pokemon questions.\n" \
    "How can I help you?")
    while True:
        loop()

