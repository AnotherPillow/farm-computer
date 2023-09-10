import bs4, requests, discord, re, time

from src.embed import EmbedBuilder
from src.config import (
    HELP_PREFIX
)
from src.emotes import getQualityFromPath, identify


logger = None

def help() -> EmbedBuilder:
    embed = EmbedBuilder(
        fields=[],
        color=discord.Color.orange()
    )

    embed.title = 'Search Stardew Valley Wiki'
    embed.description = 'Search the Stardew Valley Wiki for a specific page'
    
    embed.fields.append({
        'name': 'Usage',
        'value': f'`{HELP_PREFIX}wiki <search term>`',
        'inline': False
    })

    return embed

def cleanSellPrice(price: str) -> str:
    regex = r'data-sort-value="[a-zA-Z0-9-_ ]+"'
    return re.sub(regex, '', price)


def parse(url=None, build=True) -> EmbedBuilder or discord.Embed:
    embed = EmbedBuilder(
        fields=[],
        color=discord.Color.orange()
    )

    logger.info(f'Parsing url: {url}')

    if 'https://stardewvalleywiki.com/Special:Search' in url \
        or 'https://stardewvalleywiki.com/mediawiki/index.php?search=' in url \
            or not url:

        return help().build() if build else help()

        


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
    
    try:
        pagename = soup.find({'id': 'firstHeading'}).text
        embed.title =  pagename + ' - Stardew Valley Wiki'
    except:
        pagename = soup.find('title').text
        embed.title = pagename
    embed.url = url

    

    # find all id=infoboxtable > tr that have a infoboxsection and infoboxdetail

    infobox = soup.find_all('table', {'id': 'infoboxtable'})

    # logger.info(f'Found infoboxtable: {infobox}')

    if infobox:
        infobox = infobox[0]

        trs = infobox.find_all('tr')

        for tr in trs:
            # logger.info(f'Found tr: {tr}')
            # try:
            if tr.find_all('table', {'style': 'width:101%;'}): # or tr.find_all('div', {'class': 'parent'}):
                break
            section = tr.find_all('td', {'id': 'infoboxsection'})
            detail = tr.find_all('td', {'id': 'infoboxdetail'})

            if section:
                section = section[0].text
                # logger.info(f'Found section: {section}')
            
            if detail:
                detail = detail[0]
            
            if not section or not detail:
                continue
            
            if (table := detail.find_all('table')) and section.strip() != 'Sell Price':
                table = table[0]
                rows = table.find_all('tr')

                first_row = rows[0]

                text = ''
                for row in rows:
                    do_newline = True
                    if row.find_all('tr'):
                        continue
                    for i, td in enumerate(row.find_all('td')):
                        # logger.info(f'Found td: {td}')

                        if backimages := td.find_all('div', {'class': 'backimage'}):

                            # logger.info(f'Found backimage: {backimages}')
                            emoji = identify(backimages[0].find_all('img')[0]['src'], 
                                pagename,
                                foreimages=td.find_all('div', {'class': 'foreimage'})
                            )
                            
                            # logger.info(f'Emoji: {emoji}')
                            text += f'{emoji} '
                        inner = td.text.strip()
                        if not inner:
                            continue
                        elif td.has_attr('style') and 'vertical-align: bottom;' in td['style']:
                            # logger.info(f'Found td with style: {td["style"]}')
                            text += f'{inner} '
                        elif not td.children or not td.attrs:
                            # logger.info(f'Found td with no children/attrs')
                            do_newline = False
                            text += f'{inner} '
                        # logger.info(f'Found inner: *{inner}*')

                        # check if the next td has no attrs and no children
                        if i + 1 < len(row.find_all('td')):
                            next_td = row.find_all('td')[i + 1]
                            if not next_td.attrs and not next_td.children:
                                do_newline = False
                        elif row.parent != first_row.parent:
                            do_newline = False




                    # logger.info(f'Found row: {row}')
                    
                    if do_newline:
                        text += '\n'    
                            

                detail = text

            elif spans := detail.find_all('span', {'class': 'no-wrap'}):
                detail = spans[0].text
            elif spans := detail.find_all('span', { 'style': 'display: none;'}):
                # logger.info(f'Found span: {spans}')
                detail = detail.text.replace(spans[0].text, '')

            elif spans := detail.find_all('span', {'class': 'nametemplate'}):
                items = []
                for span in spans:
                    items.append(span.text)
                detail = ', '.join(items)
            
            elif p_tags := detail.find_all('p', {
                'class': lambda x: x != 'mw-empty-elt'
            }):
                items = []
                for p in p_tags:
                    items.append(p.text)

                detail = ', '.join(items)
            elif imgs := [
                x for x in detail.find_all('img')
                if x['alt'].endswith(' Quality.png')
            ]:
                # getinnerhtml of the detail

                # replace all LOOSE TEXT in the detail with a <loose> tag
                for child in detail.children:
                    if isinstance(child, bs4.element.NavigableString):
                        # child.replace_with(f'<loose>{child}</loose>') will escape the <> 
                        # so we have to do this instead
                        child.wrap(soup.new_tag('span'))

                
                # logger.info(f'Found child: {str(detail.children)}')
                # extract the img/span pairs
                # the html is like this:
                # text, img | text, img | text, img | text
                pairs = []
                skip = False
                for i, child in enumerate(detail.children):
                    if skip:
                        skip = False
                        continue
                    if isinstance(child, bs4.element.Tag):
                        # check if its an img, if it is, get the next child, otherwise set the img inthe aay to none
                        if child.name == 'img':
                            img = child.attrs['src']
                            text = detail.contents[i+1].text
                            
                            # for some reason it has weird escaped unicode
                            text = ''.join([i if ord(i) < 128 else ' ' for i in text]).strip()

                            pairs.append((text, img))
                            skip = True
                        else:
                            pairs.append((child.text, None))

                

                # logger.info(f'Found pairs: {str(pairs)}')

                detail = ''
                for pair in pairs:
                    if pair[1]:
                        detail += f'{getQualityFromPath(pair[1])} {pair[0]} '
                    else:
                        detail += f'{pair[0]}'
                

                
            else:
                detail = detail.text
                

            embed.fields.append({
                'name': section,
                'value': detail,
                'inline': False
            })
            # except Exception as e:
            #     logger.error(f'Error failed to parse tr: {e} on line {e.__traceback__.tb_lineno}')
            #     # throw the error
            #     # raise e
            #     pass
    else:
        body = soup.find_all('div', {'class': 'mw-parser-output'})[0]
        #  get the first two <p> tags
        for p in body.find_all('p')[:2]:
            embed.description += cleanSellPrice(p.text) + '\n\n'
    # logger.info(f'Got embed: {embed}')
    # return embed.build()
    return embed.build() if build else embed

def search(query, _logger=None, cache=None):
    global logger
    logger = _logger

    startTime = time.time()

    if isinstance(query, list) or isinstance(query, tuple):
        query = ' '.join(query)
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
        #return parse(redir)
        return cache.get(redir)

    for li in soup.find_all('li', {'class': 'mw-search-result'}):
        href = li.find_all('a')[0]['href']
        full_href = f'https://stardewvalleywiki.com{href}'

        r = requests.get(full_href)
        status = r.status_code

        if status == 200:
            #return parse(full_href)
            return cache.get(full_href)
        elif status in [301, 302, 304]:
            redirected_link = r.url
            #return parse(redirected_link)
            return cache.get(redirected_link)

    # return parse(res.url)
    if soup.find('p', {'class': 'mw-search-createlink'}):
        return help().build()
        
    resp = cache.get(res.url)
    logger.info(f'Got response for {query} in {time.time() - startTime} seconds')
    return resp


