import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key='meow',
    base_url='http://localhost:8080/'
)

prompt = [
    {
        "role": "system",
        "content": """
        <no_think> You are a helpful assistant that answers questions about Pokemon. You can only anwswer questions in a specific JSON format.
        If you want to input what you want to say, you must use the "say" field.
        You have access to a pokemon API that you can use to answer questions better. To use it, use the "api" field.

        Here is how the "api" field works:
        {
            "api":
                "pokemon": "name of the pokemon",
                "fields": ["field1", "field2", ...]
        }

        The "fields" array can contain any of the following fields:
        - "name": The name of the pokemon
        - "type": The type of the pokemon
        - "abilities": The abilities of the pokemon
        - "stats": The stats of the pokemon
        - "evolutions": The evolutions of the pokemon
        
        """
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

    print(prompt)

    # Call the OpenAI API to get a response
    streamedResponse = client.chat.completions.create(
        model="Qwen3",
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

