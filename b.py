############################IMPORTS################################
import asyncio, time, os, contextlib
from telethon import TelegramClient
from telethon import events, errors, functions
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest, LeaveChannelRequest
from colorama import Fore, Back, Style, init
from dhooks import Webhook, Embed
from datetime import datetime
############################SETTINGS###############################
 ## ALL OF THE SETTINGS ARE REQUIRED TO BE FILLED IN ##
wait1 = 0  # How long to wait between sending each message (seconds)
wait2 = 0 # How long to wait to start again after all groups have been messaged (seconds)
nickname = "" # Main account username for notification purposes
webhook_url= ""  # For logging purposes
automessage = '' # Auto message to respond when you are afk
trackgroups = {"", ""} # Group(s) to keep track if the scrip still running
#############################CODE##################################

# Slow type function
def slow_type(text, speed, newLine = True):
    for i in text:
        print(i, end = "", flush = True)
        time.sleep(speed)
    if newLine: 
        print()

# Counter and reset counter
sCount=0
def rsCount():
    sCount=0

# Clear screen function
clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clear()

# Checking for files
slow_type(Fore.GREEN + "Started!: " + Style.RESET_ALL + "Checking for files...", 0.0001)
def check_config():
    if not os.path.isfile('groups.txt'):
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'No groups.txt...', 0.0001)
        slow_type('Creating groups.txt...', 0.0001)
        open('groups.txt', 'w').close()
        clear()
    if not os.path.isfile('config.txt'):
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'No config.txt...', 0.0001)
        slow_type('Creating config.txt...', 0.0001)
        open('config.txt', 'w').close()
        clear()
    if not os.path.isfile('message.txt'):
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'No message.txt...', 0.0001)
        slow_type('Creating message.txt...', 0.0001)
        open('message.txt', 'w').close()
        clear()

check_config()

# Checking if filled
if os.stat('config.txt').st_size == 0:
    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'config.txt is empty, making one...', 0.0001)
    clear()
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f"Enter your ApiID:", 0.0001)
    apiId = input()
    clear()
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f"Enter your ApiHash:", 0.0001)
    apiHash = input()
    config = open('config.txt', 'w')
    config.write(apiId + ':' + apiHash)
    config.close()
    clear()

if os.stat('groups.txt').st_size == 0:
    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'groups.txt is empty', 0.0001)
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f"Please enter your groups separated by commas and without 't.me/' part | Ex: group1, group2, group3: ", 0.0001)
    group_list = input()
    group_list = group_list.split(',')
    group_list = [x.strip() for x in group_list]
    with open('groups.txt', 'a') as f:
        for group in group_list:
            f.write(group + '\n')
    clear()

if os.stat('message.txt').st_size == 0:
    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'message.txt is empty', 0.0001)
    slow_type(Fore.RED + "Error: " + Style.RESET_ALL + 'Please enter your message and restart the tool', 0.0001)
    time.sleep(5)
    exit()

if not wait1 or wait1 == 0:
    clear()
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f" How long do you want to wait between each message? (seconds): ", 0.0001)
    wait1 = int(input())
    clear()

if not wait2 or wait2 == 0:
    clear()
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f" How long do you want to wait after all groups have been messaged? (seconds): ", 0.0001)
    wait2 = int(input())
    clear()

if not nickname:
    clear()
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f"Enter your telegram username (for notifications): ", 0.0001)
    nickname = input()
    clear()

if not webhook_url:
    clear()
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f"Enter your discord webhook url: ", 0.0001)
    webhook_url = input()
    clear()

if not automessage:
    clear()
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f"Enter your auto message: ", 0.0001)
    automessage = input()
    clear()

if not trackgroups:
    clear()
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f"Enter your track groups separated by commas and without 't.me/' part | Ex: group1, group2, group3: ", 0.0001)
    trackgroups = input()
    trackgroups = trackgroups.split(',')
    trackgroups = [x.strip() for x in trackgroups]
    clear()

# Logo
intro = f"""
{Fore.MAGENTA}═══════════════════════════════════════════════════════════════════════════════════════════{Fore.RESET}
 ____ ____ ____ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ ____ ____ 
||S |||h |||i |||l |||l |||i |||f |||y |||       |||T |||e |||l |||e |||g |||r |||a |||m ||
||__|||__|||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|

https://github.com/kWAYTV/
{Fore.MAGENTA}═══════════════════════════════════════════════════════════════════════════════════════════{Fore.RESET}
"""
logs = f""" 
{Fore.MAGENTA}╭───────────────╮{Fore.RESET}
│ Shillify Logs │  
{Fore.MAGENTA}╰───────────────╯{Fore.RESET}
"""

# Start webhook
hook = Webhook(webhook_url)  # Discord embed logs
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

# Load API Data
with open("config.txt", "a+") as config:
    config.seek(0)
    cfg = config.read().strip()
    if cfg == "api_id:api_hash":
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Please edit config.txt with your api id and api hash", 0.0001)
        time.sleep(3)
        exit()
    else:
        try:
            api_id, api_hash = cfg.split(":")
        except ValueError:
            slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Incorrectly formatted config, make sure your format is api_id:api_hash", 0.0001)
            time.sleep(3)
            exit()
        except Exception as e:
            slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Unknown error ({e}), make sure your config is formatted correctly", 0.0001)
            time.sleep(3)
            exit()

# Define client
client = TelegramClient('anon', api_id, api_hash, sequential_updates=True)

# Load files
groups = open("groups.txt", "r+").read().strip().split("\n")
error_groups = open("error_groups.txt", "w")
message = open("message.txt", "r+").read().strip()
slow_type(Fore.BLUE + "Found " + Style.RESET_ALL + f"{len(groups)} groups in groups.txt", 0.0001)
found_groups = []
messaged_groups = []

# Join function
async def join():
    seen = []
	
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f" Do you want to join groups? (y/n): ", 0.0001)
    option = input()
    if option == "" or "n" in option: return
    print()
    
    for invite in groups:
        if invite in seen: continue
        seen.append(seen)
        
        while True:
            try:
                if "t.me" in invite: code = invite.split("t.me/")[1]
                else: code = invite
                
                await client(JoinChannelRequest(code))
                slow_type(Fore.GREEN + "OK: " + Style.RESET_ALL + "Joined group: " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Joined group: {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Joined Group', value=f'{invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
            except errors.FloodWaitError as e:
                slow_type(Fore.YELLOW + "RATE: " + Style.RESET_ALL + "Ratelimited for " + str(e.seconds) + " seconds", 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Ratelimited for {str(e.seconds)} seconds',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Ratelimited', value=f'{str(e.seconds)} seconds')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                await asyncio.sleep(int(e.seconds))
            except errors.ChannelsTooMuchError as e:
                slow_type(Fore.RED + "ERROR: " + Style.RESET_ALL + "You have joined too many groups", 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'You have joined too many groups',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Error', value=f'You have joined too many groups')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(3)
                exit()
            except errors.ChannelInvalidError as e:
                slow_type(Fore.RED + "ERROR: " + Style.RESET_ALL + "Invalid invite link: " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Invalid invite link: {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Error', value=f'Invalid invite link: {invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
            except errors.ChannelPrivateError as e:
                slow_type(Fore.RED + "ERROR: " + Style.RESET_ALL + "Private group: " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Private group: {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Error', value=f'Private group: {invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
            except Exception:
                slow_type(Fore.RED + "FAIL: " + Style.RESET_ALL + "Failed to join group: " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Failed to join group: {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Failed to join group', value=f'{invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
        await asyncio.sleep(0.8)

# Leave function
async def leave():
    seen = []
	
    slow_type(Fore.CYAN + "Input: " + Style.RESET_ALL + f" Do you want to leave groups? (y/n): ", 0.0001)
    option = input()
    if option == "" or "n" in option: return
    print()
    
    for invite in groups:
        if invite in seen: continue
        seen.append(seen)
        
        while True:
            try:
                if "t.me" in invite: code = invite.split("t.me/")[1]
                else: code = invite
                
                await client(LeaveChannelRequest(code))
                slow_type(Fore.GREEN + "OK: " + Style.RESET_ALL + "Left group: " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Joined group: {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Left Group', value=f'{invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
            except errors.FloodWaitError as e:
                slow_type(Fore.YELLOW + "RATE: " + Style.RESET_ALL + "Ratelimited for " + str(e.seconds) + " seconds", 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Ratelimited for {str(e.seconds)} seconds',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Ratelimited', value=f'{str(e.seconds)} seconds')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
            except errors.ChannelInvalidError as e:
                slow_type(Fore.RED + "FAIL: " + Style.RESET_ALL + "Failed to leave group (channel invalid): " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Failed to leave group (channel invalid): {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Failed to leave group (channel invalid)', value=f'{invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
            except errors.ChannelPrivateError as e:
                slow_type(Fore.RED + "FAIL: " + Style.RESET_ALL + "Failed to leave group (channel private): " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Failed to leave group (channel private): {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Failed to leave group (channel private)', value=f'{invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
            except errors.ChannelPublicGroupNaError as e:
                slow_type(Fore.RED + "FAIL: " + Style.RESET_ALL + "Failed to leave group (not avaiable): " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Failed to leave group (not avaiable): {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Failed to leave group (not avaiable)', value=f'{invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
            except errors.UserCreatorError as e:
                slow_type(Fore.RED + "FAIL: " + Style.RESET_ALL + "Failed to leave group (you are the owner): " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Failed to leave group (you are the owner): {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Failed to leave group (you are the owner)', value=f'{invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
            except errors.UserNotParticipantError as e:
                slow_type(Fore.RED + "FAIL: " + Style.RESET_ALL + "Failed to leave group (you are not a member): " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Failed to leave group (you are not a member): {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Failed to leave group (you are not a member)', value=f'{invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
            except Exception as e:
                slow_type(Fore.RED + "FAIL: " + Style.RESET_ALL + "Failed to leave group: " + invite, 0.0001)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                embed = Embed(
                description=f'Failed to leave group: {invite}',
                color=0x9986a3,
                timestamp='now'
                )
                image1 = 'https://i.imgur.com/Jkg9O7Q.png'
                embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
                embed.add_field(name='Failed to leave group', value=f'{invite}')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                break
        await asyncio.sleep(0.8)

# Advertise function
async def shill():
    async for dialog in client.iter_dialogs(limit = None):
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
            slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f"Couldn't find group {group} in your account.", 0.0001)
            with open("error_groups.txt", "a") as f:
                f.write(f"{group} - Not found\n")
            continue

    slow_type("", 0.00001)

    while True:
        sCount=0
        slow_type(Fore.BLUE + "Sending message to " + Style.RESET_ALL + f"{len(found_groups)} groups", 0.0001)
        await client.send_message(f'{nickname}', f'**Started sending messages to {len(found_groups)} groups**')
        for found_group in found_groups: 
            group = found_group
            try:
                if group in messaged_groups:
                    slow_type(Fore.YELLOW + "SKIP: " + Style.RESET_ALL + f"Group {group} has already been messaged.", 0.0001)
                    continue
                else:
                    messaged_groups.append(group)
                await client.send_message(group, message)
                slow_type(Fore.GREEN + "Success: " + Style.RESET_ALL + f" Message sent to {group}, sleeping for {wait1} second(s)", 0.0001)
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
                embed.add_field(name='Group', value=f'{group} :magic_wand:')
                embed.add_field(name='Time', value=f'{current_time} :clock1:')
                embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
                embed.set_thumbnail(image1)
                hook.send(embed=embed)
                time.sleep(wait1)
            except errors.rpcerrorlist.SlowModeWaitError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to slowmode, sleeping for 300 seconds", 0.0001)
                with open("error_groups.txt", "w") as f:
                    f.write(f"{group} - Slow Mode\n")
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
                continue
            except errors.rpcerrorlist.ChatWriteForbiddenError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to the account being unable to write in chat, sleeping for 30 seconds", 0.0001)
                with open("error_groups.txt", "w") as f:
                    f.write(f"{group} - Write Forbidden\n")
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
                continue
            except errors.rpcerrorlist.ChannelPrivateError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to the channel being private, sleeping for 90 seconds", 0.0001)
                with open("error_groups.txt", "w") as f:
                    f.write(f"{group} - Channel Private\n")
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
                continue
            except errors.rpcerrorlist.FloodWaitError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to flooding, sleeping for 600 seconds", 0.0001)
                with open("error_groups.txt", "w") as f:
                    f.write(f"{group} - Flood\n")
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
                continue
            except errors.rpcerrorlist.UserBannedInChannelError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to account being banned in channel, sleeping for {wait1} seconds", 0.0001)
                with open("error_groups.txt", "w") as f:
                    f.write(f"{group} - Banned in channel\n")
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
                time.sleep(wait1)
                continue
            except errors.rpcerrorlist.ChatRestrictedError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to chat being restricted, sleeping for 30 seconds", 0.0001)
                with open("error_groups.txt", "w") as f:
                    f.write(f"{group} - Chat restricted\n")
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
                continue
            except ValueError:
                slow_type(Fore.RED + "Error: " + Style.RESET_ALL + f" Failed to send to channel {group}, due to it being non-existent.", 0.0001)
                with open("error_groups.txt", "w") as f:
                    f.write(f"{group} - Non-existent\n")
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
                continue
        for group in trackgroups:
            if group not in messaged_groups:
                await client.send_message(group, message)
            else:
                continue
        slow_type(Fore.YELLOW + "Sleep: " + Style.RESET_ALL + f" Sleeping for {wait2} second(s), because all groups have been messaged.", 0.0001)
        await client.send_message(f'{nickname}', f'✅ Finished advertising! \n🕛Sleeping for {wait2} seconds(s)')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        embed = Embed(
        description='All groups have been **messaged** successfully! :purple_heart:',
        color=0xdce39f,
        timestamp='now'
        )
        image1 = 'https://i.imgur.com/Jkg9O7Q.png'
        embed.set_author(name='Telegram Ad-Bot', icon_url=image1)
        embed.add_field(name='W Groups', value=f'{sCount} :magic_wand:')
        embed.add_field(name='Time', value=f'{current_time} :clock1:')
        embed.set_footer(text=f'Telegram Ad-Bot | {nickname}', icon_url=image1)
        embed.set_thumbnail(image1)
        hook.send(embed=embed)
        time.sleep(wait2)

# Start function
async def start():
    try:
        await client.start()
        await client.send_message(f'{nickname}', f'🚀Adbot powered **on**! \nFound {len(groups)} groups in the file.\nStarting up...')
        await join()
        await leave()
        await shill()
    except Exception as e:
        slow_type(Fore.RED + "Error: " + Style.RESET_ALL + str(e), 0.0001)
        time.sleep(3)
        exit()

# Autoresponse
@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if event.is_private:
        from_ = await event.client.get_entity(event.from_id)
        if not from_.bot:
            slow_type(Fore.MAGENTA + f"Autoreplying...: {Fore.RESET} -  Time: {time.asctime()} - Event: {event.message}.", 0.00001)
            time.sleep(1)
            await event.respond(automessage)

# Run the client
client.loop.run_until_complete(start())