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
        
def get_pokedex():
    query = "select * from pokedex"
    resultado=database(query)
    for pokemon in resultado:
        print(pokemon)
def get_pokemon():
    pokemon = input("Que pokemon quieres ver? ")
    query = (f"select * from stats where id_pokemon = (select id from pokedex where pokemon = '{pokemon}')")
    resultado = database(query)
    if len(resultado)==0:
        print("No esta ese pokemon en la bbdd")
    else: 
        print(resultado)
def create_pokemon():
    pokemon_name = input("Nombre: ")
    pokemon_type = input("Tipo: ")
    new_pokemon_query = (f"insert into pokedex(pokemon,type) values ('{pokemon_name}','{pokemon_type}')")
    database(new_pokemon_query)
    pokemon_id = f"select id from pokedex where pokemon = '{pokemon_name}'"
    print(database(pokemon_id))

    atack = int(input("Ataque: "))
    special_atack = int(input("Ataque especial: "))
    defense = int(input("Defensa: "))
    special_defense = int(input("Defensa especial: "))
    media = sum(atack,special_atack,defense,special_defense)/4
    new_stats_query = f"insert into stats (pokemon_id,atack,special_atack,defense,special_defense,media) values ('{pokemon_id}','{atack}','{special_atack}','{defense}','{special_defense}','{media}')"
    database(new_stats_query)
def delete_pokemon():
    query = ""
def update_pokemon():
    query = ""
    
def menu():
    
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
