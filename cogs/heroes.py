from discord.ext import commands
from .utils.chat_formatting import box
from .utils.dataIO import dataIO
from .utils import checks
from __main__ import user_allowed, send_cmd_help
import os
import discord

import json
import time
import git
import discord
import os
import aiohttp
from cogs.utils.dataIO import dataIO
from urllib.parse import quote as uriquote



class HeroError(Exception):
    pass





class Hero:
    def __init__(self, bot):
        self.bot = bot
        
        
     
    @commands.command(hidden=True)
    async def ping(self):
        """Pong."""
        await self.bot.say("Pong.")
        
    @commands.command()
    async def choose(self, *choices):
        """Chooses between multiple choices.
        To denote multiple choices, you should use double quotes.
        """
        choices = [escape_mass_mentions(c) for c in choices]
        if len(choices) < 2:
            await self.bot.say('Not enough choices to pick from.')
        else:
            await self.bot.say(choice(choices))
        
        
        

@checks.vaild_hero()


def check_alias():
    #if not os.path.exists("data/alias"):
    #    print("Creating data/alias folder...")
    #    os.makedirs("data/alias")


def check_content():
    #aliases = {}
    #f = "data/alias/aliases.json"
    #if not dataIO.is_valid_json(f):
    #    print("Creating default alias's aliases.json...")
    #    dataIO.save_json(f, aliases)




def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(AlHeroias(bot))
