import discord
import json
import urllib.request
from discord.ext import commands
import datetime
import random
from urllib.parse import quote

TOKEN = "Njg4MzE0MDI0MDUxNzM2NTg1.XmyhDA.dC3n_GvM9AIPv3bPx26l4YKTBMQ"
client = commands.Bot(command_prefix='!')


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.command()
async def info(ctx):
    embed = discord.Embed(title="Information",
                          description="Use !covid for total stats and `!covid <countryname>` (Example: `!covid Italy` would return coronavirus stats for Italy). "
                                      "You can get a list of infected countries by doing `!covid all <pagenumber>` (Example: `!covid all 12` would return the 12th page of 21). "
                                      "You can also get a random country by doing `!covid random` If something doesn't work or you have any comments, feel free to message Segfault#9190.", color=0x000000)
    embed.set_footer(text=":) Stay Safe")
    await ctx.send(embed=embed)


@client.command()
async def covid(ctx, *args):
    if len(args) == 0:
        total_site_url = "https://corona.lmao.ninja/v2/all"
        total_site_page = urllib.request.Request(total_site_url, headers={'User-Agent': 'Mozilla/5.0'})
        total_site_info = urllib.request.urlopen(total_site_page).read()
        total_site_data = json.loads(total_site_info.decode())
        embed = discord.Embed(title="Covid 2019", description="Worldwide Stats", color=0x000000)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/International_Flag_of_Planet_Earth.svg/525px-International_Flag_of_Planet_Earth.svg.png")
        embed.add_field(name="Cases", value=str(f'{total_site_data["cases"]:,}'))
        embed.add_field(name="Deaths", value=str(f'{total_site_data["deaths"]:,}'))
        embed.add_field(name="Recoveries", value=str(f'{total_site_data["recovered"]:,}'))
        embed.add_field(name="Cases Today", value="+" + str(f'{total_site_data["todayCases"]:,}'))
        embed.add_field(name="Deaths Today", value="+" + str(f'{total_site_data["todayDeaths"]:,}'))
        embed.add_field(name="Affected Countries", value=str(f'{total_site_data["affectedCountries"]:,}'))
        date = datetime.datetime.fromtimestamp(total_site_data['updated'] / 1000.0)
        date = date.strftime('%B %-dth, %Y. %-I:%M %p')
        embed.set_footer(text="Last Updated: " + date + " GMT-4")
        await ctx.send(embed=embed)
    elif args[0].lower() == 'all':
        if len(args) > 1:
            try:
                int(args[1])
            except ValueError:
                await ctx.send("`!covid all` requires a number")
                return
        if len(args) == 1 or len(args) > 2:
            await ctx.send("Invalid usage of `!covid all` command.")
            return
        all_countries = []
        countries_url = "https://corona.lmao.ninja/v2/countries"
        countries_page = urllib.request.Request(countries_url, headers={'User-Agent': 'Mozilla/5.0'})
        countries_info = urllib.request.urlopen(countries_page).read()
        countries_data = json.loads(countries_info.decode())
        embed = discord.Embed(title="List of Countries", description="Countries", color=0x000000)
        for i in countries_data:
            all_countries.append(i['country'])
        page_num = int(args[1])
        if page_num < 1 or page_num > 21:
            await ctx.send("Invalid page number.")
            return
        count = (page_num - 1) * 10
        for i in range(count, count + 10):
            if i == 0:
                embed.add_field(name="1", value=all_countries[210], inline=False)
            embed.add_field(name=str(i + 2), value=all_countries[i], inline=False)
            embed.set_footer(text="Page number " + str(args[1]) + "/" + "21")
        await ctx.send(embed=embed)
    elif args[0].lower() == 'random':
        if not len(args) == 1:
            await ctx.send("Invalid usage of `!covid random`")
            return
        all_countries = []
        countries_url = "https://corona.lmao.ninja/v2/countries"
        countries_page = urllib.request.Request(countries_url, headers={'User-Agent': 'Mozilla/5.0'})
        countries_info = urllib.request.urlopen(countries_page).read()
        countries_data = json.loads(countries_info.decode())
        for i in countries_data:
            all_countries.append(i['country'])
        rand_country = random.randrange(0, len(all_countries))
        the_country = str(all_countries[rand_country])
        the_country = the_country.replace(" ", "%20")
        try:
            if "%20" in the_country:
                countries_url = "https://corona.lmao.ninja/v2/countries/" + the_country
            else:
                countries_url = "https://corona.lmao.ninja/v2/countries/" + quote(the_country)
            print(countries_url)
            countries_page = urllib.request.Request(countries_url, headers={'User-Agent': 'Mozilla/5.0'})
            countries_info = urllib.request.urlopen(countries_page).read()
            countries_data = json.loads(countries_info.decode())
            country = countries_data
            embed = discord.Embed(title=country['country'].upper(),
                                  description=f"Coronavirus information for {country['country'].upper()}",
                                  color=0x000000)
            embed.set_thumbnail(url=country['countryInfo']['flag'])
            embed.add_field(name="Cases", value=str(f'{country["cases"]:,}'))
            embed.add_field(name="Deaths", value=str(f'{country["deaths"]:,}'))
            embed.add_field(name="Recoveries", value=str(f'{country["recovered"]:,}'))
            embed.add_field(name="Cases Today", value="+" + str(f'{country["todayCases"]:,}'))
            embed.add_field(name="Deaths Today", value="+" + str(f'{country["todayDeaths"]:,}'))
            embed.add_field(name="Active Cases", value=str(f'{country["active"]:,}'))
            date = datetime.datetime.fromtimestamp(country['updated'] / 1000.0)
            date = date.strftime('%B %-dth, %Y. %-I:%M %p')
            embed.set_footer(text="Last Updated: " + date + " GMT-4")
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send("Please try again.")
            return
    else:
        country = " "
        arg_size = len(args)
        if arg_size > 1:
            country = country.join(args)
        else:
            country = args[0]
        countries_url = "https://corona.lmao.ninja/v2/countries"
        countries_page = urllib.request.Request(countries_url, headers={'User-Agent': 'Mozilla/5.0'})
        countries_info = urllib.request.urlopen(countries_page).read()
        countries_data = json.loads(countries_info.decode())
        country_exists = False
        index_country = 0
        for i in countries_data:
            index_country += 1
            if i['country'].upper() == country.upper():
                country_exists = True
                break
        if not country_exists:
            await ctx.send("Invalid Country.")
        else:
            country = countries_data[index_country - 1]
            embed = discord.Embed(title=country['country'].upper(), description=f"Coronavirus information for {country['country'].upper()}", color=0x000000)
            embed.set_thumbnail(url=country['countryInfo']['flag'])
            embed.add_field(name="Cases", value=str(f'{country["cases"]:,}'))
            embed.add_field(name="Deaths", value=str(f'{country["deaths"]:,}'))
            embed.add_field(name="Recoveries", value=str(f'{country["recovered"]:,}'))
            embed.add_field(name="Cases Today", value="+" + str(f'{country["todayCases"]:,}'))
            embed.add_field(name="Deaths Today", value="+" + str(f'{country["todayDeaths"]:,}'))
            embed.add_field(name="Active Cases", value=str(f'{country["active"]:,}'))
            date = datetime.datetime.fromtimestamp(country['updated'] / 1000.0)
            date = date.strftime('%B %-dth, %Y. %-I:%M %p')
            embed.set_footer(text="Last Updated: " + date + " GMT-4")
            await ctx.send(embed=embed)


@client.event
async def on_guild_join(guild):
    server_count = len(client.guilds)
    await client.change_presence(status=discord.Status.do_not_disturb,
                                 activity=discord.Game("!info in " + str(server_count) + " servers"))


@client.event
async def on_guild_remove(guild):
    print("I was removed :(")
    server_count = len(client.guilds)
    await client.change_presence(status=discord.Status.do_not_disturb,
                                 activity=discord.Game("!info in " + str(server_count) + " servers"))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    server_count = len(client.guilds)
    await client.change_presence(status=discord.Status.do_not_disturb,
                                 activity=discord.Game("!info in " + str(server_count) + " servers"))


client.run(TOKEN)
