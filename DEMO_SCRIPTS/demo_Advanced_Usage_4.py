# demo_Advanced_Usage_4.py
# Extracting Structured Data with OpenAI


import os
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(..., description="Fee for output token for the OpenAI model.")

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url='https://openai.com/api/pricing/',
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4o", api_token=os.getenv('OPENAI_API_KEY'),
                schema=OpenAIModelFee.schema(),
                extraction_type="schema",
                instruction="""From the crawled content, extract all mentioned model names along with their fees for input and output tokens.
                Do not miss any models in the entire content. One extracted model JSON format should look like this:
                {"model_name": "GPT-4", "input_fee": "US$10.00 / 1M tokens", "output_fee": "US$30.00 / 1M tokens"}."""
            ),
            bypass_cache=True,
        )
        print(result.extracted_content)

if __name__ == "__main__":
    asyncio.run(main())