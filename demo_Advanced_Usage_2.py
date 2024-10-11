# demo_Advanced_Usage_2.py
# Using a proxy server
    
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True, proxy="http://127.0.0.1:7890") as crawler:
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
            bypass_cache=True
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())