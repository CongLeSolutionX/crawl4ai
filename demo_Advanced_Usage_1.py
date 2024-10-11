# demo_Advanced_Usage_1.py
# Executing JavaScript and Using CSS Selectors

import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        js_code = ["const loadMoreButton = Array.from(document.querySelectorAll('button')).find(button => button.textContent.includes('Load More')); loadMoreButton && loadMoreButton.click();"]
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
            js_code=js_code,
            css_selector="article.tease-card",
            bypass_cache=True
        )
        print(result.extracted_content)

if __name__ == "__main__":
    asyncio.run(main())