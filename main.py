import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import json
import os
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # nécessaire pour le message de bienvenue
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("❌Membre introuvable dans ce serveur.❌")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌Tu n'a pas les permissions pour effectuer cette commande.❌")
    else:
        # Optionnel : print l'erreur si ce n'est pas un MemberNotFound, pour debug
        raise error


def get_roles_as_string(member):
    roles = [role.name for role in member.roles if role.name != "@everyone"]
    return ", ".join(roles) if roles else "Aucun rôle"


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong !")


@bot.command()
@commands.has_permissions(administrator = True)
async def helpmodo(ctx):
    await ctx.send(f"""
Voici les comamndes disponibles pour les modérateurs :\n
!helpmodo - affiche cette aide \n
!setwelcome - permet de changer le salon de notification d'arrivé \n
!clear - permet de supprimer le nombre de messages donnés (5 si pas de valeur donné)\n
""")


@bot.command()
async def helpme(ctx):
    await ctx.send(f"""
Voici les commandes disponibles :\n
!ping - Vérifie si le bot est actif\n
!helpme - Affiche cette aide\n
!userinfo - donne le pseudo, l'ID, la date d'arrivée sur le serveur et le role d'un membre\n
!avatar - affiche la photo de proful d'un utilisateur\n
!serverinfo - donne le nom, la date de création, le nombre de membres et le créateur du serveur\n
!poll - permet de créer un sondage\n
!roll - permet de lancer un dé\n
!quote - génère une citation\n
""")


@bot.command()
async def roll(ctx):
    await ctx.send("Tu as lancé un dé et obtenu " + str(random.randint(1, 6)))


@bot.command()
async def quote(ctx):
    citations = [
        "La vie, c’est comme une boîte de chocolats : on ne sait jamais sur quoi on va tomber.",
        "Ce qui ne nous tue pas nous rend plus fort.",
        "Le savoir est une arme. Je suis chargé.",
        "N’abandonne jamais. Parfois, la dernière clé est celle qui ouvre la porte.",
        "Je programme donc je suis.",
        "Tu rates 100% des tirs que tu ne tentes pas.",
        "Le bug n’est pas un problème, c’est une fonctionnalité surprise.",
        "C’est dans le calme qu’on fait les plus grands progrès.",
        "Rien n’est impossible, l’impossible prend juste plus de temps.",
        "Fais-le pour ton futur toi.",
        "Il n’y a pas d’échec, seulement des leçons.",
        "Un bon code, c’est comme une blague : s’il faut l’expliquer, c’est qu’elle est mauvaise.",
        "Toujours viser la lune. Même en cas d’échec, on atterrit dans les étoiles.",
        "Ne rêve pas ta vie, vis ton rêve.",
        "Ton seul vrai ennemi, c’est la flemme.",
        "Si tu veux aller vite, vas-y seul. Si tu veux aller loin, vas-y accompagné.",
        "Ctrl + S sauve des vies.",
        "Pourquoi dormir quand tu peux coder ?",
        "Code dur, dors dur.",
        "Fais de ton mieux, même si personne ne regarde.",
        "Ce n’est pas la machine qui est lente, c’est le code.",
        "Push ton code, pas tes bugs.",
        "Apprends à perdre du temps pour en gagner.",
        "C’est celui qui ose qui réussit.",
        "Sois le développeur que tu rêverais d’avoir dans ton équipe.",
        "Un jour sans coder est un jour perdu. (presque)",
        "Tant qu’il y a du café, il y a de l’espoir.",
        "L’avenir appartient à ceux qui commit tôt.",
        "Debugger, c’est comme être le détective d’un meurtre où tu es le coupable.",
        "La simplicité est la sophistication suprême.",
        "Fais simple, mais pas simpliste.",
        "Les erreurs sont la preuve que tu essaies.",
        "Un petit pas pour l’homme, un grand pas pour le débogage.",
        "Aujourd’hui c’est dur, mais demain t’en rigoleras.",
        "Garde le cap, même si le code rame.",
        "Le temps que tu passes à douter, d’autres avancent.",
        "Le seul code parfait est celui qu’on n’a pas encore écrit.",
        "Ne laisse jamais une ligne de code te manquer de respect.",
        "Réessaie. Échoue. Réessaie mieux.",
        "Derrière chaque grand code, il y a une grande flemme bien gérée.",
        "C’est quand tu veux abandonner qu’il faut persister.",
        "La meilleure façon d’apprendre, c’est de se planter.",
        "Plus t’échoues, plus t’apprends, plus t’es fort.",
        "T’écris pas du code, tu construis des solutions.",
        "Le code n’attend pas, alors bouge.",
        "Il n’y a pas de raccourci vers un code propre.",
        "Reste calme et corrige tes erreurs.",
        "L’ordi fait ce que tu dis, pas ce que tu veux.",
        "Un code lisible vaut mieux qu’un code rapide.",
        "Tu n’es qu’à un `;` de la gloire ou du chaos."
    ]
    citation = random.choice(citations)
    await ctx.send(citation)


@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if member not in ctx.guild.members:
        await ctx.send("Membre inconnu ou ne faisant pas partie du serveur")
        return

    roles_str = get_roles_as_string(member)
    await ctx.send(f"""pseudo: {member.name} 
ID: {member.id}
Date d'arrivée sur le serveur: {member.joined_at.strftime("%d/%m/%Y")}
role: {roles_str}""")


WELCOME_FILE = "welcome_channel.json"


def load_welcome_channel():
    if os.path.exists(WELCOME_FILE):
        with open(WELCOME_FILE, "r") as f:
            return json.load(f)
    return {}


def save_welcome_channels(data):
    with open(WELCOME_FILE, "w") as f:
        json.dump(data, f, indent=4)


@bot.command()
async def setwelcome(ctx, salon: discord.TextChannel):
    guild_id = str(ctx.guild.id)

    welcome_channels[guild_id] = salon.id
    save_welcome_channels(welcome_channels)
    
    await ctx.send(f"Salon de bienvenue défini sur {salon.mention}")


@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    channel_id = welcome_channels.get(guild_id)  # Le canal par défaut du serveur
    if channel_id:
        channel = member.guild.get_channel(channel_id)
        if channel:
            await channel.send(f"Bienvenue {member.mention} ! 🎉")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number=5):
    await ctx.channel.purge(limit=number + 1)
    msg = await ctx.send(f"{number} messages supprimés.")
    await asyncio.sleep(5)
    await msg.delete()


@bot.command()
async def poll(ctx, *, question):
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"sondage: {question}")
    await message.add_reaction("👍")
    await message.add_reaction("👎")


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    name = guild.name
    created_at = guild.created_at.strftime("%d/%m/%Y")
    member_count = guild.member_count
    owner = guild.owner.mention if guild.owner else "Inconnu"

    await ctx.send(
        f"**Nom du serveur: ** {name}\n"
        f"**Date de création: ** {created_at}\n"
        f"**Nombre de membres: ** {member_count}\n"
        f"**Propriétaire: ** {owner}"
    )


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    await ctx.send(f"Avatar de {member.display_name}: {member.display_avatar.url}")


@bot.command()
async def remind(ctx, time: int, msg: str):
    await ctx.send(f"⏰ Rappel créé ! Je te le redirais dans {time} secondes.")
    async def reminder():
        await asyncio.sleep(time)
        await ctx.send(f"🔔 {ctx.author.mention}, voici ton rappel : {msg}")
    asyncio.create_task(reminder())

welcome_channels = {}
welcome_channels.update(load_welcome_channel())
token = os.getenv("TOKEN")
if token:
    bot.run(token)
else:
    print("TOKEN manquant")