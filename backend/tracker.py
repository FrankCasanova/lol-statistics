
import asyncio  
from selectolax.lexbor import LexborHTMLParser as HTMLParser
import bisect
from curl_cffi.requests import AsyncSession
from .setting import *
# from asyncio import WindowsSelectorEventLoopPolicy


# asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

def get_rank(mmr):

    index = bisect.bisect_right(TRESHOLDS, mmr)
    return RANKS[index] if index < len(RANKS) else 'challenger'

async def mmr(name: str, session: AsyncSession) -> dict:
    url = f"{URL_MMR}{name}/420".replace('#', '%40').replace(' ', '%20')
    response = await session.get(url, headers=MMR_HEADERS)
    json_data =  response.json()
    mmr = json_data.get("mmr")
    return {
        'mmr': mmr if mmr is not None else 0,
        'rank': get_rank(mmr) if mmr is not None else 'n/a'
    }


async def champ_info(name: str, session: AsyncSession) -> dict[str, str]:
    """
    Returns a dictionary containing the result of getting the champion information from the specified URL.

    Args:
        name (str): The name of the champion.

    Returns:
        dict[str, str]: A dictionary containing the champion information. The keys are 'name', 'win_rate', 'rank', 'lp', 'top_1_used_champ', 'top_2_used_champ', 'main_role', 'player_score', 'kill_participation', 'objetive_participation', and 'xp_diff_vs_enemy'.
    """
    
    url = f"{URL_CHAMP_INFO}{name}/overview?playlist=RANKED_SOLO_5x5".replace('#', '%23').replace(' ', '%20')

    # print(f'Establishing connection to {url}...')
    response = await session.get(url, headers=DEFAULT_HEADERS)  
    # print(f'Connection established, status: {response.status_code}')
    html = HTMLParser(response.text)
    
    while not html.css_first('span.fit-text-parent > span'):
        await asyncio.sleep(5)
        html = await session.get(url, helpers=DEFAULT_HEADERS)
        
    
    selectors = {
        'name': 'span.fit-text-parent > span',
        'win_rate': 'div.trn-profile-highlighted-content__stats > div:nth-child(3) > span.stat__value',
        'rank': 'div.trn-profile-highlighted-content__stats > div:nth-child(2) > span.stat__label',
        'lp': 'div.trn-profile-highlighted-content__stats > div:nth-child(2) > span.stat__value',
        'top_1_used_champ': 'div.champions__list > div:nth-child(1) > div.info > div.left > div.name',
        'top_2_used_champ': 'div.champions__list > div:nth-child(2) > div.info > div.left > div.name',
        'main_role': 'div > div.role__wr > div.role__role',
        'player_score': 'div.score__text > div.value',
        'kill_participation': 'div.performance-score__stats > div:nth-child(2) > div.stat__value',
        'objective_participation': 'div.performance-score > div.performance-score__container > div.performance-score__stats > div:nth-child(3) > div.stat__value',
        'xp_diff_vs_enemy': 'div.performance-score > div.performance-score__container > div.performance-score__stats > div:nth-child(4) > div.stat__value',
        'profile_image': 'div.user-avatar.user-avatar--large.ph-avatar > img.user-avatar__image',
        'rank_image': 'div.trn-profile-highlighted-content__stats > img',
        'top_1_used_champ_image': 'div.champions__list > div:nth-child(1) > div.icon.cursor-pointer > img',
        'top_2_used_champ_image': 'div.champions__list > div:nth-child(2) > div.icon.cursor-pointer > img',
    }
    
    result = {}
    for key, selector in selectors.items():
        try:
            if 'image' in key:
                element = html.css_first(selector)
                result[key] = element.attributes['src'] if element else 'https://salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png'
            else:
                result[key] = html.css_first(selector).text()
        except AttributeError:
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
        url = f'{URL_WIKI}{top_1_used_champ.replace(" ", "_")}/LoL#Hide_'
        # print(f'Establishing connection to {url}...')
        response = await session.get(url, headers=DEFAULT_HEADERS)
        # print(f'Connection established, status: {response.status_code}')
        html = HTMLParser(response.text)
        
        lore = html.css_first('div.skinviewer-info-lore > div:nth-child(1)').text()
        
        return {
            'lore': lore
        }
    except:
        return {
            'lore': 'Lore Not Found'	
        }

    

async def ingsingfull_info(top_1_used_champ: str, session: AsyncSession) -> dict[str, str]:
    """
    Returns a dictionary containing the result of getting the brief summary from the specified URL.

    Args:
        url (str, optional): The URL to get the brief summary from. Defaults to LOLALYTICS_URL.

    Returns:
        dict[str, str]: A dictionary containing the brief summary.
    """
    try:
        url = f'{URL_INGSINGFULL_INFO}{top_1_used_champ.lower().replace(" ", "")}/build/'
        # print(f'Establishing connection to {url}...')
        response = await session.get(url, headers=DEFAULT_HEADERS)
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
        return {'brief_summary': 'n/a',
                'data_about_champ': 'n/a',
                'top_5_best_wr_with_champ': [{'name': 'n/a', 'wr': 'n/a', 'region': 'n/a'}]}


async def ladder_rank(name: str, session: AsyncSession) -> dict[str, str]:
    try:
        url = f'{URL_LADDER_RANK}{name.replace(" ", "%20").replace("#", "-")}'
        # print(f'Establishing connection to {url}...')
        response = await session.get(url, headers=DEFAULT_HEADERS)
        html = HTMLParser(response.text)
        ladder_rank = html.css_first('div.info > div.team-and-rank > div.rank > a').text()
        return {'ladder_rank': ladder_rank}
    except:
        return {'ladder_rank': 'n/a'}

async def mastery(name: str, session: AsyncSession) -> dict:
    try:
        url = f'{URL_MASTERY}{name.replace(" ", "+").replace("#", "%23")}&region=EUW&lang=en_US'
        response = await session.get(url, headers=DEFAULT_HEADERS)
        html = HTMLParser(response.text)
        
        top_3_mastery = []
        for i in range(3):
            mastery_name_element = html.css_first(f'#tbody > tr:nth-child({i+1}) > td:nth-child(1) > a')
            mastery_amount_element = html.css_first(f'#tbody > tr:nth-child({i+1}) > td:nth-child(3)')
            if mastery_name_element and mastery_amount_element:
                mastery_name = mastery_name_element.text()
                mastery_amount = mastery_amount_element.text()
                top_3_mastery.append({'name': mastery_name, 'amount': mastery_amount})
            else:
                break  # Break the loop if the elements are not found
        
        return {'top_3_mastery': top_3_mastery}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'top_3_mastery': [{'name': 'n/a', 'amount': 'n/a'}]}

        
        

async def main(name: str) -> dict[str, dict]:
    try:
        session = AsyncSession(impersonate='edge101')
        champ_info_result = await champ_info(name, session)
        top_1_used_champ = champ_info_result.get('top_1_used_champ', '')

        wiki_info_task = asyncio.create_task(wiki_info(top_1_used_champ, session))
        ingsingfull_info_task = asyncio.create_task(ingsingfull_info(top_1_used_champ, session))
        mmr_task = asyncio.create_task(mmr(name, session))
        ladder_rank_task = asyncio.create_task(ladder_rank(name, session))
        mastery_task = asyncio.create_task(mastery(name, session))


        results = await asyncio.gather(wiki_info_task, ingsingfull_info_task, mmr_task, ladder_rank_task, mastery_task)

        wiki_info_result = results[0]
        ingsingfull_info_result = results[1]
        mmr_result = results[2]
        ladder_rank_result = results[3]
        mastery_result = results[4]
    
        await session.close()
        

        return {
            'champ_info': champ_info_result,
            'wiki_info': wiki_info_result,
            'ingsingfull_info': ingsingfull_info_result,
            'mmr': mmr_result,
            'ladder_rank': ladder_rank_result,
            'mastery': mastery_result,
    
        }
            
    except Exception as e:
        print(f'An error occurred in the main function: {e}')
        return {}


    

