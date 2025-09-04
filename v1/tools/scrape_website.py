# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "playwright",
# ]
# ///

from playwright.async_api import async_playwright
import asyncio

async def scrape_website(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until = 'domcontentloaded', timeout = 60000)
            content = await page.content()
            with open("scraped_content.html", "w", encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            print(f"Failed to load page: {e}")
            await browser.close()
            return
        await browser.close()

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"  
    asyncio.run(scrape_website(url))
    print("Website scraped successfully.")