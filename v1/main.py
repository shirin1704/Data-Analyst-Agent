# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "python-dotenv",
#     "playwright",
#     "beautifulsoup4",
# ]
# ///

from tools import scrape_website, get_relevant_data
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

import httpx
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

def get_relevant_data(file_name: str, js_selector: str=None) -> Dict[str, Any]:
    with open(file_name, encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    if js_selector:
        elements = soup.select(js_selector)
        return {"data":[el.get_text(strip=True) for el in elements]}

    return {"data": soup.get_text(strip=True)}

async def scrape_website(url: str, output_file: str = "scraped_content.html"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            content = await page.content()
            with open("scraped_content.html", "w", encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            print(f"Failed to load page: {e}")
            await browser.close()
            return
        await browser.close()

async def answer_questions(code: str) -> Dict[str, Any]:
    with open("temp_script.py", "w") as f:
        f.write(code)
    import subprocess
    result = subprocess.run(["python", "temp_script.py"], capture_output=True, text=True)
    return result.stdout

tools = [
    {
        "type": "function",
        "function": {
            "name": "scrape_website",
            "description": "Scrape a website and save its HTML content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the website to scrape."
                    },
                    "output_file": {
                        "type": "string",
                        "description": "The file where the scraped HTML content will be saved.",
                    }
                },
                "required": ["url", "output_file"],
                "additionalProperties": False
            },
            "strict" : True
    }
    },
    {
        "type": "function",
        "function": {
            "name": "get_relevant_data",
            "description": "Extract relevant data from wikitables in a webpage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The file containing the HTML content to analyze."
                    },
                    "js_selector":{
                        "type": "string",
                        "description": "The CSS selector to target target elements in the HTML content."
                    }
                },
                "required": ["file_name", "js_selector"],
                "additionalProperties": False
            },
            "strict" : True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "answer_questions",
            "description": "Answer questions based on the provided code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute for answering questions."
                    }
                },
                "required": ["code"],
                "additionalProperties": False
            },
            "strict" : True
        }
    }
]

def query_gpt(user_input: str, tools: list[Dict[str, Any]]) -> Dict[str, Any]:
    response = httpx.post(
        "https://aipipe.org/openai/v1/chat/completions",
        headers = {
            "Authorization": f"Bearer {os.getenv('AIPIPE_TOKEN')}",
            "Content-Type": "application/json"
        },
        json = {
            "model" : "gpt-4o-mini",
            "messages":[{"role": "user", "content": user_input}],
            "tools": tools,
            "tool_choice": "auto",
        },
    )
    with open('gpt_response.json', 'w', encoding = "utf-8") as f:
        f.write(response.text)
    return response.json()["choices"][0]["message"]

def main():
    user_input = input("Enter your query: ")
    response = query_gpt(user_input, tools)

    if "tool_calls" in response:
        for tool_call in response["tool_calls"]:
            if tool_call["type"] == "function":
                function_name = tool_call["function"]["name"]
                parameters = tool_call["function"]["arguments"]

                if function_name == "scrape_website":
                    scrape_website(**parameters)
                elif function_name == "get_relevant_data":
                    get_relevant_data(**parameters)
                elif function_name == "answer_questions":
                    answer_questions(**parameters)
    
    print("Response:", response.get("content", "No content returned."))

if __name__ == "__main__":
    main()
