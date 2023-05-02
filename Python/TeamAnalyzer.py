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

    try:
        pokedex_num = int(arg)
    except ValueError:
        print(f"Error: Invalid pokedex number {arg}")
        sys.exit()
    # Analyze the pokemon whose pokedex_number is in "arg"
    conn = sqlite3.connect('pokemon.sqlite')
    c = conn.cursor()

    # find curr pokemon name
    query = """
    SELECT *
    FROM pokemon
    WHERE pokedex_number = ?
    """
    c.execute(query, (arg,))
    name_result = c.fetchone()
    pokemon_name = name_result[2]

    # find curr pokemon types
    query_1 = """
    SELECT *
    FROM pokemon_types_view
    WHERE name = ?
    """
    c.execute(query_1, (pokemon_name,))
    types_result = c.fetchone()
    pokemon_types = (types_result[1], types_result[2])

    # find curr pokemon type id
    query_2 = """
    SELECT *
    FROM pokemon_types_battle_view
    WHERE type1name = ? and type2name = ?
    """
    c.execute(query_2, (pokemon_types[0],pokemon_types[1]))
    against_result = c.fetchone()
    

   
    


    # create new list without type id's
    new_against_result = against_result[2:]

    # Store the analysis in a dictionary
    against_map = {}
    for against, nums in zip(types, new_against_result):
            against_map[against] = nums



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
    

    # printing
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