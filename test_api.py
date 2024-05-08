import asyncio
from curl_cffi.requests import AsyncSession
from asyncio import WindowsSelectorEventLoopPolicy


asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

async def main():
    async with AsyncSession(impersonate='edge101') as client:
        url = "https://api.tracker.gg/api/v2/lol/standard/profile/riot/CHADUDYR%23UDYR?region=EUW"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Dnt": "1",
            "Upgrade-Insecure-Requests": "1",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
        }

        payload = ""

        response = await client.get(url, headers=headers, data=payload,)

        print(response.text)


asyncio.run(main())

# print(response.headers)
# print(response.status_code)
# print(response.cookies)




















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