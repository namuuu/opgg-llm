import pokebase as pb



def get_pokemon_summary(pokemon_name):
    try:
        pokemon = pb.pokemon(pokemon_name)
        return {
            "name": pokemon.name,
            "height": pokemon.height,
            "weight": pokemon.weight,
            "types": [type.type.name for type in pokemon.types]
        }
    except Exception as e:
        return {"error": str(e)}

def get_pokemon_abilities(pokemon_name):
    try:
        pokemon = pb.pokemon(pokemon_name)
        abilities = [ability.ability.name for ability in pokemon.abilities]
        return {"abilities": abilities}
    except Exception as e:
        return {"error": str(e)}
    
def get_pokemon_evolution_chain(pokemon_name):
    try:
        pokemon = pb.pokemon(pokemon_name)
        species = pb.pokemon_species(pokemon.species.name)
        evolution_chain = pb.evolution_chain(species.evolution_chain.id)
        
        chain = []
        current = evolution_chain.chain
        while current:
            chain.append(current.species.name)
            current = current.evolves_to[0] if current.evolves_to else None
        
        return {"evolution_chain": chain}
    except Exception as e:
        return {"error": str(e)}
    
def get_pokemon_moves(pokemon_name):
    try:
        pokemon = pb.pokemon(pokemon_name)
        moves = [move.move.name for move in pokemon.moves]
        return {"moves": moves}
    except Exception as e:
        return {"error": str(e)}
    
def get_pokemon_stats(pokemon_name):
    try:
        pokemon = pb.pokemon(pokemon_name)
        stats = {stat.stat.name: stat.base_stat for stat in pokemon.stats}
        return {"stats": stats}
    except Exception as e:
        return {"error": str(e)}
    
def call_pokemon_api(pokemon_list, fields):
    """
    Fetches data for a list of Pokemon with specified fields.
    
    Args:
        pokemon_list (list): List of Pokemon names.
        fields (list): List of fields to fetch for each Pokemon.
        
    Returns:
        dict: A dictionary containing the requested data for each Pokemon.
    """

    results = {}
    for pokemon_name in pokemon_list:
        pokemon_name = pokemon_name.lower()
        results[pokemon_name] = {}
        if "name" in fields or "type" in fields or "summary" in fields:
            results[pokemon_name] = get_pokemon_summary(pokemon_name)
        if "abilities" in fields:
            results[pokemon_name]["abilities"] = get_pokemon_abilities(pokemon_name)
        if "evolutions" in fields:
            results[pokemon_name]["evolution_chain"] = get_pokemon_evolution_chain(pokemon_name)
        if "moves" in fields:
            results[pokemon_name]["moves"] = get_pokemon_moves(pokemon_name)
        if "stats" in fields:
            results[pokemon_name]["stats"] = get_pokemon_stats(pokemon_name)
    
    return results
    

if __name__ == "__main__":
    print(call_pokemon_api(["charizard"], ["abilities"]))