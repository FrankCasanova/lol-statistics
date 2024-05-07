import httpx
import asyncio  
from selectolax.lexbor import LexborHTMLParser as HTMLParser
import bisect
from setting import MMR_HEADERS, DEFAULT_HEADERS

#TODO:
#1. install fastapi
#2. install uvicorn
#3. create an endpoint for the tracker
#4. create the frontend



async def get_html(url: str, headers: dict) -> HTMLParser:
    """
    Returns a HTMLParser object for the HTML content of the specified URL.

    Args:
        url (str): The URL to get the HTML from.

    Returns:
        HTMLParser: A HTMLParser object for the HTML content of the specified URL.
    """
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url, headers=headers)
        return HTMLParser(response.text)
    
async def get_json_data(url, headers: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception if the request was unsuccessful
        json_data = response.json()
        return json_data

def get_rank(mmr):
    thresholds = [125, 250, 375, 500, 625, 750, 875, 1000, 1125, 1250, 1375, 1500, 1625, 1750, 1875, 2000, 2125, 2250, 2375, 2500, 2625, 2750, 2875, 3000, 3125, 3250, 3375, 3500, 4000, 5000]
    ranks = ['iron-iv', 'iron-iii', 'iron-ii', 'iron-i', 'bronze-iv', 'bronze-iii', 'bronze-ii', 'bronze-i', 'silver-iv', 'silver-iii', 'silver-ii', 'silver-i', 'gold-iv', 'gold-iii', 'gold-ii', 'gold-i', 'platinum-iv', 'platinum-iii', 'platinum-ii', 'platinum-i', 'emerald-iv', 'emerald-iii', 'emerald-ii', 'emerald-i', 'diamond-iv', 'diamond-iii', 'diamond-ii', 'diamond-i', 'master', 'grandmaster', 'challenger']

    index = bisect.bisect_right(thresholds, mmr)
    return ranks[index] if index < len(ranks) else 'challenger'

async def mmr(name: str):
    try:
        url = f"https://api.mylolmmr.com/api/mmr/euw1/{name}/420".replace('#', '%40').replace(' ', '%20')
        json_data = await get_json_data(url, MMR_HEADERS)
        mmr = json_data["mmr"]
        rank = get_rank(mmr)
        return {
            'mmr': mmr,
            'rank': rank
        }
    except:
        return {
            'error': 'there was some trouble fetching the mmr'
        }


async def champ_info(name: str) -> dict[str, str]:
    """
    Returns a dictionary containing the result of getting the champion information from the specified URL.

    Args:
        name (str): The name of the champion.

    Returns:
        dict[str, str]: A dictionary containing the champion information. The keys are 'name', 'win_rate', 'rank', 'lp', 'top_1_used_champ', 'top_2_used_champ', 'main_role', 'player_score', 'kill_participation', 'objetive_participation', and 'xp_diff_vs_enemy'.
    """
    retry_count = 3
    while retry_count > 0:
        
        url = f'https://tracker.gg/lol/profile/riot/EUW/{name}/overview?playlist=RANKED_SOLO_5x5'.replace('#', '%23').replace(' ', '%20')
        html = await get_html(url, DEFAULT_HEADERS)
        
        if not html.css_first('span.fit-text-parent > span'):
            retry_count -= 1
            continue
        else:
            break
    
    
    keys = [
        ('name', 'span.fit-text-parent > span'),
        ('win_rate', 'div.trn-profile-highlighted-content__stats > div:nth-child(3) > span.stat__value'),
        ('rank', 'div.trn-profile-highlighted-content__stats > div:nth-child(2) > span.stat__label'),
        ('lp', 'div.trn-profile-highlighted-content__stats > div:nth-child(2) > span.stat__value'),
        ('top_1_used_champ', 'div.champions__list > div:nth-child(1) > div.info > div.left > div.name'),
        ('top_2_used_champ', 'div.champions__list > div:nth-child(2) > div.info > div.left > div.name'),
        ('main_role', 'div > div.role__wr > div.role__role'),
        ('player_score', 'div.score__text > div.value'),
        ('kill_participation', 'div.performance-score__stats > div:nth-child(2) > div.stat__value'),
        ('objetive_participation', '#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.trn-grid.content > div.performance-score > div.performance-score__container > div.performance-score__stats > div:nth-child(3) > div.stat__value'),
        ('xp_diff_vs_enemy', '#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.trn-grid.content > div.performance-score > div.performance-score__container > div.performance-score__stats > div:nth-child(4) > div.stat__value'),
    ]
    
    result = {}
    for key, selector in keys:
        try:
            result[key] = html.css_first(selector).text()
        except:
            result[key] = f'{key.capitalize()} Not Found'
    result['rank_image'] = f'https://trackercdn.com/cdn/tracker.gg/lol/ranks/2022/{result["rank"].lower().split()[0]}.png'
    return result
        

    
async def wiki_info(top_1_used_champ: str) -> dict[str, str]:
    """
    Returns a dictionary containing the result of getting the wiki information from the specified URL.

    Args:
        url (str, optional): The URL to get the wiki information from. Defaults to WIKI_URL.

    Returns:
        dict[str, str]: A dictionary containing the wiki information. The keys are 'lore' and the value is a string.
    """
    try:
        url = f'https://leagueoflegends.fandom.com/wiki/{top_1_used_champ}/LoL#Hide_'
        print(url)
        html = await get_html(url, DEFAULT_HEADERS)
        
        lore = html.css_first('div.skinviewer-info-lore > div:nth-child(1)').text()
        
        return {
            'lore': lore
        }
    except:
        return {'error': 'there was some trouble fetching the wiki information'}

    

async def ingsingfull_info(top_1_used_champ: str) -> dict[str, str]:
    """
    Returns a dictionary containing the result of getting the brief summary from the specified URL.

    Args:
        url (str, optional): The URL to get the brief summary from. Defaults to LOLALYTICS_URL.

    Returns:
        dict[str, str]: A dictionary containing the brief summary.
    """
    try:
        url = f'https://lolalytics.com/lol/{top_1_used_champ}/build/'.lower()
        print(url)
        html = await get_html(url, DEFAULT_HEADERS)
        brief_summary = html.css_first('div.flex-1 > p').text()
        
        return {
            'brief_summary': brief_summary 
        }
    except:
        return {'error': 'there was some trouble fetching the brief summary'}


async def main(name: str) -> dict[str, dict]:
    """
    Returns a dictionary containing the results of the following async functions:
    - champ_info
    - mmr
    - wiki_info
    - ingsingfull_info

    Each value in the dictionary is a dictionary itself, representing the return value of the corresponding async function.

    The return type of this function is `dict[str, dict]`. The keys of the outer dictionary are
    the names of the async functions, and the values are the return values of each function.
    """
    
    champ_info_task = asyncio.create_task(champ_info(name))
    champ_info_result = await champ_info_task
    top_1_used_champ = champ_info_result.get('top_1_used_champ', '')

    wiki_info_task = asyncio.create_task(wiki_info(top_1_used_champ))
    ingsingfull_info_task = asyncio.create_task(ingsingfull_info(top_1_used_champ))
    mmr_task = asyncio.create_task(mmr(name))

    results = await asyncio.gather(wiki_info_task, ingsingfull_info_task, mmr_task)

    wiki_info_result = results[0]
    ingsingfull_info_result = results[1]
    mmr_result = results[2]

    return {
        'champ_info': champ_info_result,
        'wiki_info': wiki_info_result,
        'ingsingfull_info': ingsingfull_info_result,
        'mmr': mmr_result,
    }
       
if __name__ == "__main__":
    print(asyncio.run(main('CHADUDYR#UDYR')))
