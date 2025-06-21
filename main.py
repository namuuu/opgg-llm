import os
from dotenv import load_dotenv
import json

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
                "pokemon": [List of pokemon names],
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

    print("-- DEBUG --")

    # Printing this way helps with the streaming response
    response = ""
    for chunk in streamedResponse:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end='', flush=True)
    print()  # Print a newline after the response

    print("-- END DEBUG --")

    # Check if the response is in the correct JSON format
    if not response.startswith("{") or not response.endswith("}"):
        print("Error: Response is not in the correct JSON format.")
        return
    
    # Parse the response as JSON
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return
    
    # Check if the response contains an "api" field
    if "api" in response_json:
        api_data = response_json["api"]
        if "pokemon" in api_data and isinstance(api_data["pokemon"], list):
            pokemon_list = api_data["pokemon"]
            fields = api_data.get("fields", [])
            print(f"Fetching data for Pokemon: {', '.join(pokemon_list)} with fields: {', '.join(fields)}")
            # Here you would typically call the actual API to fetch the data
            # For now, we will just simulate it
            print("Simulated API response: [Pokemon data would be here]")

    # Add the assistant's response to the prompt
    prompt.append({"role": "assistant", "content": response})
    


if __name__ == "__main__":
    loop()
