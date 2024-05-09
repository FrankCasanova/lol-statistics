
import asyncio  
from selectolax.lexbor import LexborHTMLParser as HTMLParser
import bisect
from curl_cffi.requests import AsyncSession
from setting import MMR_HEADERS, DEFAULT_HEADERS
from asyncio import WindowsSelectorEventLoopPolicy
#TODO:
#URGENT, TRACKER HAS AN API, WE NEED THE WAY TO TAKE THE DATA FROM THE API
#1. install fastapi
#2. install uvicorn
#3. create an endpoint for the tracker
#4. create the frontend

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

def get_rank(mmr):
    thresholds = [125, 250, 375, 500, 625, 750, 875, 1000, 1125, 1250, 1375, 1500, 1625, 1750, 1875, 2000, 2125, 2250, 2375, 2500, 2625, 2750, 2875, 3000, 3125, 3250, 3375, 3500, 4000, 5000]
    ranks = ['iron-iv', 'iron-iii', 'iron-ii', 'iron-i', 'bronze-iv', 'bronze-iii', 'bronze-ii', 'bronze-i', 'silver-iv', 'silver-iii', 'silver-ii', 'silver-i', 'gold-iv', 'gold-iii', 'gold-ii', 'gold-i', 'platinum-iv', 'platinum-iii', 'platinum-ii', 'platinum-i', 'emerald-iv', 'emerald-iii', 'emerald-ii', 'emerald-i', 'diamond-iv', 'diamond-iii', 'diamond-ii', 'diamond-i', 'master', 'grandmaster', 'challenger']

    index = bisect.bisect_right(thresholds, mmr)
    return ranks[index] if index < len(ranks) else 'challenger'

async def mmr(name: str, session: AsyncSession) -> dict:
    try:
        url = f"https://api.mylolmmr.com/api/mmr/euw1/{name}/420".replace('#', '%40').replace(' ', '%20')
        print(f'Establishing connection to {url}...')
        response = await session.get(url, headers=MMR_HEADERS)
        print(f'Connection established, status: {response.status_code}')
        json_data = response.json()
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


async def champ_info(name: str, session: AsyncSession) -> dict[str, str]:
    """
    Returns a dictionary containing the result of getting the champion information from the specified URL.

    Args:
        name (str): The name of the champion.

    Returns:
        dict[str, str]: A dictionary containing the champion information. The keys are 'name', 'win_rate', 'rank', 'lp', 'top_1_used_champ', 'top_2_used_champ', 'main_role', 'player_score', 'kill_participation', 'objetive_participation', and 'xp_diff_vs_enemy'.
    """
    
        
    url = f'https://tracker.gg/lol/profile/riot/EUW/{name}/overview?playlist=RANKED_SOLO_5x5'.replace('#', '%23').replace(' ', '%20')
    print(f'Establishing connection to {url}...')
    response = await session.get(url, headers=DEFAULT_HEADERS)
    print(f'Connection established, status: {response.status_code}')
    html = HTMLParser(response.text)
    
    while not html.css_first('span.fit-text-parent > span'):
        await asyncio.sleep(5)
        html = await session.get(url, helpers=DEFAULT_HEADERS)
        
    
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
        ('objetive_participation', 'div.performance-score > div.performance-score__container > div.performance-score__stats > div:nth-child(3) > div.stat__value'),
        ('xp_diff_vs_enemy', 'div.performance-score > div.performance-score__container > div.performance-score__stats > div:nth-child(4) > div.stat__value'),
        ('profile_image', 'div.user-avatar.user-avatar--large.ph-avatar > img.user-avatar__image'),
        ('rank_image', 'div.trn-profile-highlighted-content__stats > img'),
        ('top_1_used_champ_image', 'div.champions__list > div:nth-child(1) > div.icon.cursor-pointer > img'),
        ('top_2_used_champ_image', 'div.champions__list > div:nth-child(2) > div.icon.cursor-pointer > img'),	
    ]
    
    result = {}
    for key, selector in keys:
        if key == 'rank_image' or key == 'profile_image' or key == 'top_1_used_champ_image' or key == 'top_2_used_champ_image':
            result[key] = html.css_first(selector).attributes['src']
            continue
        try:
            result[key] = html.css_first(selector).text()
        except:
            result[key] = f'{key.capitalize()} Not Found'
    return result
        

    
async def wiki_info(top_1_used_champ: str, session: AsyncSession) -> dict[str, str]:
    """
    Returns a dictionary containing the result of getting the wiki information from the specified URL.

    Args:
        url (str, optional): The URL to get the wiki information from. Defaults to WIKI_URL.

    Returns:
        dict[str, str]: A dictionary containing the wiki information. The keys are 'lore' and the value is a string.
    """
    try:
        url = f'https://leagueoflegends.fandom.com/wiki/{top_1_used_champ}/LoL#Hide_'
        print(f'Establishing connection to {url}...')
        response = await session.get(url, headers=DEFAULT_HEADERS)
        print(f'Connection established, status: {response.status_code}')
        html = HTMLParser(response.text)
        
        lore = html.css_first('div.skinviewer-info-lore > div:nth-child(1)').text()
        
        return {
            'lore': lore
        }
    except:
        return {'error': 'there was some trouble fetching the wiki information'}

    

async def ingsingfull_info(top_1_used_champ: str, session: AsyncSession) -> dict[str, str]:
    """
    Returns a dictionary containing the result of getting the brief summary from the specified URL.

    Args:
        url (str, optional): The URL to get the brief summary from. Defaults to LOLALYTICS_URL.

    Returns:
        dict[str, str]: A dictionary containing the brief summary.
    """
    try:
        url = f'https://lolalytics.com/lol/{top_1_used_champ}/build/'.lower()
        print(f'Establishing connection to {url}...')
        response = await session.get(url, headers=DEFAULT_HEADERS)
        print(f'Connection established, status: {response.status_code}')
        html = HTMLParser(response.text)
        
        brief_summary = html.css_first('div.flex-1 > p').text()
        data_about_champ = html.css_first('div:nth-child(7) > div > h2').text()
        data_about_champ += ' ' + html.css_first('div:nth-child(7) > div > h1').text()
        data_about_champ += ' ' + html.css_first('div:nth-child(7) > div > div > p:nth-child(1)').text()
        data_about_champ += ' ' + html.css_first('div:nth-child(7) > div > div > p:nth-child(2)').text()
        data_about_champ += ' ' + html.css_first('div:nth-child(7) > div > div > p:nth-child(3)').text()
        top_5_best_wr_with_champ = []
        for i in range(5):
            champ_info = {
                'name': html.css_first(f'div:nth-child({i+2}) > div.flex.w-\[100px\].flex-none.items-center.justify-center.truncate > a').text(),
                'wr': html.css_first(f'div:nth-child({i+2}) > div.flex.w-8.flex-none.items-center.justify-center').text(),
                'region': html.css_first(f'div:nth-child({i+2}) > div.w-\[35px\].flex-none > div > div').text()
            }       
            top_5_best_wr_with_champ.append(champ_info)

            
        
        return {
            'brief_summary': brief_summary,
            'data_about_champ': data_about_champ,
            'top_5_best_wr_with_champ': top_5_best_wr_with_champ 
        }
    except:
        return {'error': 'there was some trouble fetching the brief summary'}


async def main(name: str) -> dict[str, dict]:
    try:
        async with AsyncSession(impersonate='edge101') as session:
            champ_info_task = asyncio.create_task(champ_info(name, session))
            champ_info_result = await champ_info_task
            top_1_used_champ = champ_info_result.get('top_1_used_champ', '')

            wiki_info_task = asyncio.create_task(wiki_info(top_1_used_champ, session))
            ingsingfull_info_task = asyncio.create_task(ingsingfull_info(top_1_used_champ, session))
            mmr_task = asyncio.create_task(mmr(name, session))

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
    except Exception as e:
        print(f'An error occurred in the main function: {e}')
        return {}
if __name__ == "__main__":
    print(asyncio.run(main('Twitch Oskr1938#1938')))
