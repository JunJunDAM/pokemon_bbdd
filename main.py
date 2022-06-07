# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:12:15 2022

@author: Jun
"""

import pymysql

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
        resultado = ""
        #conn=pymysql.connect(host = "localhost", port = 3306, user = "root", passwd = "admin", database = "pokemon_bbdd")
        conn=pymysql.connect(host = "localhost", port = 3308, user = "root", passwd = "", database = "pokemon_bbdd")
        cursor=conn.cursor()
        cursor.execute(f"select id from pokedex where pokemon = '{pokemon_name}'")
        for base in cursor:
            resultado = list(map(int, base))
        if len(resultado) == 0:
            return False
        else:
            return resultado[0]
    except(pymysql.err.OperationalError,pymysql.err.InternalError) as e:
        print("Error: ",e)

#GET ALL POKEMONS
def get_pokedex():
    query = "select * from pokedex"
    resultado=database(query)
    for pokemon in resultado:
        print(pokemon)
 
#GET POKEMON BY NAME
def get_pokemon():
    pokemon = input("Que pokemon quieres ver? ")
    query = (f"select * from stats where id_pokemon = (select id from pokedex where pokemon = '{pokemon}')")
    stats = database(query)
    if len(stats)==0:
        print("\n" + pokemon + " no esta en la pokedex \n")
    else: 
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
    #POKEMON DATA
    pokemon_name = input("Nombre: ")
    if exists(pokemon_name) == False:
        pokemon_type = input("Tipo: ")
        #STATS DATA
        atack = int(input("Ataque: "))
        special_atack = int(input("Ataque especial: "))
        defense = int(input("Defensa: "))
        special_defense = int(input("Defensa especial: "))
        media = (atack+special_atack+defense+special_defense)/4
        #ADD POKEMON TO POKEDEX
        new_pokemon_query = (f"insert into pokedex(pokemon,type) values ('{pokemon_name}','{pokemon_type}')")
        database(new_pokemon_query)
        #GET POKEMON ID
        pokemon_id = exists(pokemon_name)
        #ADD STATS
        new_stats_query = f"insert into stats (id_pokemon,atack,special_atack,defense,special_defense,media) values ('{pokemon_id}','{atack}','{special_atack}','{defense}','{special_defense}','{media}')"
        database(new_stats_query)
    else:
        print("\n" + pokemon_name + " ya esta registrado en la pokedex \n")
 
#DELETE POKEMON FROM DATABASE
def delete_pokemon():
    pokemon = input("Que pokemon quieres borrar? ")
    id_pokemon = exists(pokemon)
    if id_pokemon == False:
        print("\n" + pokemon + " no existe en la pokedex \n")
    else:
        query = (f"delete from pokedex where id = {id_pokemon}")
        database(query)
        print("\n" + pokemon + " ha sido eliminado de la pokedex \n")
 
#UPDATE POKEMON VALUES AND STATS
def update_pokemon():
    pokemon = input("Que pokemon quieres evolucionar? ")
    id_pokemon = exists(pokemon)
    if id_pokemon == False:
        print("\n" + pokemon + " no existe en la pokedex \n")
    else:
        evo_name = input(pokemon + " evoluciona a: ")
        query = f"update pokedex set pokemon = '{evo_name}' where id = '{id_pokemon}'"
        database(query)
        stats = database("select * from stats where id_pokemon = '{id_pokemon}'")
        print(stats)
    
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
    print("* [5] - Salir               *")
    print("*****************************")
    option = input("* Opcion: ")
    validar_option(option)

def validar_option(option):   
    if option == '0':
        get_pokedex()
    elif option == '1':
        get_pokemon()
    elif option == '2':
        create_pokemon()
    elif option == '3':
        delete_pokemon()
    elif option == '4':
        update_pokemon()
    elif option == '5':
        print("\nAdios!")
        exit()
    else: 
        print("\nOpcion incorrecta, intente nuevamente\n")
        menu()

while True:        
    menu()
