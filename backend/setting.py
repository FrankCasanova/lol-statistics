DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

MMR_HEADERS = {
    
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "accept-encoding": "gzip, deflate,",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "referer": "https://mylolmmr.com/",
    "sec-ch-ua": "'Chromium';v='99', 'Google Chrome';v='99', ';Not A Brand';v='99'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
}

TRESHOLDS = [125, 250, 375, 500, 625, 750, 875, 1000, 1125, 1250, 1375, 1500, 1625, 1750, 1875, 2000, 2125, 2250, 2375, 2500, 2625, 2750, 2875, 3000, 3125, 3250, 3375, 3500, 4000, 5000]
RANKS = ['iron-iv', 'iron-iii', 'iron-ii', 'iron-i', 'bronze-iv', 'bronze-iii', 'bronze-ii', 'bronze-i', 'silver-iv', 'silver-iii', 'silver-ii', 'silver-i', 'gold-iv', 'gold-iii', 'gold-ii', 'gold-i', 'platinum-iv', 'platinum-iii', 'platinum-ii', 'platinum-i', 'emerald-iv', 'emerald-iii', 'emerald-ii', 'emerald-i', 'diamond-iv', 'diamond-iii', 'diamond-ii', 'diamond-i', 'master', 'grandmaster', 'challenger']


URL_MMR = 'https://api.mylolmmr.com/api/mmr/euw1/'
URL_CHAMP_INFO = 'https://tracker.gg/lol/profile/riot/EUW/'
URL_WIKI = 'https://leagueoflegends.fandom.com/wiki/'
URL_INGSINGFULL_INFO = 'https://lolalytics.com/lol/'
URL_LADDER_RANK = 'https://www.op.gg/summoners/euw/'
URL_MASTERY = 'https://championmastery.gg/player?riotId='
