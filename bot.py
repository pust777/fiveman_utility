import asyncio
import os
from discord.ext import commands
from cogs.utils import checks
import fetch
import db_worker
from hots_build_builder import BuildBuilder
import logging

KEY = os.environ.get('FIVE_MAN')#JSON_KEYS['five-man']
BUILD_BUILDER = BuildBuilder()

DESCRIPTION = '''An example bot to showcase the discord.ext.commands extension
module.There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix="?", description=DESCRIPTION)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="?help"))

@bot.event
async def on_message(message):
    if message.content.startswith("[[") and message.content.endswith("]]"):
        info_request = message.content[2:-2].lower()
        msg = BUILD_BUILDER.process_request(info_request)
        talent = message.content[2:-2].lower()
        description = BUILD_BUILDER.get_talent(talent)
        await bot.send_message(message.channel, "talent, that's generous")
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def say(ctx, *, message=None):
    if message is None:
        await bot.say("Say something, I'm giving up on you.\nI'll be the bot, if you want me to.")
    else:
        await bot.say(message)

@bot.command(pass_context=True)
async def strong(ctx, *, message=None):
    if message is None:
        await bot.say("What hero counter are you looking for?")
    else:
        counters = fetch.get_strong_counters(message)
        await bot.say(counters)

@bot.command(pass_context=True)
async def weak(ctx, *, message=None):
    if message is None:
        await bot.say("What hero counter are you looking for?")
    else:
        counters = fetch.get_weak_counters(message)
        await bot.say(counters)

@bot.command(pass_context=True)
async def patchfor(ctx, *, message=None):
    if message is None:
        await bot.say("What hero patchnotes are you looking for?")
    else:
        patch = fetch.get_hero_patch_notes(message)
        await bot.say(patch)

@bot.command(pass_context=True)
async def build(ctx, *, message=None, aliases=["build", "builds"]):
    if message is None:
        await bot.say("What hero build are you looking for?")
    else:
        hero = message
        builds = BUILD_BUILDER.get_builds_for_hero(hero)
        await bot.say(builds)

@bot.command()
async def patchnotes():
    patch_notes_links = fetch.get_latest_patch_notes()
    patch_notes_links = '3 most recent patches:\n' + patch_notes_links
    await  bot.say(patch_notes_links)

@bot.command(pass_context=True)
async def h(ctx, *, message=None):
    if message is None:
        await bot.say("What?")
    else:
        info_request = message.content[2:-2].lower()
        msg = BUILD_BUILDER.process_request(info_request)
        talent = message.content[2:-2].lower()
        #description = BUILD_BUILDER.get_talent(talent)
        #await bot.send_message(message.channel, msg)
        await bot.send_message(message.channel, "talent, that's generous")


# def test():
#     '''test all the things'''
#     print("Testing strong...{}".format(fetch.get_strong_counters('the lost vikings')))
     # print("Testing weak...{}".format(fetch.get_weak_counters('the lost vikings')))
     # print("Testing patchfor...{}".format(fetch.get_hero_patch_notes('the lost vikings')))
     # print("Testing patchnotes...{}".format(fetch.get_latest_patch_notes()))
     # #print("Testing build...{}".format(BUILD_BUILDER.get_builds_for_hero('the lost vikings')))
     # print("Testing details...{}".format(fetch.get_hero_details('the lost vikings')))
     # print("Testing talents...{}".format(fetch.get_hero_talents('the lost vikings')))
     # print("Testing ability-hotkey...{}".format(fetch.get_hero_ability_for_hotkey('the lost vikings', 'Q')))


# @bot.command(passed_context=True)
# async def registertag(ctx):
#     discordID = ctx.message.author
#     battletag = message
#     await bot.say("{0}, {1}".format(discordID, battletag))
#         #db_worker.register_discordID_for_battletag(db_worker.get_connection(JAWS_DICT), discordID, battletag)

# "kregnax#2710"
# @bot.command(passed_context=True)
# async def addtxtcmd(ctx):
#     if(str(ctx.message.author) == "ody77#9828"):
#         print(ctx.message.content)
#         bot.say(ctx.message.content)


    #     cmd_in = message.content.split()
    #     if(cmd_in[0] == "!addtxtcmd"):
    #         text_command = cmd_in[1]
    #         text_output = ''.join(w + ' ' for w in cmd_in[2:]).strip()
    #         TEXT_COMMANDS[text_command] = text_output
    #         db_worker.add_new_text_command(db_worker.get_connection(JAWS_DICT), text_command, text_output)
    #     else:
    #         await CLIENT.send_message(message.channel, "Unrecognized command: {}".format(cmd_in[0]))
    # else:
    #     await CLIENT.send_message(message.channel, "You don't have access, fool.")

# @bot.command(pass_context=True)
# async def excom(self, ctx):
#     """CTX example command"""
#     author = ctx.message.author
#     description2 = ("Short little description with a link to "
#                    "the [guide](https://github.com/Redjumpman/Jumper-Cogs/wiki/Discord-Coding-Guide)")
#     field_name = "Generic Name"
#     field_contents = "Example contents for this field"
#     footer_text = "Hi. I am a footer text. I look small when displayed."
#     embed = discord.Embed(colour=0xFF0000, description=description2)  # Can use discord.Colour()
#     embed.title = "Cool title for my embed"
#     embed.set_author(name=str(author.name), icon_url=author.avatar_url)
#     embed.add_field(name=field_name, value=field_contents)  # Can add multiple fields.
#     embed.set_footer(text=footer_text)
#     await self.bot.say(embed=embed)



bot.run(KEY)
