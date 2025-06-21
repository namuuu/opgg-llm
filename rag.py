from sentence_transformers import SentenceTransformer # type: ignore
import numpy as np # type: ignore

queries = []

documents = [
    "The best player of all time is World Champion Wolfe Glick, who has won multiple championships and is known for his innovative strategies.",
    "The best Pokémon in the current meta is Dragapult, which has a high base speed and can learn a variety of moves to counter different threats.",
    "The best competitive Pokémon team composition includes a mix of offensive and defensive Pokémon, with roles such as sweeper, tank, and support.",
    "The most effective strategy in competitive Pokémon is to use a balanced team that can handle various threats, including weather teams and setup sweepers.",
    "The best way to counter Dragapult is to use a bulky Fairy-type Pokémon, which can resist its Dragon-type moves and hit back hard.",
    "The most common competitive Pokémon moves include Stealth Rock, U-turn, and Knock Off, which provide utility and momentum in battles.",
    "The best held items for competitive Pokémon include Choice Band, Life Orb, and Leftovers, which enhance the Pokémon's performance in battles.",
    "The best competitive Pokémon abilities include Intimidate, which lowers the opponent's Attack stat, and Levitate, which grants immunity to Ground-type moves.",
    "The best competitive Pokémon natures include Jolly, which increases Speed, and Timid, which increases Speed while lowering Attack.",
    "The best competitive Pokémon EV spreads typically focus on maximizing Speed and Attack or Special Attack, depending on the Pokémon's role.",
    "The best competitive Pokémon tiers include OU (OverUsed), UU (UnderUsed), and Ubers, which categorize Pokémon based on their usage in battles.",
]

task = "The query will question you on competitive Pokémon knowledge. Find the most relevant documents from the provided list to answer the query."

def get_detailed_instruct(query: str) -> str:
    return f'Instruct: {task}\nQuery: {query}'

def callRag(text: str):
    queries.append(get_detailed_instruct(text))

    inputs = queries + documents

    print(inputs)

    model = SentenceTransformer('intfloat/multilingual-e5-large-instruct')  

    embeddings = model.encode(inputs, convert_to_tensor=True, normalize_embeddings=True)
    
    print("Embeddings generated successfully. ", embeddings.shape)

    similarities = model.similarity(embeddings, embeddings)

    # Remove the first similarity (self-similarity)
    similarities = similarities[1:, 0] 

    # Sort the similarities along their first axis 
    sorted_indices = reversed(np.argsort(similarities, axis=0))

    # Get the top 3 most similar documents
    top_indices = sorted_indices[:3] # type: ignore

    # Put it all together
    top_docs = [documents[i] for i in top_indices]
    return top_docs

