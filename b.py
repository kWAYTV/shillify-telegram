############################IMPORTS################################
import asyncio, time, os, contextlib
from telethon import TelegramClient, errors, sync, events
from telethon.tl.functions.channels import GetFullChannelRequest
from colorama import Fore, Back, Style, init
from dhooks import Webhook, Embed
from datetime import datetime
hook = Webhook("")
automessage = 'Hey! Open a ticket in my discord server for any questions or to get support: discord.gg/kws'
#############################CODE##################################

def slow_type(text, speed, newLine = True):
    for i in text:
        print(i, end = "", flush = True)
        time.sleep(speed)
    if newLine: 
        print()

sCount=0
def rsCount():
    sCount=0

clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

slow_type(Fore.GREEN + "Started!: " + Style.RESET_ALL + "Checking for files...", 0.01)
def check_config():
    if not os.path.isfile('groups.txt'):
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'No groups.txt...', 0.01)
        slow_type('Creating groups.txt...', 0.01)
        open('groups.txt', 'w').close()
        clear()
    if not os.path.isfile('config.txt'):
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'No config.txt...', 0.01)
        slow_type('Creating config.txt...', 0.01)
        open('config.txt', 'w').close()
        clear()
    if not os.path.isfile('message.txt'):
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'No message.txt...', 0.01)
        slow_type('Creating message.txt...', 0.01)
        open('message.txt', 'w').close()
        clear()

check_config()

if os.stat('config.txt').st_size == 0:
    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'config.txt is empty, making one...', 0.01)
    clear()
    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + f"Enter your ApiID:", 0.01)
    apiId = input()
    clear()
    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + f"Enter your ApiHash:", 0.01)
    apiHash = input()
    config = open('config.txt', 'w')
    config.write(apiId + ':' + apiHash)
    config.close()
    clear()

if os.stat('groups.txt').st_size == 0:
    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'groups.txt is empty', 0.01)
    slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + f"Please enter your groups sepparated by commas and without 't.me/' part | Ex: group1, group2, group3: ", 0.01)
    group_list = input()
    group_list = group_list.split(',')
    group_list = [x.strip() for x in group_list]
    with open('groups.txt', 'a') as f:
        for group in group_list:
            f.write(group + '\n')
    clear()

if os.stat('message.txt').st_size == 0:
    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'message.txt is empty', 0.01)
    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'Please enter your message and restart the tool', 0.01)
    time.sleep(5)
    exit()

clear()
slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + f" How long do you want to wait between each message? (seconds): ", 0.01)
wait1 = int(input())
clear()
slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + f" How long do you want to wait after all groups have been messaged? (seconds): ", 0.01)
wait2 = int(input())
clear()
slow_type(Fore.BLUE + "Input: " + Style.RESET_ALL + f"Enter your nickname: ", 0.01)
nickname = input()
clear()


intro = f"""
{Fore.MAGENTA}═══════════════════════════════════════════════════════════════════════════════════════════{Fore.RESET}
 ____ ____ ____ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ ____ ____ 
||S |||h |||i |||l |||l |||i |||f |||y |||       |||T |||e |||l |||e |||g |||r |||a |||m ||
||__|||__|||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|
{Fore.MAGENTA}═══════════════════════════════════════════════════════════════════════════════════════════{Fore.RESET}
"""
logs = f""" 
{Fore.MAGENTA}╭───────────────╮{Fore.RESET}
│ Shillify Logs │  
{Fore.MAGENTA}╰───────────────╯{Fore.RESET}
"""

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
embed = Embed(
description=f'The Ad-Bot has been successfully **started**! :magic_wand:',
color=0x9986a3,
timestamp='now'
)
image1 = 'https://i.imgur.com/Jkg9O7Q.png'
embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
embed.add_field(name='Ad-Bot Started', value=f':magic_wand:')
embed.add_field(name='Time', value=f'{current_time} :clock1:')
embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
embed.set_thumbnail(image1)
hook.send(embed=embed)

clear()
slow_type(intro + Style.RESET_ALL, 0.001)
slow_type("\n" + logs + Style.RESET_ALL, 0.001)

with open("config.txt", "a+") as config:
    config.seek(0)
    cfg = config.read().strip()
    if cfg == "api_id:api_hash":
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Please edit config.txt with your api id and api hash", 0.01)
        time.sleep(3)
        exit()
    else:
        try:
            api_id, api_hash = cfg.split(":")
        except ValueError:
            slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Incorrectly formatted config, make sure your format is api_id:api_hash", 0.01)
            time.sleep(3)
            exit()
        except Exception as e:
            slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Unknown error ({e}), make sure your config is formatted correctly", 0.01)
            time.sleep(3)
            exit()

client = TelegramClient('anon', api_id, api_hash, sequential_updates=True)

groups = open("groups.txt", "r+").read().strip().split("\n")
found_groups = []
message = open("message.txt", "r+").read().strip()

async def x():
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            with contextlib.suppress(Exception):
                inv = await client(GetFullChannelRequest(dialog.id))
                for group in groups:
                        for chat in inv.chats:
                            if chat.username.lower() == group.lower():
                                found_groups.append(f"{chat.username}")

    v = [found_group.lower() for found_group in found_groups]
    for group in groups:
        if group.lower() not in v:
            continue

    slow_type("", 0.00001)

    while True:
        sCount=0
        for found_group in found_groups:
            group = found_group
            try:
                await client.send_message(group, message)
                slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + f" Message sent to {group}, sleeping for {wait1} second(s)", 0.01)
                sCount += 1
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Group {group} has been successfully **messaged**! :white_check_mark:',
                color=0x03fc73,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Ad sent', value=f'{group} :magic_wand:')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(wait1)
            except errors.rpcerrorlist.SlowModeWaitError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to slowmode, sleeping for 300 seconds", 0.01)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Group {group} got **slowmode** error! :x:',
                color=0xff0000,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Slowmode error', value=f'{group} :x:')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(300)
                time.sleep(wait1)
            except errors.rpcerrorlist.ChatWriteForbiddenError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to the account being unable to write in chat, sleeping for 30 seconds", 0.01)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Group {group} got **write forbidden** error! :x:',
                color=0xff0000,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Write forbidden error', value=f'{group} :x:')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(30)
            except errors.rpcerrorlist.ChannelPrivateError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to the channel being private, sleeping for 90 seconds", 0.01)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Group {group} got **private channel** error! :x:',
                color=0xff0000,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Private channel error', value=f'{group} :x:')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(90)
            except errors.rpcerrorlist.FloodWaitError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to flooding, sleeping for 600 seconds", 0.01)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Group {group} got **flood** error! :x:',
                color=0xff0000,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Flood error', value=f'{group} :x:')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(600)
            except errors.rpcerrorlist.UserBannedInChannelError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to account being banned in channel, sleeping for 7200 seconds", 0.01)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Group {group} got **banned** error! :x:',
                color=0xff0000,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Banned error', value=f'{group} :x:')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(7200)
            except errors.rpcerrorlist.ChatRestrictedError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to chat being restricted, sleeping for 30 seconds", 0.01)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Group {group} got **restricted** error! :x:',
                color=0xff0000,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Restricted error', value=f'{group} :x:')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(30)
            except ValueError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to it being non-existent.", 0.01)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Group {group} got **non-existent** error! :x:',
                color=0xff0000,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Non-existent error', value=f'{group} :x:')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(1)
        slow_type(Fore.YELLOW + "Sleep: " + Style.RESET_ALL + f" Sleeping for {wait2} second(s), because all groups have been messaged.", 0.01)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        embed = Embed(
        description='All groups have been **messaged** successfully! :purple_heart:',
        color=0xdce39f,
        timestamp='now'
        )
        image1 = 'https://i.imgur.com/Jkg9O7Q.png'
        embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
        embed.add_field(name='Ad sent', value=f'{group} :magic_wand:')
        embed.add_field(name='Time', value=f'{current_time} :clock1:')
        embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
        embed.set_thumbnail(image1)
        hook.send(embed=embed)
        time.sleep(wait2)


client.start()
client.loop.run_until_complete(x())