import discord
from discord.ext import commands
import time
import os
import asyncio

bot = commands.Bot(command_prefix='!',case_insensitive = True)
bot.remove_command('help')

def print_log(ctx):
    print("\n{.message.author} used {.message.clean_content}\nAt {} in {.message.channel}\n".format(ctx,ctx,time.asctime(time.localtime()),ctx))

#Log events

@bot.event
async def on_ready():
    print('Logged in as: {}\nLogging time: {}'.format(bot.user.name,time.asctime(time.localtime())))
    print('Logging id: {}'.format(bot.user.id))
    print('------\n')

#Reactions Events

@bot.event
async def on_member_join(member):
    print("\n{.name} joined the server at {}\n".format(member,time.asctime(time.localtime())))
    role = discord.utils.get(member.server.roles,name = "Aspirante")

    await bot.add_roles(member,role)

    embed= discord.Embed(title="Bienvenido a Robota", description="Gracias por unirte al servidor de Discord de Robota, aqui podras consultar a los miembros y lideres de categoria mas eficientemente", color=0x14ff34)
    embed.set_author(name="PITKA", url="https://github.com/kazp058/PITKA", icon_url="https://github.com/kazp058/PITKA/blob/master/PITKA%20logo.png?raw=true")
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/898515510412881920/48vQFici.jpg")
    embed.add_field(name="Para informarte sobre las reglas puedes ingresar a:", value="https://docplayer.es/60703623-Escuela-superior-politecnica-del-litoral-reglamento-interno-del-club-de-robotica-robota-espol-preambulo.html", inline=False)
    embed.add_field(name = "Comandos:",value = "Hay algunos comandos que puedes usar para ingresar a categorias o cambiar tu nombre, usa !help para saber mas",inline = True)

    await bot.send_message(member,embed=embed)

@bot.event
async def on_command_error(error,ctx):
    if isinstance(error,commands.MissingRequiredArgument):
        embed= discord.Embed(title="Error", description="No has ingresado todos los parametros para el comando, usa el comando !help para mas informacion", color=0xff1414)
        await bot.send_message(ctx.message.channel,embed=embed)
    elif isinstance(error,commands.CommandInvokeError):
        embed= discord.Embed(title="Error", description="Ha ocurrido un error al invocar el comando, porfavor intentalo mas tarde", color=0xff1414)
        await bot.send_message(ctx.message.channel,embed=embed)
    elif isinstance(error,commands.CommandNotFound):
        embed= discord.Embed(title="Error", description="El comando que has invocado no existe, usa el comando !help para ver los comandos disponibles", color=0xff1414)
        await bot.send_message(ctx.message.channel,embed=embed)

#Commands

@bot.command(pass_context = True)
async def nickname(ctx,nombre):
    
    print_log(ctx)
    
    if ctx.message.channel.is_private == True:
        embed= discord.Embed(title="Error", description="Usaste el comando en un canal privado, los comandos solo estan habilitados en los canales de Robota", color=0xff1414)
        await bot.send_message(ctx.message.author,embed=embed)
    else:
        nombre = ' '.join(str(ctx.message.clean_content).split(' ')[1:])
        nombre = nombre.title()
        await bot.change_nickname(ctx.message.author,nombre)

        embed= discord.Embed(title="Success", description="El comando ha sido ejecutado correctamente", color=0x144fff)
        await bot.send_message(ctx.message.author,embed=embed)

        await bot.delete_message(ctx.message)

@bot.command(pass_context = True, brief = 'Muestra las categorias disponibles' ,help = "Muestra las categorias disponibles")
async def categorias(ctx):

    print_log(ctx)

    if ctx.message.channel.is_private == True:
        embed= discord.Embed(title="Error", description="Usaste el comando en un canal privado, los comandos solo estan habilitados en los canales de Robota", color=0xff1414)
        await bot.send_message(ctx.message.author,embed=embed)
    else:
        roles = list(ctx.message.channel.server.role_hierarchy)

        aspirante = discord.utils.get(ctx.message.channel.server.roles,name = "Aspirante")
        everyone = ctx.message.channel.server.default_role

        embed= discord.Embed(color=0xfffb14)
        embed.set_author(name="PITKA", url="https://github.com/kazp058/PITKA", icon_url="https://github.com/kazp058/PITKA/blob/master/PITKA%20logo.png?raw=true")
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/898515510412881920/48vQFici.jpg")

        nrole = []

        for role in roles:
            if role < aspirante and role > everyone:
                nrole.append(str(role))

        embed.add_field(name = "Categorias: " , value = "\n".join(nrole),inline = False)
        await bot.send_message(ctx.message.channel,embed = embed)

@bot.command(pass_context = True)
async def join(ctx,categoria):

    print_log(ctx)

    if ctx.message.channel.is_private == True:
        embed= discord.Embed(title="Error", description="Usaste el comando en un canal privado, los comandos solo estan habilitados en los canales de Robota", color=0xff1414)
        await bot.send_message(ctx.message.author,embed=embed)
    else:
        categoria = categoria.title()
        if categoria in get_roles(ctx.message.server):
            if ctx.message.author.top_role >= get_role(ctx.message.server,"Miembro Activo"):

                categoria = get_role(ctx.message.server,categoria)
                await bot.add_roles(ctx.message.author,categoria)
                await bot.delete_message(ctx.message)

            else:
                if len(list(ctx.message.author.roles)) <= 4:
                    categoria = get_role(ctx.message.server,categoria)
                    await bot.add_roles(ctx.message.author,categoria)
                    await bot.delete_message(ctx.message)
                else:
                    embed= discord.Embed(title="Error", description="Haz superado el limite de categorias a las que puedes postular", color=0xff1414)
                    await bot.send_message(ctx.message.author,embed=embed)
        else:
            embed= discord.Embed(title="Error", description="La categoria mencionada no se encuentra en la lista de categorias usa !categorias para ver las categorias disponibles", color=0xff1414)
            await bot.send_message(ctx.message.author,embed=embed)
            
@bot.command(pass_context = True)
async def help(ctx,*,msg = None):

    print_log(ctx)

    commands = ["join","categorias","nickname"]

    if msg not in commands:
        embed= discord.Embed(title="Comando de Ayuda", description="Acontinuacion podras ver todos los comandos disponibles.", color=0xfffb14)
        embed.set_author(name="PITKA", url="https://github.com/kazp058/PITKA", icon_url="https://github.com/kazp058/PITKA/blob/master/PITKA%20logo.png?raw=true")
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/898515510412881920/48vQFici.jpg")
        embed.add_field(name="\n!join categoria", value="Te permite unirte a una categoria.", inline=False)
        embed.add_field(name="\n!categorias", value="Te visualizar las categorias disponibles.", inline=False)
        embed.add_field(name="\n!nickname nombre apellido", value="Te permite cambiar el nombre que se muestra en el chat.", inline=False)
        embed.add_field(name="\n!help comando", value="Te permite obtener mas ayuda sobre un comando especifico.", inline=False)
        embed.set_footer(text="Recuerda que los comandos solo pueden ser usados en canales del servidor de Robota")
        await bot.send_message(ctx.message.channel,embed=embed)
    elif msg == "join":
        embed= discord.Embed(title="Comando Join", description="El comando !join te permite unirte a una categoria de las que se encuentren disponibles.", color=0xfffb14)
        embed.set_author(name="PITKA", url="https://github.com/kazp058/PITKA", icon_url="https://github.com/kazp058/PITKA/blob/master/PITKA%20logo.png?raw=true")
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/898515510412881920/48vQFici.jpg")
        embed.add_field(name="Comando:", value="!join Categoria", inline=False)
        embed.add_field(name="Ejemplo 1:", value="!join Soccer", inline=True)
        embed.add_field(name="Ejemplo 2:", value="!join Batalla", inline=True)
        embed.set_footer(text="Recuerda que los comandos solo pueden ser usados en canales del servidor de Robota")
        await bot.send_message(ctx.message.channel,embed=embed)
    elif msg == "categorias":
        embed= discord.Embed(title="Comando Join", description="El comando !categorias te muestra todas las categorias disponibles a las que te puedes unir.", color=0xfffb14)
        embed.set_author(name="PITKA", url="https://github.com/kazp058/PITKA", icon_url="https://github.com/kazp058/PITKA/blob/master/PITKA%20logo.png?raw=true")
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/898515510412881920/48vQFici.jpg")
        embed.add_field(name="Comando:", value="!categorias", inline=False)
        embed.add_field(name="Ejemplo:", value="!categorias", inline=True)
        embed.set_footer(text="Recuerda que los comandos solo pueden ser usados en canales del servidor de Robota")
        await bot.send_message(ctx.message.channel,embed=embed)
    elif msg == "nickname":
        embed= discord.Embed(title="Comando Join", description="El comando !nickname te permite cambiar tu nombre que se muestra en chat, esto permite que sea mas facil saber con quien se esta hablando.", color=0xfffb14)
        embed.set_author(name="PITKA", url="https://github.com/kazp058/PITKA", icon_url="https://github.com/kazp058/PITKA/blob/master/PITKA%20logo.png?raw=true")
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/898515510412881920/48vQFici.jpg")
        embed.add_field(name="Comando:", value="!nickname Nombre Apellido", inline=False)
        embed.add_field(name="Ejemplo 1:", value="!nickname Fernando Troya", inline=True)
        embed.add_field(name="Ejemplo 2:", value="!nickname Abraham Gavilanes", inline=True)
        embed.set_footer(text="Recuerda que los comandos solo pueden ser usados en canales del servidor de Robota")
        await bot.send_message(ctx.message.channel,embed=embed)

if __name__ == "__main__":
    try:
        token = os.environ.get("BOT_TOKEN")
        bot.run(token)
    except Exception as e:
        print("Tried to start session at {}\nBut failed using token: {}".format(time.asctime(time.localtime()),token))
        print(str(e))
