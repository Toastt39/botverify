from sre_parse import State
import nextcord, config, json
import os
import asyncio
from datetime import datetime, timedelta, timezone
from nextcord.ui import Button, View
from nextcord.ext import commands
from myserver import server_on


bot = commands.Bot(
    command_prefix='.',
    help_command=None,
    intents=nextcord.Intents.all(),
    strip_after_prefix=True,
    case_insensitive=True
)


bangkok_tz = timezone(timedelta(hours=7))
current_time_in_bangkok = datetime.now(bangkok_tz)
roles_to_add = config.roleIds

class ButtonVerify(nextcord.ui.View):

    def __init__(self, roles_to_add):
        super().__init__(timeout=None)
        self.roles_to_add = roles_to_add

    @nextcord.ui.button(
        label='กดเพื่อยืนยันตัวตน',
        custom_id='giverole',
        style=nextcord.ButtonStyle.green,
        emoji='<a:11616992290021212371:1175381633814237184>',
    )
    async def giverole(self, button: nextcord.Button, interaction: nextcord.Interaction):
        try:
            await interaction.response.send_message(content='ยืนยันตัวตนสำเร็จเรียบร้อย', ephemeral=True)
            member = interaction.guild.get_member(interaction.user.id)
            roles = [interaction.guild.get_role(role_id) for role_id in self.roles_to_add]

            for role in roles:
                if role is None:
                    await interaction.response.send_message(content='พบปัญหาในการเพิ่มบทบาท: บทบาทไม่ถูกต้อง', ephemeral=True)
                    return

            await member.add_roles(*roles)

            embed = nextcord.Embed(
                description=f'''
> `✅`︱รับยศ สำเร็จ

> `👑`︱User {interaction.user.name}#{interaction.user.discriminator}

> `⏰`︱Time {datetime.now(bangkok_tz).strftime('%d/%m/%Y %H:%M:%S')}
''',
                color=nextcord.Color.from_rgb(76, 63, 50)
            )
            embed.set_thumbnail(url=interaction.user.display_avatar.url if interaction.user.display_avatar else None)
            await bot.get_channel(config.channelLog).send(embed=embed)
        except nextcord.errors.Forbidden:
            await interaction.response.send_message(content='บอทไม่มีสิทธิ์ในการเพิ่มบทบาท', ephemeral=True)


@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game(name="พร้อมใช้งาน 💚"))
    bot.add_view(ButtonVerify(roles_to_add=config.roleIds))


@bot.event
async def on_message(message):
    if message.channel.id == config.channelVfy and '.' in message.content:
        member = message.guild.get_member(message.author.id)
        roles = [message.guild.get_role(role_id) for role_id in roles_to_add]
        await member.add_roles(*roles)

        # สร้าง embed พร้อมกับเวลาในเขตเวลา Bangkok
        embed = nextcord.Embed(
            description=f'''
> `✅`︱รับยศ สำเร็จ

> `👑`︱User {message.author.name}#{message.author.discriminator}

> `⏰`︱Time {datetime.now(bangkok_tz).strftime('%d/%m/%Y %H:%M:%S')}
''',
            color=nextcord.Color.from_rgb(76, 63, 50)
        )

        embed.set_image(url='')
        embed.set_thumbnail(url=message.author.display_avatar.url if message.author.display_avatar else None)

        await bot.get_channel(config.channelLog).send(embed=embed)

    await bot.process_commands(message)


@bot.slash_command(
    name='setup-help',
    description='📌︱ตั้งระบบช่วยเหลือ︱คำสั่งนี้สำหรับผู้ดูเเลระบบเท่านั้น',
    guild_ids=[config.serverId]
)
async def setuphelp(interaction: nextcord.Interaction):
    if (interaction.user.id not in config.ownerIds):
        return await interaction.response.send_message(content='[ERROR] สมาชิกไม่มีสิทธิ์เข้าถึงคำสั่งนี้', ephemeral=True)
    embedhelp = nextcord.Embed()
    embedhelp.title = f"`☕` : BOT VERIFICATION"
    embedhelp.description = f'''
ㅤ
> ยินดีต้อนรับสมาชิกที่เข้ามา สำหรับพิมพ์จุดเพื่อรับยศ

> ช่องสำหรับ กรณีที่ไม่สามารถกดปุ่มเพื่อยืนยันตัวตน

> พิมพ์เเค่ . ยืนยันตัวตนเท่านั้นห้ามพิมพ์เเชทในนี้
'''
    embedhelp.set_image(url='https://i.pinimg.com/564x/58/00/3d/58003d6611095b3473566cb14bd34ea8.jpg')
    embedhelp.set_footer(text="© MADE BY  :  ._toastt")
    embedhelp.color = nextcord.Color.from_rgb(76, 63, 50)
    await interaction.channel.send(embed=embedhelp)
    await interaction.response.send_message(content='[SUCCESS] ตั้งค่าระบบสำเร็จเรียบร้อย', ephemeral=True)


@bot.slash_command(
    name='setup-verify',
    description='📌︱ตั้งระบบกดยืนยัน︱คำสั่งนี้สำหรับผู้ดูเเลระบบเท่านั้น',
    guild_ids=[config.serverId]
)
async def setupverify(interaction: nextcord.Interaction):
    if (interaction.user.id not in config.ownerIds):
        return await interaction.response.send_message(content='[ERROR] สมาชิกไม่มีสิทธิ์เข้าถึงคำสั่งนี้', ephemeral=True)
    embedsetup = nextcord.Embed()
    embedsetup.title = f"`🍞` : BOT VERIFICATION"
    embedsetup.description = f'> ```ยินดีต้อนรับสมาชิกที่เข้ามาใหม่ กดปุ่มด้านล่างเพื่่อยืนยันตัวตน```'
    embedsetup.set_image(url='https://i.pinimg.com/originals/84/f1/ef/84f1efd20bc2f224979bdc955ef6cb35.gif')
    embedsetup.set_footer(text="© MADE BY  :  ._toastt")
    embedsetup.color = nextcord.Color.yellow()
    await interaction.channel.send(embed=embedsetup, view=ButtonVerify(roles_to_add=config.roleIds))
    await interaction.response.send_message(content='[SUCCESS] ตั้งค่าระบบสำเร็จเรียบร้อย', ephemeral=True)
    

server_on()

bot.run(os.getenv('TOKEN'))