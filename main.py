import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from api import call_pokemon_api 
from rag import callRag

load_dotenv()

client = OpenAI(
    api_key='meow',
    base_url='http://localhost:8080/'
)

ask_user: bool = True

prompt = [
    {
        "role": "system",
        "content": """
        <no_think> You are a helpful assistant that answers questions about Pokemon. You can only anwswer questions in a specific JSON format.
        If you want to input what you want to say, you must use the "say" field.
        You have access to a pokemon API that you can use to answer questions better. To use it, use the "api" field.
        You also have access to a documentation specific to competitive Pokemon knowledge that you MUST use when the question is related to the competitive scene, which you can use to answer questions on competitive play. Use the "rag" field to access it.
        If you receive data from the rag that is not relevant to the question, decline the answer and say that you cannot answer the question.
        If you wish to use the API or the documentation (rag), you mustn't use the "say" field.

        Here is how the "api" field works:
        {
            "api":
                "pokemon": [List of pokemon names],
                "fields": ["field1", "field2", ...]
        }

        The "fields" array can contain any of the following fields:
        - "summary": The name of the pokemon. This will also include the height, weight, and types of the pokemon.
        - "abilities": The abilities of the pokemon
        - "stats": The stats of the pokemon
        - "evolutions": The evolutions of the pokemon
        - "moves": The moves of the pokemon

        Here is how the "rag" field works:
        {
            "rag": "query"
        }
        
        """
    }
]

def loop():
    global ask_user, prompt
    if ask_user == True:
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
        model="Qwen3",
        messages=prompt, # type: ignore
        stream=True
    ) # type: ignore

    # print("-- API THINKING --")

    # Printing this way helps with the streaming response
    response = ""
    for chunk in streamedResponse:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end='', flush=True)
    print()  # Print a newline after the response

    # print("-- END API THINKING --")

    # Remove the <think> tag from the response
    response = response.replace("<think>", "").replace("</think>", "").strip()
    
    # Parse the response as JSON
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return
    
    # Check if the response contains a "say" field
    if "say" in response_json:
        ask_user = True # Ask the user again at the next loop
        say_content = response_json["say"]
        if isinstance(say_content, str):
            print(say_content)
            # Add the assistant's response to the prompt
            prompt.append({"role": "assistant", "content": say_content})
            return
        else:
            print("Error: 'say' field is not a string.")
            return
    
    # Check if the response contains an "api" field
    if "api" in response_json:

        api_data = response_json["api"]
        if "pokemon" in api_data and isinstance(api_data["pokemon"], list):
            pokemon_list = api_data["pokemon"]
            fields = api_data.get("fields", [])
            # Call the API to get the Pokemon data
            print(f"-- CALLING POKEMON API FOR: {pokemon_list} FOR FIELDS {fields} --")
            pokemon_data = call_pokemon_api(pokemon_list, fields)
            # Add the Pokemon data to the prompt
            prompt.append({"role": "api", "content": json.dumps(pokemon_data)})
            ask_user = False  # Don't ask the user again in this loop
        else:
            print("Error: 'pokemon' field is missing or not a list in the API response.")
            return
        
    # Check if the response contains a "rag" field
    if "rag" in response_json:
        rag_data = response_json["rag"]
        if isinstance(rag_data, str):
            # Call the RAG function to get the relevant documents
            print(f"-- CALLING RAG FOR: {rag_data} --")
            rag_response = callRag(rag_data)
            print(f"-- RAG RESPONSE: {rag_response} --")
            # Add the RAG response to the prompt
            prompt.append({"role": "rag", "content": json.dumps(rag_response)})
            ask_user = False
        else:
            print("Error: 'rag' field is not a string in the response.")
            return
    


if __name__ == "__main__":
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

    ask_user = True  # Start by asking the user for input

    print("Hello! I am your Pokemon assistant. Ask me anything about Pokemon!")
    while True:
        loop()
