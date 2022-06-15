from multiprocessing.sharedctypes import Value
from operator import index
from pydoc import html
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import Creds, urls_internal
import pandas as pd

page_max = 155
counter = 1
devices = []

# Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=50)
    page = browser.new_page()
    page.goto(urls_internal.base_url)
    page.is_visible('button[type=submit]')

    # Login Fill
    page.fill('input#j_username', Creds.user_name_chilgren)
    page.fill('input#j_password', Creds.pass_chilgren)
    page.click('button[type=submit]')
    page.is_visible('h3')

    # Goes through each of devices page
    for page_current in range(page_max):
        url = urls_internal.device_url + page_current
        page.goto(url)
        print('Going to page ', page_current)
        page.is_visible('table#devices_table')
        page.is_visible('tbody')
        page.is_visible('table#devices_table')
        page.is_visible('tr')

        # Playwright locator function to grab rows
        rows = page.locator("table tr")

        count = rows.count()
        for i in range(count):
            device_properties = rows.nth(i).all_inner_texts()
            temp = []
            repl_delm_t = ','
            repl_delm_n = ''
            temp = temp = device_properties[0].replace('\n', repl_delm_n)
            temp = temp.replace('\t', repl_delm_t)
            devices.append(temp)
            counter += 1

        page_current -= 1

    #Final Processing
    devices_df = pd.DataFrame([sub.split(",") for sub in devices])
    devices_df.to_csv(document_path, index=False)
    print('done')
