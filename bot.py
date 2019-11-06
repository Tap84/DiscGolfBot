import discord
import sqlite3

client = discord.Client()

conn = sqlite3.connect('database.sqlite3')

"""
conn.execute(''' CREATE TABLE IF NOT EXISTS prodigy_discs(
                NAME TEXT PRIMARY KEY NOT NULL,
                CLASS TEXT NOT NULL,
                SPEED DECIMAL NOT NULL,
                GLIDE DECIMAL NOT NULL,
                TURN DECIMAL NOT NULL,
                FADE DECIMAL NOT NULL
                                            ) ''')
"""
#                       Tyler               Dylan               Nick                Zane                Skaffen             Deck
authorized_users = [94953298645225472, 428298884998234112, 275626705475862530, 99017591317610496, 507227977394946048, 98607564257771520]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content.startswith('.disc'):
        try:
            discs_stripped = message.content[6:].replace(' ','').split(',')
            for disc in discs_stripped:    
                await search_disc_by_name(disc,message)
        except:
            await message.channel.send("Search Failed")
    
    if message.content.startswith('.adddisc') and message.author.id in authorized_users:
        discinfo = message.content[8:].split()
        try:
            await add_disc(discinfo, message)
        except:
            await message.channel.send("Failed")
    elif message.content.startswith('.adddisc'):
        await message.channel.send("Unauthorized")                     
                                            
async def add_disc(discinfo, message):
    conn.execute(''' INSERT INTO discs(NAME,MANUFACTURER,SPEED,GLIDE,TURN,FADE)
                        VALUES(?,?,?,?,?,?)''',    (discinfo[0].lower(),
                                                    discinfo[1].lower(),
                                                    discinfo[2],
                                                    discinfo[3],
                                                    discinfo[4],
                                                    discinfo[5]))
    conn.commit()
    await message.channel.send("Added")
    
async def search_disc_by_name(name, message):
    name = name.lower()
    
    out_message = "```"
    cur = conn.cursor()
    cur.execute(f''' SELECT * FROM discs WHERE NAME=?''',(name,))
    disc = cur.fetchall()[0]
    out_message += f'''Name: {disc[0]}\nManufacturer: {disc[1]}\nSpeed: {disc[2]}\nGlide: {disc[3]}\nTurn: {disc[4]}\nFade: {disc[5]}'''
    out_message += "```"
    await message.channel.send(out_message)

keyfile = open('key.txt')
key = keyfile.readline().strip()         
client.run(key)