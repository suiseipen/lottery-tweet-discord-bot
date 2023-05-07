import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import requests
import random

bot = commands.Bot()
token = ""
authorization_key = "Bearer AAAAAAAAAAAAAAAAAAAAAPYXBAAAAAAACLXUNDekMxqa8h%2F40K4moUkGsoc%3DTYfbDKbT3jJPCEVnMYqilB28NHfOPqkca3qaAxGfsyKCs0wRbw"
def guest_key(authorization_key):
    headers = {
        'authorization': authorization_key,
        }
    response = requests.post('https://api.twitter.com/1.1/guest/activate.json', headers=headers)
    guest_token = response.json()["guest_token"]
    return guest_token

def screen_name(user_id):
    headers = {
    'authorization': authorization_key,
    'x-guest-token': guest_key(authorization_key)
    }
    screen_name = requests.get('https://api.twitter.com/1.1/users/show.json?user_id=' + user_id, headers=headers).json()["screen_name"]
    return screen_name

def rt_user(tweet_id):
    api_url = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json?id=' + tweet_id
    headers = {
        'authorization': authorization_key,
        'x-guest-token': guest_key(authorization_key)
        }
        
    data = {
        'cards_platform': 'Web-12',
        'include_cards': 1,
        'include_reply_count': 1,
        'include_user_entities': 0,
        'tweet_mode': 'extended',
        }
        
    tweet_data = requests.get(api_url, data=data, headers=headers).json()
    return tweet_data

class func(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "抽選したいツイートIDを入力",
            timeout=None,
        )

        self.func = nextcord.ui.TextInput(
            label="ツイートID",
            style=nextcord.TextInputStyle.short,
            placeholder="000000",
            required=True,
        )
        self.add_item(self.func)

    async def callback(self, interaction: Interaction) -> None:
        champ = screen_name(str(random.choice(rt_user(self.func.value)["ids"])))
        await interaction.response.send_message(f"https://twitter.com/{champ}\nが選ばれました！")
        return

@bot.slash_command(name="lottery", description="ツイートのRTの中から抽選します")
async def food_slash(interaction: Interaction):
    modal = func()
    await interaction.response.send_modal(modal=modal)

bot.run(token)
