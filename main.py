import requests
import json
import discord
from discord import Webhook, Embed
import aiohttp
import asyncio

async def notif(webhookurl, tweet_text):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhookurl, session=session)
        embed = Embed(title="C'est le Buyday!", description=tweet_text)
        await webhook.send(embed=embed, username="Ledger")
        
async def check_twitter_and_notify(webhookurl):
    username = "Ledger"
    url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"

    r = requests.get(url)
    html = r.text

    start_str = '<script id="__NEXT_DATA__" type="application/json">'
    end_str = '</script></body></html>'

    start_index = html.index(start_str) + len(start_str)
    end_index = html.index(end_str, start_index)

    json_str = html[start_index:end_index]
    data = json.loads(json_str)

    for entry in data["props"]["pageProps"]["timeline"]["entries"]:
        tweet_content = entry["content"]["tweet"]

        if tweet_content.get("pinned", False):
            continue
        if "BuyDay" in tweet_content["full_text"]:
            await notif(webhookurl, tweet_content["full_text"])

webhookurl = '{YOUR_WEBHOOK_URL}'
asyncio.run(check_twitter_and_notify(webhookurl))
