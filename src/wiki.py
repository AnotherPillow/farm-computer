import bs4, requests, discord

from src.embed import EmbedBuiler
from src.config import (
    BOT_PREFIX
)

logger = None

def parse(url=None):
    embed = EmbedBuiler(
        fields=[],
        color=discord.Color.orange()
    )

    logger.info(f'Parsing url: {url}')

    if url == 'https://stardewvalleywiki.com/Special:Search' or not url:
        embed.title = 'Search Stardew Valley Wiki'
        embed.description = 'Search the Stardew Valley Wiki for a specific page'
        embed.fields.append({
            'name': 'Usage',
            'value': f'`{BOT_PREFIX}wiki <search term>`',
            'inline': False
        })
        return embed.build()


    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # find the first <img> that does NOT have a srcset attr

    main_logo_url = f'https://stardewvalleywiki.com/mediawiki/images/6/68/Main_Logo.png'

    try:
        
        embed.thumbnail = 'https://stardewvalleywiki.com' + soup.find_all('img', {'srcset': False})[0]['src']
        if embed.thumbnail == 'https://stardewvalleywiki.com/mediawiki/resources/assets/licenses/cc-by-nc-sa.png':
            embed.image = main_logo_url
            embed.thumbnail = None
        
    except:
        embed.image = main_logo_url
    
    embed.title = soup.find_all('h1', {'id': 'firstHeading'})[0].text + ' - Stardew Valley Wiki'
    embed.url = url

    

    # find all id=infoboxtable > tr that have a infoboxsection and infoboxdetail

    infobox = soup.find_all('table', {'id': 'infoboxtable'})

    # logger.info(f'Found infoboxtable: {infobox}')

    if infobox:
        infobox = infobox[0]

        trs = infobox.find_all('tr')

        for tr in trs:
            # logger.info(f'Found tr: {tr}')
            try:
                section = tr.find_all('td', {'id': 'infoboxsection'})[0].text
                detail = tr.find_all('td', {'id': 'infoboxdetail'})[0]

                if spans := detail.find_all('span', {'class': 'no-wrap'}):
                    detail = spans[0].text
                elif spans := detail.find_all('span', {'style': 'display: none;'}):
                    # logger.info(f'Found span: {spans}')
                    detail = detail.text.replace(spans[0].text, '')

                elif spans := detail.find_all('span', {'class': 'nametemplate'}):
                    items = []
                    for span in spans:
                        items.append(span.text)
                    detail = ', '.join(items)
                
                elif p_tags := detail.find_all('p'):
                    items = []
                    for p in p_tags:
                        items.append(p.text)

                    detail = ', '.join(items)
                
                else:
                    detail = detail.text
                    

                embed.fields.append({
                    'name': section,
                    'value': detail,
                    'inline': False
                })
            except Exception as e:
                # logger.error(f'Error failed to parse tr: {e}')
                pass
    else:
        body = soup.find_all('div', {'class': 'mw-parser-output'})[0]
        #  get the first two <p> tags
        for p in body.find_all('p')[:2]:
            embed.description += p.text + '\n\n'
    return embed.build()

def search(query, _logger=None):
    global logger
    logger = _logger

    query = " ".join(query)
    encoded = query.replace(" ", "+")

    url = f'https://stardewvalleywiki.com/mediawiki/index.php?search={encoded}'
    
    res = requests.get(url)

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # logger.info(f'Got status code: {res.status_code}')
    # logger.info(f'Got url: {res.url}')

    redir = False
    if res.status_code in [301, 302, 304]:
        try:
            redir = soup.find_all('meta', {'property': 'og:url'})[0]['content']
        except:
            pass

    if redir:
        return parse(redir)

    for li in soup.find_all('li', {'class': 'mw-search-result'}):
        href = li.find_all('a')[0]['href']
        full_href = f'https://stardewvalleywiki.com{href}'

        r = requests.get(full_href)
        status = r.status_code

        if status == 200:
            return parse(full_href)
        elif status in [301, 302, 304]:
            redirected_link = r.url
            return parse(redirected_link)

    return parse(res.url)


