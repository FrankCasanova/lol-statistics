import httpx
import json
from pprint import pprint

# url = "https://api.tracker.gg/api/v2/lol/standard/profile/riot/CHADUDYR%23UDYR?region=EUW"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
#     "Accept": "application/json",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Connection": "keep-alive",
# }
# response = httpx.get(url, headers=headers)
# if response.status_code == 200:
#     with open("data.json", "w") as file:
#         json.dump(response.json(), file)
# else:
#     print(f"Error: {response.status_code} - {response.text}")


with open("data.json", "r") as file:
    data = json.load(file)
    pprint(data['data']['segments'][1]['stats']['expDiffPct'])