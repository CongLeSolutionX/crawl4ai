# demo_Advanced_Usage_3_Extract_Medium_content.py
# Extracting Structured Data without LLM

import asyncio
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


async def extract_news_teasers():
    schema = {
        "name": "Medium Article Extractor",
        "baseSelector": "article.meteredContent",
        "fields": [
            {
                "name": "title",
                "selector": "[data-testid='storyTitle']",
                "type": "text"
            },
            {
                "name": "subtitle",
                "selector": ".pw-subtitle-paragraph",
                "type": "text"
            },
            {
                "name": "metaDescription",
                "selector": "meta[name='description']",
                "type": "attribute",
                "attribute": "content"
            },
            {
                "name": "author",
                "selector": "[data-testid='authorName']",
                "type": "text"
            },
            {
                "name": "readingTime",
                "selector": "[data-testid='storyReadTime']",
                "type": "text"
            },
            {
                "name": "publishDate",
                "selector": "[data-testid='storyPublishDate']",
                "type": "text"
            },
            {
                "name": "authorImage",
                "type": "nested",
                "selector": "[data-testid='authorPhoto']",
                "fields": [
                    {
                        "name": "src",
                        "type": "attribute",
                        "attribute": "src"
                    },
                    {
                        "name": "alt",
                        "type": "attribute",
                        "attribute": "alt"
                    }
                ]
            },
            {
                "name": "content",
                "selector": "article.meteredContent",
                "type": "html"
            },
            {
                "name": "tags",
                "selector": ".qc.ee.cx.qd.ff.qe.qf.bf.b.bg.z.bk.qg",
                "type": "text",
                "multiple": True
            },
            {
                "name": "canonicalUrl",
                "selector": "link[rel='canonical']",
                "type": "attribute",
                "attribute": "href"
            },
            {
                "name": "headings",
                "selector": "h1, h2, h3, h4, h5, h6",
                "type": "nested",
                "multiple": True,
                "fields": [
                    {
                        "name": "level",
                        "type": "property",
                        "property": "tagName"
                    },
                    {
                        "name": "text",
                        "type": "text"
                    }
                ]
            }
        ]
    }

    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://medium.com/@CongLeSolutionX/state-management-in-swiftui-overview-part-1-4c7cb7d3b931",
            extraction_strategy=extraction_strategy,
            bypass_cache=True,
        )

        assert result.success, "Failed to crawl the page"

        news_teasers = json.loads(result.extracted_content)
        print(f"Successfully extracted {len(news_teasers)} news teasers")
        print(json.dumps(news_teasers[0], indent=2))


if __name__ == "__main__":
    asyncio.run(extract_news_teasers())
