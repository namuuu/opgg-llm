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
    
def test_api():
    print(get_pokemon_summary("pikachu"))
    print(get_pokemon_abilities("pikachu"))
    print(get_pokemon_evolution_chain("pikachu"))
    print(get_pokemon_moves("pikachu"))
    print(get_pokemon_stats("pikachu"))