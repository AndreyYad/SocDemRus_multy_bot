from aiohttp import ClientSession
from bs4 import BeautifulSoup
from re import findall, search, sub

from main_modules.config import URLS

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
}

async def get_last_post():
    async with ClientSession() as session:
        async with session.get(URLS['sdr_vk'], headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            
            # with open('test.txt', 'w', encoding='utf-8') as file:
                # file.write(str(soup))
            
            post = soup.find('div', {'class':'post_content'}) 
            text_post = post.find('div', {'class':'wall_post_text'}).contents
            
            if text_post[-1].name == 'span':
                text_post = text_post[:-1] + text_post[-1].contents
            
            for i in range(len(text_post)):
                if type(text_post[i]) == str:
                    continue
                else:
                    match text_post[i].name:
                        case 'br':
                            text_post[i] = '\n'
                        case 'img':
                            text_post[i] = text_post[i].attrs['alt']
                        case 'button':
                            text_post[i] = ''
                    
            text_post = ''.join(text_post)
            print(text_post)
            
            return text_post