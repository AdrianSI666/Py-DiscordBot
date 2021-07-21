# -*- coding: utf-8 -*-
import os
import re
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
import random


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = commands.Bot(command_prefix='.')

folder = ['divinity', 'memy', 'me', 'me2', 'illaoi', 'lol', 'poppy', 'wrex', 'benezia']
pliki = []
aliasy = []
zajety = 0
podpiety = 0
usuniecia = 10


# melodie = ['divinity/hes dangerous we should kill him prince.mp3',
#            'divinity/monkey noises.mp3',
#            'divinity/oh how good ure would u like a treat.mp3',
#            'divinity/they found u monkey woman.mp3',
#            'divinity/yeeeeees.mp3']


@client.event
async def on_ready():
    k = 0
    for j in range(0, len(folder)):
        obecnepliki = []
        obecnealiasy = []
        files = os.listdir(folder[j])
        for f in files:
            obecnepliki.append(f)
        pliki.append(obecnepliki)
        for i in range(0, len(obecnepliki)):
            obecnealiasy.append(re.sub('[^A-Za-z0-9]+', '', obecnepliki[i][:6]))
            if obecnealiasy[i] == obecnealiasy[i - 1]:
                obecnealiasy[i - 1] = obecnealiasy[i - 1] + str(k)
                k = k + 1
            else:
                k = 0
        aliasy.append(obecnealiasy)
    print('Gotowy')


def switch_melodia(folders, melodia):
    wyjscie = ''
    for i in range(0, len(folder)):
        if folder[i] == folders:
            for j in range(0, len(aliasy[i])):
                if melodia == aliasy[i][j]:
                    wyjscie = folder[i] + '/' + pliki[i][j]
    return wyjscie
    # return {
    #     aliasy[0]: folder[0]+'/' + divinity[0],
    #     aliasy[1]: folder[0]+'/' + divinity[1],
    #     aliasy[2]: folder[0]+'/' + divinity[2],
    #     aliasy[3]: folder[0]+'/' + divinity[3],
    #     aliasy[4]: folder[0]+'/' + divinity[4]
    # }.get(folder, 'brak')


async def play(ctx, s):
    global usuniecia
    global zajety
    global podpiety
    global voice
    if podpiety == 0:
        podpiety = 1
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
    while True:
        if zajety == 0:
            zajety = 1
            usuniecia = 10
            source = FFmpegPCMAudio(s)
            voice.play(source)
            while voice.is_playing():
                await asyncio.sleep(.1)
            zajety = 0
            break
        else:
            await asyncio.sleep(.1)
    usuniecia = usuniecia - 1
    while usuniecia > 0:
        await asyncio.sleep(2)
        if (usuniecia == 10):
            break
        else:
            usuniecia = usuniecia - 1
            if usuniecia < 1:
                podpiety = 0
                if (usuniecia == 10):
                    break
                else:
                    await voice.disconnect()




que = []


def add(arg):
    que.insert(0, arg)


def get():
    return que.pop()


@client.command(pass_context=True)
async def say(ctx, opcja=None, opcja2=None):

    n = 0
    if opcja == None:

        embed1 = discord.Embed()
        embed1.description = "```\n.say <zestaw> <dzwiek> ```"
        embed1.set_author(name="Dostępne zestawy")
        for i in range(0, len(folder)):
            embed1.add_field(name=folder[i], value=folder[i], inline=True)
        embed1.add_field(name="Losowy dziwiek", value='rand', inline=True)
        await ctx.send(embed=embed1)

    else:
        if opcja == 'rand':
            fol = random.choice(folder)
            for i in range(0, len(folder)):
                if fol == folder[i]:
                    pli = random.choice(aliasy[i])
                    s = switch_melodia(fol, pli)
                    if ctx.author.voice:
                        add(s)
                        await play(ctx, get())
                    else:
                        await ctx.send("Nie jesteś na kanale głosowym")

        else:
            if opcja2 == None:

                embed1 = discord.Embed()
                embed1.description = "```\n.say " + opcja + " <dzwiek> ```"
                embed1.set_author(name="Dostępne dźwięki i komendy w tym zestawie")
                for j in range(0, len(folder)):
                    if opcja == folder[j]:
                        for i in range(0, len(aliasy[j])):
                            if (i % 25 == 24):
                                await ctx.send(embed=embed1)
                                embed1.clear_fields()
                            embed1.add_field(name=aliasy[j][i], value=pliki[j][i], inline=True)
                        await ctx.send(embed=embed1)
                    else:
                        n = n + 1

            else:
                if opcja2 == 'rand':
                    for i in range(0, len(folder)):
                        if opcja == folder[i]:
                            pli = random.choice(aliasy[i])
                            s = switch_melodia(opcja, pli)
                            if ctx.author.voice:
                                add(s)
                                await play(ctx, get())
                            else:
                                await ctx.send("Nie jesteś na kanale głosowym")
                else:
                    # opcja2=re.sub('[^A-Za-z0-9]+', '', opcja2[:6])
                    for i in range(0, len(folder)):
                        if opcja == folder[i]:
                            if ctx.author.voice:
                                s = switch_melodia(opcja, opcja2)
                                if s == '':
                                    await ctx.send("Brak takiego dźwięku.")
                                else:
                                    add(s)
                                    await play(ctx, get())
                            else:
                                await ctx.send("Nie jesteś na kanale głosowym")
                        else:
                            n = n + 1
    if n == len(folder):
        await ctx.send("Brak wybranego zestawu dźwięków, dostępne opcje:")
        embed1 = discord.Embed()
        embed1.description = "```\n.say <zestaw> <dzwiek> | !stop```"
        embed1.set_author(name="Dostępne zestawy")
        for i in range(0, len(folder)):
            embed1.add_field(name=folder[i], value=folder[i], inline=True)
        await ctx.send(embed=embed1)


client.run(token)
