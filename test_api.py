from curl_cffi import requests


url = "https://api.tracker.gg/api/v2/lol/standard/profile/riot/CHADUDYR%23UDYR?region=EUW"


# headers = {
#     "cookie": "__cf_bm=aLfEOsXLW7ZBqAa5nP2.TW2R8O__j6bFSztgxtqo7MY-1715162182-1.0.1.1-rPjfYz74f8mgO3YtMAFce.UobGlySK5vjho_1RmGMN67LzPpuaBIRF0JaimpPZEpFSulzcmibRhJK91m1aEk6TmVlOYJGdl3cEAtsVFmlAg; cf_clearance=OPWcBgzFnqc4gTyJyOkgFaGHg_J2r_alPVDBq4u1FC8-1715162182-1.0.1.1-oncx1uuzDhK3HrGPaOuHWC8kIs2EIjLILG96vdfWjV_C7E89J6Yluq3ZlYyNLwE.r.FyunIRsGynd88tNbf55w; _ga=GA1.1.439411161.1715162175; session_id=a531145f-1969-4bc3-95f7-f9d8f8d18a7f; X-Mapping-Server=s12; __cflb=02DiuFQAkRrzD1P1mdm8JatZXtAyjoPD2CUUKCN3AcQSQ; _sharedid=cfa5acfb-b156-4367-b829-bb27ae70ef7e; _ga_HWSV72GK8X=GS1.1.1715162175.1.1.1715162199.0.0.0",
#     "accept": "application/json, text/plain, */*",
#     "accept-language": "en-US,en;q=0.9",
#     "dnt": "1",
#     "origin": "https://tracker.gg",
#     "priority": "u=1, i",
#     "referer": "https://tracker.gg/",
#     "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-site",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
# }

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


response = requests.request("GET", url, data=payload,impersonate='edge101')

# print(response.text)
print(response.headers)
print(response.status_code)
print(response.cookies)




















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