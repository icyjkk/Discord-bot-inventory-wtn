from dataclasses import replace
from http import client
import imp
from urllib import request
from discord.ext import commands
import json
import discord
import os
import requests

os.system("title BotInventory")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

with open("BotConfig.json", "r") as archivo:
    data = json.load(archivo)
    # Canal asociado al bot, es el unico del que puede leer y escribir EL BOT.
    chanelID = int(data["chanelIDcomandos"])
    TOKEN = data["tokenBot"]
    ChanelID_monitor = data["chanelIDmonitor"]
    roleIDcomandosInternos = data["rolIDcomandosInternos"]


def crearEmbedinventory(dictshoes):

    lista = list(dictshoes.keys())
    if len(lista) != 0:
        resul = ""

        for elem in lista:
            resul = resul + "\n **" + elem + "** \n " + str(dictshoes[elem])

        embed = discord.Embed(
            title="**Your inventory**",
            description=resul,
            color=10181046,
        )

    else:
        embed = discord.Embed(
            title="**Your inventory**",
            description="Your inventory is empty",
            color=10181046,
        )

    embed.set_footer(
        text="Holdify ",
        icon_url="https://cdn.discordapp.com/attachments/837347805768843324/1019987728689025154/holdify_logo.jpg",
    )

    return embed


def escribirtag(message, nombre, talla):

    with open("tag.json", "r") as f:
        data = json.load(f)

    if nombre in data:
        if talla in data[nombre]:
            data[nombre][talla].append(message.author.id)
        else:
            data[nombre][talla] = [message.author.id]
    else:
        d = {talla: [message.author.id]}
        data[nombre] = d

    with open("tag.json", "w") as f:
        f.write(json.dumps(data, indent=1))


def comprobarCanal(message):
    resul = False

    if message.channel.id == chanelID:
        resul = True

    return resul


def sacarRoles(message):

    ListID = []

    for i in message.author.roles:
        ListID.append(i.id)

    return roleIDcomandosInternos in ListID


@bot.event
async def on_ready():  # Enciende el bot
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.channel.id == ChanelID_monitor:
        embed_content_in_dict = message.embeds[0].to_dict()

        title = embed_content_in_dict["title"]
        tallas = []
        for talla in embed_content_in_dict["fields"]:
            tallav = talla["name"]
            tallaf = tallav[:-3]
            tallas.append(tallaf)

        with open("tag.json", "r") as f:
            data = json.load(f)

        if title in data:
            menciones = []
            for talla in tallas:

                if talla in data[title]:

                    for id in data[title][talla]:
                        if id not in menciones:
                            await message.channel.send("<@!" + str(id) + ">")
                            menciones.append(id)

    elif message.channel.id == chanelID:
        await bot.process_commands(message)


@bot.command()
async def ping(message):
    # Para que solo se ejecuten comandos en el canal deseado y no en todos.
    if comprobarCanal(message):
        await message.send("PONG")


@bot.command(name="addName", help='!addName "name" size', pass_context=True)
async def addName(message, nombre, talla1, talla2=None):

    if comprobarCanal(
        message
    ):  # compruebo que es el canal en el que quiero los comandos
        if len(nombre) < 10:
            await message.channel.send(
                "Error, please enter the name in quotes"
            )  # Para que el nombre de la zapa completo este entre comillas y no se cuele solo por ejemplo el Air
        else:

            if talla2 == None:
                talla = talla1
            else:
                talla = str(talla1) + " " + str(talla2)

            escribir = True

            with open("diccionario.json", "r") as archivo:
                data = json.load(archivo)

            if (nombre not in data.keys()):  
                escribir = False
                await message.send( 
                    "This model does not exist in WTN. Tag some staff if is not name error or Search again the name : https://wethenew.com/"
                )        
            else:
                AuthorId = (
                    message.author.id
                )  # aqui se 100% que esta la zapa y hago el algoritmo del tiron

                if "," in talla:
                    talla = talla.replace(",", ".")

                with open("inventory.json", "r") as f:
                    data = json.load(f)
                    listUsers = data["users"]

                if AuthorId not in listUsers:
                    listUsers.append(AuthorId)
                    data["users"] = listUsers

                    d = {nombre: [talla]}
                    data[str(AuthorId)] = d
                else:
                    try:
                        if talla not in data[str(AuthorId)][nombre]:
                            data[str(AuthorId)][nombre].append(talla)
                            escribir = True
                        else:
                            await message.send(
                                "This model and size already in inventory."
                            )
                            escribir = False
                    except:
                        print("excepcion")
                        data[str(AuthorId)][nombre] = [talla]
            if escribir:
                with open("inventory.json", "w") as f:
                    f.write(json.dumps(data, indent=1))
                    await message.send(nombre + " " + talla + " added to inventory.")

                escribirtag(message, nombre, talla)


@bot.command(name="addSKU", help="!addSKU sku size", pass_context=True)
async def addSKU(message, sku, talla1, talla2=None):

    if comprobarCanal(message):

        escribir = True

        with open("diccionario.json", "r") as archivo:
            data = json.load(archivo)

        if sku not in data.values():

            if sku not in data.values():
                escribir = False
                await message.send(
                    "This sku does not exist in WTN. Try again with the name, since in WTN some sneakers do not have the sku. https://wethenew.com/"
                )
        else:
            nombre = list(data.keys())[list(data.values()).index(sku)]
            if talla2 == None:
                talla = talla1
            else:
                talla = str(talla1) + " " + str(talla2)
            AuthorId = message.author.id

            if "," in talla:
                talla = talla.replace(",", ".")

            with open("inventory.json", "r") as f:
                data = json.load(f)
                listUsers = data["users"]

            if AuthorId not in listUsers:
                listUsers.append(AuthorId)
                data["users"] = listUsers

                d = {nombre: [talla]}
                data[str(AuthorId)] = d
            else:
                try:
                    if talla not in data[str(AuthorId)][nombre]:
                        data[str(AuthorId)][nombre].append(talla)
                        escribir = True
                    else:
                        await message.send("This model and size already in inventory.")
                        escribir = False
                except:
                    print("excepcion")
                    data[str(AuthorId)][nombre] = [talla]

        if escribir:
            with open("inventory.json", "w") as f:
                f.write(json.dumps(data, indent=1))
                await message.send(nombre + " " + talla + " added to inventory.")

            escribirtag(message, nombre, talla)


@bot.command()
async def inventory(message):

    if comprobarCanal(message):
        AuthorId = message.author.id
        with open("inventory.json", "r") as f:
            data = json.load(f)
        if AuthorId not in data["users"]:
            await message.channel.send("Your inventory is empty")
        else:

            dictshoes = data[str(AuthorId)]
            embed = crearEmbedinventory(dictshoes)
            await message.channel.send(embed=embed)


@bot.command(
    name="remove",
    help='!remove "name" size or !remove "name" ',
    pass_context=True,
)
async def remove(message, nombre, talla=None):

    if comprobarCanal(message):

        if len(nombre) < 10:
            await message.channel.send("Error, please enter the name in quotes")
        else:
            AuthorId = message.author.id
            if talla == None:
                with open("inventory.json", "r") as f:
                    data = json.load(f)

                tallas=data[str(AuthorId)][nombre]

                if data[str(AuthorId)].pop(nombre, 404) != 404:

                    if len(data[str(AuthorId)]) == 0:
                        data["users"].remove(AuthorId)
                        data.pop(str(AuthorId))
                    
                    with open("inventory.json", "w") as f:
                        f.write(json.dumps(data, indent=1))
                        

                    with open("tag.json", "r") as f:
                        data1 = json.load(f)

                    for talla in tallas:
                        data1[nombre][talla].remove(AuthorId)

                        if len(data1[nombre][talla]) == 0:
                            data1[nombre].pop(talla)
                            if len(data1[nombre]) == 0:
                                data1.pop(nombre)
                            
                    with open("tag.json", "w") as f:
                        f.write(json.dumps(data1, indent=1))
                        await message.send(nombre + " removed from inventory.")

                else:
                    await message.channel.send(
                        "Error, this element is not in your inventory"
                    )
            else:
                with open("inventory.json", "r") as f:
                    data = json.load(f)

                if "," in talla:

                    talla = talla.replace(",", ".")

                if talla not in data[str(AuthorId)][nombre]:
                    await message.channel.send(
                        "Error, this size is not in your inventory"
                    )
                else:
                    data[str(AuthorId)][nombre].remove(talla)

                    if len(data[str(AuthorId)][nombre]) == 0:
                        data[str(AuthorId)].pop(nombre)
                        if len(data[str(AuthorId)]) == 0:
                            data["users"].remove(AuthorId)
                            data.pop(str(AuthorId))

                    with open("inventory.json", "w") as f:
                        f.write(json.dumps(data, indent=1))
                        
                    
                    with open("tag.json", "r") as f:
                        data1 = json.load(f)

                    data1[nombre][talla].remove(AuthorId)

                    if len(data1[nombre][talla]) == 0:
                        data1[nombre].pop(talla)
                        if len(data1[nombre]) == 0:
                            data1.pop(nombre)
                            
                    with open("tag.json", "w") as f:
                        f.write(json.dumps(data1, indent=1))
                        await message.send(
                            nombre + " " + talla + " removed from inventory."
                        )


@bot.command(
    name="removeSKU",
    help="!removeSKU sku size or !removeSKU sku ",
    pass_context=True,
)
async def remove(message, sku, talla=None):

    if comprobarCanal(message):

        with open("diccionario.json", "r") as archivo:
            data = json.load(archivo)

        nombre = list(data.keys())[list(data.values()).index(sku)]

        AuthorId = message.author.id
        if talla == None:
            with open("inventory.json", "r") as f:
                data = json.load(f)

            tallas=data[str(AuthorId)][nombre]

            if data[str(AuthorId)].pop(nombre, 404) != 404:

                if len(data[str(AuthorId)]) == 0:
                    data["users"].remove(AuthorId)
                    data.pop(str(AuthorId))

                with open("inventory.json", "w") as f:
                    f.write(json.dumps(data, indent=1))
                
                with open("tag.json", "r") as f:
                    data1 = json.load(f)

                for talla in tallas:
                    data1[nombre][talla].remove(AuthorId)

                    if len(data1[nombre][talla]) == 0:
                        data1[nombre].pop(talla)
                        if len(data1[nombre]) == 0:
                            data1.pop(nombre)
                            
                with open("tag.json", "w") as f:
                    f.write(json.dumps(data1, indent=1))
                    await message.send(nombre + " removed from inventory.")

            else:
                await message.channel.send(
                    "Error, this element is not in your inventory"
                )
        else:
            with open("inventory.json", "r") as f:
                data = json.load(f)

            if "," in talla:

                talla = talla.replace(",", ".")

            if talla not in data[str(AuthorId)][nombre]:
                await message.channel.send("Error, this size is not in your inventory")
            else:
                data[str(AuthorId)][nombre].remove(talla)

                if len(data[str(AuthorId)][nombre]) == 0:
                    data[str(AuthorId)].pop(nombre)
                    if len(data[str(AuthorId)]) == 0:
                        data["users"].remove(AuthorId)
                        data.pop(str(AuthorId))

                with open("inventory.json", "w") as f:
                    f.write(json.dumps(data, indent=1))
                
                with open("tag.json", "r") as f:
                        data1 = json.load(f)

                data1[nombre][talla].remove(AuthorId)

                if len(data1[nombre][talla]) == 0:
                    data1[nombre].pop(talla)
                    if len(data1[nombre]) == 0:
                         data1.pop(nombre)
                            
                with open("tag.json", "w") as f:
                    f.write(json.dumps(data1, indent=1))
                    await message.send(
                        nombre + " " + talla + " removed from inventory."
                    )


@bot.command() #Este comando añade el nombre de la zapa y el sku a la base de datos
async def add(message, nombre, sku=None):

    if comprobarCanal(message) and sacarRoles(message):
        AuthorId = message.author.id

        if len(nombre) < 10:
            await message.channel.send("Error, please enter the name in quotes")
        else:

            with open("diccionario.json", "r") as f:
                data = json.load(f)

            if nombre in data.keys():
                await message.channel.send("This name alredy in DataBase")
            else:

                if sku in data.values() and sku != None:
                    await message.channel.send("This sku alredy in DataBase")
                else:
                    if sku == None:
                        data[nombre] = ""
                    else:
                        data[nombre] = sku

                    with open("diccionario.json", "w") as f:
                        f.write(json.dumps(data, indent=1))

                    await message.send(nombre + " added successfully.")


bot.run(TOKEN)
