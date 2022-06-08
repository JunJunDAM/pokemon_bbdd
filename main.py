# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:12:15 2022

@author: Jun
"""

import pymysql
#database with phpMyAdmin
def database (query):
    try:
        #conn=pymysql.connect(host = "localhost", port = 3306, user = "root", passwd = "admin", database = "pokemon_bbdd")
        conn=pymysql.connect(host = "localhost", port = 3308, user = "root", passwd = "", database = "pokemon_bbdd")
        cursor=conn.cursor()
        cursor.execute(query)
        conn.commit()
        result = []
        for base in cursor:
            result.append(base)
        conn.close()
        return result
    except(pymysql.err.OperationalError,pymysql.err.InternalError) as e:
        print("Error: ",e)
        
#VERIFY IF POKEMON EXISTS AND RETURNS ID
def exists (pokemon_name):
    try:
        result = ""
        #conn=pymysql.connect(host = "localhost", port = 3306, user = "root", passwd = "admin", database = "pokemon_bbdd")
        conn=pymysql.connect(host = "localhost", port = 3308, user = "root", passwd = "", database = "pokemon_bbdd")
        cursor=conn.cursor()
        cursor.execute(f"select id from pokedex where pokemon = '{pokemon_name}'")
        for base in cursor:
            result = list(map(int, base))
        if len(result) == 0:
            return False
        else:
            return result[0]
    except(pymysql.err.OperationalError,pymysql.err.InternalError) as e:
        print("Error: ",e)

#GET ALL POKEMONS
def get_pokedex():
    query = "select * from pokedex"
    resultado=database(query)
    for pokemon in resultado:
        print(pokemon)
 
#GET POKEMON BY NAME
def get_pokemon(pokemon):
    query = (f"select * from stats where id_pokemon = (select id from pokedex where pokemon = '{pokemon}')")
    stats = database(query)
    if len(stats)==0:
        print("\n" + pokemon + " no esta en la pokedex \n")
    else: 
        #GET VALUES FROM TUPLE
        id_pokemon = stats[0][0]
        atack = stats[0][1]
        special_atack = stats[0][2]
        defense = stats[0][3]
        special_defense = stats[0][4]
        media = stats[0][5]
        print("\n" + pokemon + " ID :",id_pokemon,"\n")
        print("Ataque: ",atack , "---" + " Ataque especial: ",special_atack,"\n" + "Defensa:",defense,"---" + " Defensa especial:",special_defense,"\n")
        print("PODER DEL POKEMON:",media)

#ADD POKEMON TO DATABASE
def create_pokemon():
    import random
    pokemon_type_list = ""
    random_type = random.randint(0, 30)
    if random_type < 10:
        pokemon_type_list = "fuego"
    elif random_type >= 10 and random_type < 20:
        pokemon_type_list = "agua"
    elif random_type >= 20 and random_type <= 30:
        pokemon_type_list = "planta"
    #POKEMON DATA
    pokemon_name = input("Nombre: ")
    if exists(pokemon_name) == False:
        pokemon_type = pokemon_type_list
        #STATS DATA
        atack = random.randint(5, 100)
        special_atack = random.randint(5, 100)
        defense = random.randint(5, 100)
        special_defense = random.randint(5, 100)
         
        media = (atack+special_atack+defense+special_defense)/4
        #ADD POKEMON TO POKEDEX
        new_pokemon_query = (f"insert into pokedex(pokemon,type) values ('{pokemon_name}','{pokemon_type}')")
        database(new_pokemon_query)
        #GET POKEMON ID
        pokemon_id = exists(pokemon_name)
        #ADD STATS
        new_stats_query = f"insert into stats (id_pokemon,atack,special_atack,defense,special_defense,media) values ({pokemon_id},{atack},{special_atack},{defense},{special_defense},{media})"
        database(new_stats_query)
        get_pokemon(pokemon_name)
    else:
        print("\n" + pokemon_name + " ya esta registrado en la pokedex \n")
 
#DELETE POKEMON FROM DATABASE
def delete_pokemon(pokemon):
    id_pokemon = exists(pokemon)
    if id_pokemon == False:
        print("\n" + pokemon + " no existe en la pokedex \n")
    else:
        delete_stats_query = (f"delete from stats where id_pokemon = {id_pokemon}")
        delete_pokedex_query = (f"delete from pokedex where id = {id_pokemon}")
        database(delete_stats_query)
        database(delete_pokedex_query)
        print("\n" + pokemon + " ha sido eliminado de la pokedex \n")
 
#UPDATE POKEMON VALUES AND STATS
def update_pokemon(pokemon):
    import random
    id_pokemon = exists(pokemon)
    if id_pokemon == False:
        print("\n" + pokemon + " no existe en la pokedex \n")
    else:
        evo_name = input(pokemon + " evoluciona a: ")
        update_name_query = f"update pokedex set pokemon = '{evo_name}' where id = {id_pokemon}"
        #database(update_pokemon_query)
        stats = database(f"select * from stats where id_pokemon = {id_pokemon}")
        evo_atack = stats[0][1] + random.randint(5, 50)
        evo_special_atack = stats[0][2] + random.randint(5, 50)
        evo_defense = stats[0][3] + random.randint(5, 50)
        evo_special_defense = stats[0][4] + random.randint(5, 50)
        evo_media = (evo_atack+evo_special_atack+evo_defense+evo_special_defense)/4
        evo_stats_query = f"update stats set atack = {evo_atack}, special_atack = {evo_special_atack}, defense = {evo_defense}, special_defense = {evo_special_defense}, media = {evo_media} where id_pokemon = {id_pokemon}"
        database(update_name_query)
        database(evo_stats_query)
        print("********** EVOLUTION STATS **********")
        get_pokemon(evo_name)
        print("*************************************")
        
def figth(pokemon1,pokemon2):
    import random
    cont_pokemon1 = 0
    cont_pokemon2 = 0
    id_pokemon1 = exists(pokemon1)
    id_pokemon2 = exists(pokemon2)
    #GET MEDIA
    media_pokemon1_query = f"select media from stats where id_pokemon = {id_pokemon1}"
    media_pokemon2_query = f"select media from stats where id_pokemon = {id_pokemon2}"
    media_pokemon1 = database(media_pokemon1_query)
    media_pokemon2 = database(media_pokemon2_query)
    media_pokemon1 = media_pokemon1[0][0]
    media_pokemon2 = media_pokemon2[0][0]
    
    media_dif = abs(media_pokemon1 - media_pokemon2)
    print(media_dif)
    max_media = ""
    min_media = ""
    if media_pokemon1 > media_pokemon2:
        max_media = pokemon1
        min_media = pokemon2
    else:
        max_media = pokemon2
        min_media = pokemon1
        
    print("\n")
    print("****************************************")
    print("***** " + pokemon1 + " tiene un poder de", media_pokemon1)
    print("**************    VS    ****************")
    print("***** " + pokemon2 + " tiene un poder de", media_pokemon2)
    print("****************************************")
    print("\n")
    
    for i in range(1,4):
        if media_dif < 10:
            randomn = random.randint(0, 100)
            if randomn >= 50:
                print("Combate", i , ", Ganador: " + max_media)
                cont_pokemon1 += 1
            else:
                print("Combate", i , ", Ganador: " + min_media)
                cont_pokemon2 += 1
                
        elif media_dif >= 10 and media_dif < 30:
            randomn = random.randint(20, 100)
            if randomn >= 50:
                print("Combate", i , ", Ganador: " + max_media)
                cont_pokemon1 += 1
            else:
                print("Combate", i , ", Ganador: " + min_media)
                cont_pokemon2 += 1
                
        elif media_dif >= 30:
            randomn = random.randint(40, 100)
            if randomn >= 50:
                print("Combate", i , ", Ganador: " + max_media)
                cont_pokemon1 += 1
            else: 
                print("Combate", i , ", Ganador: " + min_media)
                cont_pokemon2 += 1
    
    print("\n",max_media, ":" , cont_pokemon1, min_media, ":", cont_pokemon2)
    if cont_pokemon1 > cont_pokemon2:
        print("\nGanador : "+ max_media)
    else:
        print("\nGanador: " + min_media)
    
def menu():
    print("\n")
    print("*****************************")
    print("********** POKEMON **********")
    print("*****************************")
    print("* [0] - Ver pokedex         *")
    print("* [1] - Ver pokemon         *")
    print("* [2] - Añadir pokemon      *")
    print("* [3] - Eliminar pokemon    *")
    print("* [4] - Evolucionar pokemon *")
    print("* [5] - Pelea pokemon       *")
    print("* [6] - Salir               *")
    print("*****************************")
    option = input("* Opcion: ")
    validar_option(option)

def validar_option(option):   
    if option == '0':
        get_pokedex()
    elif option == '1':
        pokemon = input("Que pokemon quieres ver? ")
        get_pokemon(pokemon)
    elif option == '2':
        create_pokemon()
    elif option == '3':
        pokemon = input("Que pokemon quieres borrar? ")
        delete_pokemon(pokemon)
    elif option == '4':
        pokemon = input("Que pokemon quieres evolucionar? ")
        update_pokemon(pokemon)
    elif option == '5':
        pokemon = input("Pokemon 1: ")
        pokemon2 = input("Pokemon 2: ")
        figth(pokemon,pokemon2)
    elif option == '6':
        print("\nAdios!")
        exit()
    else: 
        print("\nOpcion incorrecta, intente nuevamente\n")
        menu()

while True:        
    menu()
