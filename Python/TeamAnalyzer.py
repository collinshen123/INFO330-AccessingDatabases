import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")

    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # try:
    #     pokedex_num = int(arg)
    # except ValueError:
    #     print(f"Error: Invalid pokedex number {arg}")
    #     sys.exit()
    # Analyze the pokemon whose pokedex_number is in "arg"
    conn = sqlite3.connect('pokemon.sqlite')
    c = conn.cursor()
    
        
    # You will need to write the SQL, extract the results, and compare

    # find curr pokemon name
    query = """
    SELECT *
    FROM pokemon
    WHERE pokedex_number = ?
    """
    c.execute(query, (arg,))
    name_result = c.fetchone()
    pokemon_name = name_result[2]
    # print (name_result[2])

    # find curr pokemon types
    query_1 = """
    SELECT *
    FROM pokemon_types_view
    WHERE name = ?
    """
    c.execute(query_1, (pokemon_name,))
    types_result = c.fetchone()
    pokemon_types = (types_result[1], types_result[2])
    # print(pokemon_types)

    # find curr pokemon type id
    query_2 = """
    SELECT *
    FROM type
    WHERE name = ?
    """
    c.execute(query_2, (pokemon_types[0],))
    types_1 = c.fetchone()
    c.execute(query_2, (pokemon_types[1],))
    types_2 = c.fetchone()


    type_1_id = types_1[0]
    type_2_id = types_2[0]
    # print(type_1_id)
    # print(type_2_id)

    # find curr pokemon weaknesses
    query_3 = """
    SELECT *
    FROM against
    WHERE type_source_id1 = ? and type_source_id2 = ?
    """
    c.execute(query_3, (type_1_id, type_2_id))
    against_result = c.fetchone()

    new_against_result = against_result[2:]

    against_map = {}
    for against, nums in zip(types, new_against_result):
            against_map[against] = nums
            
    # print (against_result)

    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    strengths = []
    weaknesses = []
    for against in against_map.keys():
        if against_map[against] > 1:
            strengths.append(against)
        elif against_map[against] < 1:
            weaknesses.append(against)
    
    # Store the analysis in a dictionary
    
    # print(pokemon_name)
    # print(pokemon_types)
    # print(strengths)
    # print(weaknesses)

    # team[arg] = {'name': pokemon_name, 'types': pokemon_types, 'strengths': strengths, 'weaknesses': weaknesses}

    print(f"Analyzing {arg}")
    print(f"{pokemon_name} ({pokemon_types[0]}{' ' + pokemon_types[1] if pokemon_types[1] else ''}) is strong against {strengths} but weak against {weaknesses}")
    conn.close()
    


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")