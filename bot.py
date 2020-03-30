import discord
import requests
from bs4 import BeautifulSoup
import time
import datetime
from discord.ext import commands

prev_time = 0
prev_cases = 0
prev_deaths = 0
prev_recoveries = 0
server_list = []
TOKEN = the_token
count = 0
client = commands.Bot(command_prefix='!')


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.command()
async def info(ctx):
    await ctx.send(
        "Use !covid for total stats and !covid <countryname> for a specific country. You can get a list of supported countries "
        "by doing !covid all <pagenumber> where pagenumber is between 1 and 5. The bot only supports top 25 countries. If something doesn't work, "
        "blame the code, not me ;)")


@client.command()
async def covid(ctx, *args):
    if len(args) == 0:
        global prev_time, prev_cases, prev_deaths, prev_recoveries, count, server_list
        x = requests.get('https://www.worldometers.info/coronavirus/')
        soup = BeautifulSoup(x.content, features="html.parser")
        divs = soup.findAll("div", {"class": "maincounter-number"})
        embed = discord.Embed(title="Covid 2019", description="Worldwide Stats", color=0x000000)
        curr_cases = divs[0].text.strip()
        curr_deaths = divs[1].text.strip()
        curr_recoveries = divs[2].text.strip()
        embed.add_field(name="Cases", value=curr_cases, inline=False)
        embed.add_field(name="Deaths", value=curr_deaths, inline=False)
        embed.add_field(name="Recoveries", value=curr_recoveries, inline=False)
        prev_cases = str(prev_cases).replace(",", "")
        prev_deaths = str(prev_deaths).replace(",", "")
        prev_recoveries = str(prev_recoveries).replace(",", "")
        curr_cases = str(curr_cases).replace(",", "")
        curr_deaths = str(curr_deaths).replace(",", "")
        curr_recoveries = str(curr_recoveries).replace(",", "")
        prev_curr_cases_diff = int(curr_cases) - int(prev_cases)
        if not count == 0:
            embed.add_field(name="Number of new cases", value=str(prev_curr_cases_diff), inline=False)
            prev_curr_deaths_diff = int(curr_deaths) - int(prev_deaths)
            embed.add_field(name="Number of new deaths", value=str(prev_curr_deaths_diff), inline=False)
            prev_curr_rec_diff = int(curr_recoveries) - int(prev_recoveries)
            embed.add_field(name="Number of new recoveries", value=str(prev_curr_rec_diff), inline=False)
        prev_cases = curr_cases
        prev_deaths = curr_deaths
        prev_recoveries = curr_recoveries
        curr_time = round(time.time())
        if not count == 0:
            prev_curr_diff = curr_time - prev_time
            t_format = str(datetime.timedelta(seconds=prev_curr_diff))
            embed.add_field(name="Time before last call", value=t_format, inline=False)
        prev_time = curr_time
        await ctx.send(embed=embed)
        count += 1
    else:
        x = requests.get('https://www.worldometers.info/coronavirus/')
        soup = BeautifulSoup(x.content, features="html.parser")
        countries = soup.findAll("a", {"class": "mt_a"})
        try:
            if len(args) > 2:
                await ctx.send("Invalid Country")
                return
            if args[0] == 'all':
                page_num = int(args[1])
                if page_num < 0 or page_num > 5:
                    await ctx.send("Invalid page number.")
                    return
                embed = discord.Embed(title="Countries", description="List of Countries", color=0x000000)
                c_count = ((page_num - 1) * 5)
                l_countries = []
                for country in countries:
                    l_countries.append(country.text)
                if "S. Korea" in l_countries:
                    index_ = l_countries.index("S. Korea")
                    l_countries[index_] = "South Korea"
                if "USA" in l_countries:
                    index_ = l_countries.index("USA")
                    l_countries[index_] = "US"
                del l_countries[26:]
                for c in range(c_count, c_count + 5):
                    embed.add_field(name=l_countries[c], value=str(c + 1) + '. ' + l_countries[c], inline=False)
                    embed.set_footer(text="Page number: " + str(args[1]) + '/' + "5")
                await ctx.send(embed=embed)
            else:
                l_countries = []
                for country in countries:
                    l_countries.append(country.text)
                if "S. Korea" in l_countries:
                    index_ = l_countries.index("S. Korea")
                    l_countries[index_] = "South Korea"
                if "USA" in l_countries:
                    index_ = l_countries.index("USA")
                    l_countries[index_] = "US"
                del l_countries[26:]
                l_countries = [x.lower() for x in l_countries]
                if args[0].lower() in l_countries or (args[0].lower() + ' ' + args[1].lower() in l_countries):
                    if len(args) == 1:
                        x = requests.get('https://www.worldometers.info/coronavirus/country/' + args[0])
                    else:
                        if args[0] == "Hong":
                            x = requests.get('https://www.worldometers.info/coronavirus/country/china-hong-kong-sar/')
                        else:
                            x = requests.get(
                                'https://www.worldometers.info/coronavirus/country/' + args[0] + '-' + args[1])
                    soup = BeautifulSoup(x.content, features="html.parser")
                    divs = soup.findAll("div", {"class": "maincounter-number"})
                    if args[0] == "Hong":
                        embed = discord.Embed(title="HONG KONG", description="Stats for HONG KONG", color=0x000000)
                    elif args[0] == "South":
                        embed = discord.Embed(title="SOUTH KOREA", description="Stats for SOUTH KOREA", color=0x000000)
                    else:
                        embed = discord.Embed(title=args[0].upper(), description=f"Stats for {args[0].upper()}",
                                              color=0x000000)
                    embed.add_field(name="Cases", value=divs[0].text.strip(), inline=False)
                    embed.add_field(name="Deaths", value=divs[1].text.strip(), inline=False)
                    embed.add_field(name="Recoveries", value=divs[2].text.strip(), inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Invalid Country")
                    return
        except Exception:
            await ctx.send("Invalid Country")
            return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("!info"))


client.run(TOKEN)
