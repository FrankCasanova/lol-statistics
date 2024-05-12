from selectolax.parser import HTMLParser
from curl_cffi.requests import AsyncSession
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from setting import DEFAULT_HEADERS
import pprint

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
session = AsyncSession()

async def tags(name: str, session: AsyncSession) -> dict[str, str]:
    try:
        url = f'https://www.leagueofgraphs.com/summoner/euw/{name.replace(" ", "%20").replace("#", "-")}'
        print(f'Establishing connection to {url}...')
        response = await session.get(url, headers=DEFAULT_HEADERS)
        print(f'Connection established, status: {response.status_code}')
        html = HTMLParser(response.text)
        pprint.pprint(html.text())
        tags = html.css('.tags-box')
        texts = [div.text(deep=True, separator='', strip=True) for div in tags]
        return {
            'tags': texts
        }
    except:
        return {'error': 'there was some trouble fetching the tags'}




asyncio.run(tags('CHADUDYR#UDYR', session))




# import httpx
# import json
# from pprint import pprint

# url = "https://api.tracker.gg/api/v2/lol/standard/profile/riot/CHADUDYR%23UDYR?region=EUW"

# headers = {
    
#    'Accept': '*/*',
#    'User-Agent': 'User-Agent: Thunder Client (https://www.thunderclient.com)',

# }
# response = httpx.get(url, headers=headers)
# if response.status_code == 200:
#     with open("data.json", "w") as file:
#         json.dump(response.json(), file)
# else:
#     print(f"Error: {response.status_code} - {response.text}")

# print(response.json)

# with open("data.json", "r") as file:
#     data = json.load(file)
#     pprint(data['data']['segments'][1]['stats']['expDiffPct'])