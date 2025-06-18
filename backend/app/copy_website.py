from playwright.async_api import async_playwright, Playwright
from google import genai
from google.genai import types
from browserbase import Browserbase
from dotenv import load_dotenv
from PIL import Image
import asyncio
import requests
import io
import os
from bs4 import Comment, BeautifulSoup as soup
import regex as re
import json 
import time

 
load_dotenv()
gemini_api = os.getenv("gemini_api")
browser_base_api = os.getenv("browser_base_api")
bb_project = os.getenv("bb_project")

async def talk_to_llm(full_dom, image, layout, img_lst):
    client = genai.Client(api_key=gemini_api)
    image = Image.open('screenshot.png')
    if len(img_lst) == 0:
        img_lst = "There are no Images"
    max_tries = 3
    tries = 0
    delay = 5
    prompt = True
    while (tries < max_tries) and prompt:
        try:
            first_iteration = client.models.generate_content(
                model="gemini-2.0-flash", config=types.GenerateContentConfig(
                system_instruction=   
                        "You are a web designer. I have provided you the full layout of the website, along with an image on how it should look, with " \
                        "the full dom as well. Your task is the create a clone of the website. Be sure to:" \
                        "-use the exact same layout" \
                        "use the same texts" \
                        "Use the same coloring scheme" \
                        "resize images so they fit as they did on the original" \
                        "keep the same styling, padding, ect" \
                        "At the end, the website you create should look like an exact clone of the image you are provided" \
                        "DO NOT PROVIDE ANY COMMENTARY, RESPONSE SHOULD JUST BE EXCLUSIVLY HTML CODE"),
                contents=[layout, image, full_dom]
            )
            prompt = False
        except Exception as e:
            print(e)
            time.sleep(delay)
            tries+=1
    tries = 0
    prompt = True

    print('part one done')
    while (tries < max_tries) and prompt:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", config=types.GenerateContentConfig(
                system_instruction=   "You are a web designer. This is your second iteration of creating a website" \
                "I have given you your first iteration. " \
                "You are given your attempt, an image of the website you are trying to copy" \
                "that websites, full_dom and layout, along with a list of links to the images used." \
                "Determine how big an image should be based only on the image of the website given" \
                "The Layout should be the exact same as the layout you are given" \
                "At the end, the website you create should look like an exact clone of the image you are provided" \
                "INCLUDE EVERY PART OF THE WEBSITE AND GET EVERY PICTURE"\
                "DO NOT PROVIDE ANY COMMENTARY, RESPONSE SHOULD JUST BE EXCLUSIVLY HTML CODE"),
                contents=[first_iteration, image, full_dom, layout, img_lst]
            )
            prompt = False
            return response.text
        except Exception as e:
            print(e)
            time.sleep(delay)
            tries+=1
    


async def generate_website_copy(URL):
    bb = Browserbase(api_key=browser_base_api)
    session = bb.sessions.create(project_id=bb_project)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(session.connect_url)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url=str(URL))
        await page.wait_for_load_state()
        img_lst = []
        all_link = await page.query_selector_all('img')
        for link in all_link:
            link_url = await link.get_attribute('src')
            if link_url is None:
                continue
            if URL in link_url:
                img_lst.append(link_url)
            else:
                img_lst.append(URL + link_url)
        
        full_dom = await page.content()

        layout_tree = await page.evaluate("""() => {
            const walk = (el) => ({
                tag: el.tagName,
                class: el.className,
                id: el.id,
                children: Array.from(el.children).map(walk)
            });
            return walk(document.body);
        }""")
        layout_str = json.dumps(layout_tree, indent=2)


        s  = soup(full_dom, "html.parser")
        for tag in s(["script", "style", "noscript", "meta", "link"]):
            tag.decompose()



        for comment in s.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()


        cleaned_html = re.sub(r'>\s+<', '><', str(s)) 
        cleaned_html = re.sub(r'\s{2,}', ' ', cleaned_html)
        

        screenshot = await page.screenshot(path="screenshot.png", full_page=True)
        html_str = await talk_to_llm(cleaned_html, screenshot, layout_str, img_lst)
        await browser.close()
        return "\n".join(html_str.splitlines()[1:-1])


