# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:12:15 2022

@author: Jun
"""

import pymysql

def database (query):
    try:
        conn=pymysql.connect(host = "localhost", port = 3308, user = "root", passwd = "", database = "pokemon_bbdd")
        cursor=conn.cursor()
        cursor.execute(query)
        conn.commit()
        for base in cursor:
            print(base)
        conn.close()
        
    except(pymysql.err.OperationalError,pymysql.err.InternalError) as e:
        print("Error: ",e)
        
def get_pokedex():
    query = "select * from pokedex"
    database(query)
def get_pokemon():
    pokemon = input("Que pokemon quieres ver? ")
    query = f"select * from stats where id_pokemon = select id from pokedex where pokemon = '{pokemon}'"
    database(query)
def create_pokemon():
    query = ""
def delete_pokemon():
    query = ""
def update_pokemon():
    query = ""
    
def menu():
    while True:
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
        option = int(input("* Opcion: "))
        if option == 0:
            get_pokedex()
        elif option == 1:
            get_pokemon()
        elif option == 2:
            create_pokemon()
        elif option == 3:
            delete_pokemon()
        elif option == 4:
            update_pokemon()
        elif option == 5:
            break
        else:
            print("Opcion no valida")
        
menu()