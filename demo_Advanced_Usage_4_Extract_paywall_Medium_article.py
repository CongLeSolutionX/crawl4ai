# demo_Advanced_Usage_4_Extract_paywall_Medium_article.py
# Extracting Structured Data with OpenAI

import os
import asyncio
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field


class MediumArticle(BaseModel):  # Define your Pydantic model
    title: str = Field(...)
    subtitle: str = Field(...)
    metaDescription: str = Field(...)
    author: str = Field(...)
    readingTime: str = Field(...)
    publishDate: str = Field(...)
    authorImage: dict = Field(...)  # Use dict for nested authorImage field
    content: str = Field(...)
    tags: list = Field(...)        # Use list for tags
    canonicalUrl: str = Field(...)
    headings: list = Field(...)


async def extract_medium_article():

    extraction_strategy = LLMExtractionStrategy(
        provider="openai/gpt-4o",  # or "openai/gpt-3.5-turbo-0301" if you prefer
        api_token=os.getenv('OPENAI_API_KEY'),
        schema=MediumArticle.schema(),          # Updated class name
        extraction_type="schema",

        instruction="""Extract the following information from the crawled web page, \
        formatted as a JSON object adhering to the provided schema.  If an element is \
        not found or doesn't exist, provide an empty string ("") for text fields, an empty \
        dictionary (`{}`) for nested objects, and an empty list (`[]`) for list/array fields:

        * title: The title of the article.
        * subtitle: The subtitle of the article.
        * metaDescription: The content of the meta description tag.
        * author: The author of the article.
        * readingTime: The estimated reading time.
        * publishDate: The publication date of the article.
        * authorImage: A dictionary containing the 'src' and 'alt' attributes of the author's image.
        * content: The main content of the article (HTML).
        * tags: A list of tags associated with the article.
        * canonicalUrl: The canonical URL of the article.
        * headings: A list of all headings (h1-h6) with their level (e.g., 'H1', 'H2') and text content.
        """
    )


    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://medium.com/@claudia.nikel/how-to-setup-a-jupyter-notebook-in-vs-code-w-virtual-env-kernels-install-packages-884cf643375e",
            extraction_strategy=extraction_strategy,
            bypass_cache=True,
        )

        assert result.success, f"Failed to crawl or extract: {result.error}" # Better error

        try:
            article_data = json.loads(result.extracted_content)
            print(json.dumps(article_data, indent=2))

        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            print(f"Raw extracted content: {result.extracted_content}")  # Print raw content for debugging


if __name__ == "__main__":
    asyncio.run(extract_medium_article())
