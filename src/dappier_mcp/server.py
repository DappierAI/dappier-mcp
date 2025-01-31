from typing import Annotated, Any, Dict, Literal, Optional
from mcp.server import Server
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from pydantic import BaseModel, Field
from dappier import Dappier

DEFAULT_AI_MODEL_ID = "am_01j06ytn18ejftedz6dyhz2b15"
DEFAULT_DATA_MODEL_ID = "dm_01j0pb465keqmatq9k83dthx34"

class RealTimeDataSearch(BaseModel):
    """Parameters for Dappier Real-Time Data search."""

    query: Annotated[
        str,
        Field(description="The user-provided input string for retrieving real-time data, including web search results, financial information, news, weather, and more, with AI-powered insights and updates.")
    ]

    ai_model_id: Annotated[
        Literal[
            "am_01j06ytn18ejftedz6dyhz2b15", # Real Time Data
            "am_01j749h8pbf7ns8r1bq9s2evrh" # Stock Market Data
        ],
        Field
        (
            default=DEFAULT_AI_MODEL_ID,
            description=(
            "The AI model ID to use for the query. The AI model ID always starts with the prefix 'am_'.\n\n"
            "Available AI Models:\n"
            "- am_01j06ytn18ejftedz6dyhz2b15: (Real Time Data) Access real-time Google web search results, "
            "including the latest news, weather, stock prices, travel, deals, and more.\n"
            "- am_01j749h8pbf7ns8r1bq9s2evrh: (Stock Market Data) Access real-time financial news, stock prices, "
            "and trades from Polygon.io, with AI-powered insights and up-to-the-minute updates to keep you informed "
            "on all your financial interests.\n\n"
            "Defaults to 'am_01j06ytn18ejftedz6dyhz2b15'.\n\n"
            "Multiple AI models are available, which can be found at: https://marketplace.dappier.com/marketplace"
            ),
        )
    ]


class AIRecommendations(BaseModel):
    """Parameters for Dappier AI-powered recommendations."""

    query: Annotated[
        str,
        Field(
            description="The user-provided input string for AI recommendations across Sports, Lifestyle News, and niche favorites like I Heart Dogs, I Heart Cats, Green Monster, WishTV, and many more."
        )
    ]

    data_model_id: Annotated[
        Literal[
            "dm_01j0pb465keqmatq9k83dthx34",  # Sports News
            "dm_01j0q82s4bfjmsqkhs3ywm3x6y",  # Lifestyle News
            "dm_01j1sz8t3qe6v9g8ad102kvmqn",  # iHeartDogs AI
            "dm_01j1sza0h7ekhaecys2p3y0vmj",  # iHeartCats AI
            "dm_01j5xy9w5sf49bm6b1prm80m27",  # GreenMonster
            "dm_01jagy9nqaeer9hxx8z1sk1jx6",  # WISH-TV AI
        ],
        Field(
            default=DEFAULT_DATA_MODEL_ID,
            description=(
                "The data model ID to use for recommendations. Data model IDs always start with the prefix 'dm_'.\n\n"
                "Available Data Models:\n"
                "- dm_01j0pb465keqmatq9k83dthx34: (Sports News) Real-time news, updates, and personalized content "
                "from top sports sources like Sportsnaut, Forever Blueshirts, Minnesota Sports Fan, LAFB Network, "
                "Bounding Into Sports, and Ringside Intel.\n"
                "- dm_01j0q82s4bfjmsqkhs3ywm3x6y: (Lifestyle News) Real-time updates, analysis, and personalized "
                "content from top sources like The Mix, Snipdaily, Nerdable, and Familyproof.\n"
                "- dm_01j1sz8t3qe6v9g8ad102kvmqn: (iHeartDogs AI) A dog care expert with access to thousands of "
                "articles on health, behavior, lifestyle, grooming, ownership, and more from the industry-leading pet "
                "community iHeartDogs.com.\n"
                "- dm_01j1sza0h7ekhaecys2p3y0vmj: (iHeartCats AI) A cat care expert with access to thousands of "
                "articles on health, behavior, lifestyle, grooming, ownership, and more from the industry-leading pet "
                "community iHeartCats.com.\n"
                "- dm_01j5xy9w5sf49bm6b1prm80m27: (GreenMonster) A helpful guide to making conscious and compassionate "
                "choices that benefit people, animals, and the planet.\n"
                "- dm_01jagy9nqaeer9hxx8z1sk1jx6: (WISH-TV AI) Covers sports, politics, breaking news, multicultural "
                "news, Hispanic language content, entertainment, health, and education.\n\n"
                "Defaults to 'dm_01j0pb465keqmatq9k83dthx34'.\n\n"
                "Multiple data models are available, which can be found at: https://marketplace.dappier.com/marketplace"
            ),
        )
    ]


    similarity_top_k: Annotated[
        int,
        Field(
            default=9,
            description="The number of top documents to retrieve based on similarity. Defaults to 9.",
        )
    ]

    ref: Annotated[
        Optional[str],
        Field(
            default=None,
            description="The site domain where AI recommendations should be displayed. Defaults to None.",
        )
    ]

    num_articles_ref: Annotated[
        int,
        Field(
            default=0,
            description="The minimum number of articles to return from the specified reference domain (`ref`). The remaining articles will come from other sites in the RAG model. Defaults to 0.",
        )
    ]

    search_algorithm: Annotated[
        Literal["most_recent", "semantic", "most_recent_semantic", "trending"],
        Field(
            default="most_recent",
            description="The search algorithm to use for retrieving articles. Defaults to 'most_recent'.",
        )
    ]

async def serve(api_key: str) -> None:
    """Run the Dappier MCP server.

    Args:
        api_key: Dappier API key
    """
    server = Server("dappier-mcp")
    client = Dappier(api_key=api_key)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="dappier_real_time_search",
                description="""Retrieves direct answers to real-time queries using AI-powered search. 
                This includes web search results, financial information, news, weather, stock market 
                updates, and more.

                - AI-Powered Direct Answer: The response is a concise and relevant answer 
                generated by an AI model.
                - Ideal for quick lookups: Get real-time insights on trending topics, 
                stock prices, breaking news, and live weather updates.

                Example Queries:
                - "How is the weather today in Austin, TX?"
                - "What is the latest news for Meta?"
                - "What is the stock price for AAPL?"
                """,
                inputSchema=RealTimeDataSearch.model_json_schema(),
            ),
            Tool(
                name="dappier_ai_recommendations",
                description="""Provides AI-powered content recommendations based on structured 
                data models. Returns a list of articles with titles, summaries, images, and 
                source URLs for in-depth exploration.

                - Structured JSON Response: Unlike real-time AI models, this tool returns 
                rich metadata instead of a direct answer.
                - Personalized Content Discovery: Ideal for exploring news, lifestyle topics, 
                niche interests, and domain-specific recommendations.
                - Flexible Customization:
                - Data Model Selection: Choose a predefined data model to tailor recommendations 
                    (e.g., Sports, Lifestyle, Pets, or News). Available models can be found at: 
                    [Dappier Marketplace](https://marketplace.dappier.com/marketplace).
                - Similarity Filtering: Retrieve top articles based on semantic relevance (default: 9).
                - Reference Domain Filtering: Prioritize content from a specific website (`ref`).
                - Search Algorithms: Select from 'most_recent', 'semantic', 'most_recent_semantic', 
                    or 'trending' for refined recommendations.

                Example Queries:
                - "Show me the latest sports news."
                - "Find trending articles on sustainable living."
                - "Get pet care recommendations from IHeartDogs AI."
                
                The tool returns a list of recommended articles in the following structure:
                ```
                Title: <Article title>
                Author: <Article author>
                Published on: <Publication date>
                Source: <Site name> (<Site domain>)
                URL: <Full article link>
                Image URL: <Thumbnail link>
                Summary: <Brief article overview>
                Score: <Relevance score>
                ```
                """,
                inputSchema=AIRecommendations.model_json_schema(),
            )
        ]


    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="dappier_real_time_search",
                description="""Retrieves direct answers to real-time queries using AI-powered search. 
                This includes web search results, financial information, news, weather, stock market 
                updates, and more. The response is a concise AI-generated answer rather than structured 
                data.

                Example Queries:
                - "How is the weather today in Austin, TX?"
                - "What is the latest news for Meta?"
                - "What is the stock price for AAPL?"
                """,
                arguments=[
                    PromptArgument(
                        name="query",
                        description="The search query to retrieve real-time information.",
                        required=True,
                    ),
                ],
            ),
            Prompt(
                name="dappier_ai_recommendations",
                description="""Provides AI-powered recommendations based on structured data models. 
                Returns a list of articles containing titles, summaries, images, and source URLs 
                for in-depth exploration.

                Key Features:
                - Structured JSON Response: Unlike real-time AI search, this returns rich metadata 
                instead of a direct answer.
                - Personalized Content Discovery: Retrieve articles on Sports, Lifestyle, Niche News, 
                and specific topics like I Heart Dogs, I Heart Cats, and WishTV.
                - Flexible Customization:
                - Data Model Selection: Choose a predefined data model for specific recommendations 
                    (e.g., 'dm_01j0pb465keqmatq9k83dthx34' for sports). Available models:  
                    [Dappier Marketplace](https://marketplace.dappier.com/marketplace).
                - Similarity Filtering: Retrieve top articles based on semantic relevance.
                - Reference Domain Filtering: Prioritize content from a specific website (`ref`).
                - Search Algorithms: Choose from 'most_recent', 'semantic', 'most_recent_semantic', 
                    or 'trending'.

                Example Queries:
                - "Show me the latest sports news."
                - "Find trending articles on sustainable living."
                - "Get pet care recommendations from IHeartDogs AI."
                """,
                arguments=[
                    PromptArgument(
                        name="query",
                        description="The user-provided input string for AI recommendations.",
                        required=True,
                    ),
                    PromptArgument(
                        name="data_model_id",
                        description="The data model ID for recommendations. Data model IDs always start with 'dm_'. Defaults to 'dm_01j0pb465keqmatq9k83dthx34'. Explore available models at: https://marketplace.dappier.com/marketplace.",
                        required=False,
                    ),
                    PromptArgument(
                        name="similarity_top_k",
                        description="The number of top articles to retrieve based on similarity. Defaults to 9.",
                        required=False,
                    ),
                    PromptArgument(
                        name="ref",
                        description="The site domain where AI recommendations should be prioritized. Defaults to None.",
                        required=False,
                    ),
                    PromptArgument(
                        name="num_articles_ref",
                        description="The minimum number of articles to return from the specified reference domain (`ref`). The remaining articles will come from other sites within the AI model. Defaults to 0.",
                        required=False,
                    ),
                    PromptArgument(
                        name="search_algorithm",
                        description="The search algorithm to use for retrieving articles. Options: 'most_recent', 'semantic', 'most_recent_semantic', or 'trending'. Defaults to 'most_recent'.",
                        required=False,
                    ),
                ],
            ),
        ]

    def format_results(response: Dict[str, Any]) -> str:
        """
        Converts a Dappier's AI Recommendations API response into a human-readable text format for LLMs.
        
        :param response: JSON object returned by the Dappier API
        :return: Formatted string representation
        """
        message = response.get("message")
        
        if isinstance(message, str) and message:
            return message

        if response.get("status") != "success":
            return "The API response was not successful."
        
        query = response["response"].get("query", "No query provided")
        results = response["response"].get("results", [])
        
        formatted_text = f"Search Query: {query}\n\n"
        
        for idx, result in enumerate(results, start=1):
            formatted_text += (f"Result {idx}:\n"
                            f"Title: {result.get('title', 'No title')}\n"
                            f"Author: {result.get('author', 'Unknown author')}\n"
                            f"Published on: {result.get('pubdate', 'No date available')}\n"
                            f"Source: {result.get('site', 'Unknown site')} ({result.get('site_domain', 'No domain')})\n"
                            f"URL: {result.get('source_url', 'No URL available')}\n"
                            f"Image URL: {result.get('image_url', 'No URL available')}\n"
                            f"Summary: {result.get('summary', 'No summary available')}\n"
                            f"Score: {result.get('score', 'No score available')}\n"
                            f"\n")
        
        return formatted_text

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            if name == "dappier_real_time_search":
                args = RealTimeDataSearch(**arguments)
                response = client.search_real_time_data(
                    query=args.query,
                    ai_model_id=args.ai_model_id or DEFAULT_AI_MODEL_ID
                )
            elif name == "dappier_ai_recommendations":
                args = AIRecommendations(**arguments)
                response = client.get_ai_recommendations(
                    query=args.query,
                    data_model_id=args.data_model_id or DEFAULT_DATA_MODEL_ID,  # Default value
                    similarity_top_k=args.similarity_top_k or 9,  # Default value
                    ref=args.ref or "",  # Convert None to an empty string
                    num_articles_ref=args.num_articles_ref or 0,  # Default value
                    search_algorithm=args.search_algorithm or "most_recent",  # Default value
                )
            else:
                raise ValueError(f"Unknown tool: {name}")
            
            if response is None:
                raise McpError(ErrorData(code=INTERNAL_ERROR, message="An Unknown error occured."))
                
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        return [TextContent(
            type="text",
            text=format_results(response=response.model_dump()),
        )]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        if not arguments or "query" not in arguments:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="Query is required"))

        try:
            if name == "dappier_real_time_search":
                response = client.search_real_time_data(
                    query=arguments["query"],
                    ai_model_id=arguments.get("ai_model_id", DEFAULT_AI_MODEL_ID)
                )
            elif name == "dappier_ai_recommendations":
                response = client.get_ai_recommendations(
                    query=arguments["query"],  # Required field, assuming it is mandatory
                    data_model_id=arguments.get("data_model_id", DEFAULT_DATA_MODEL_ID),  # Default value
                    similarity_top_k=arguments.get("similarity_top_k", 9),  # Default value
                    ref=arguments.get("ref", ""),  # Default empty string
                    num_articles_ref=arguments.get("num_articles_ref", 0),  # Default value
                    search_algorithm=arguments.get("search_algorithm", "most_recent"),  # Default value
                )
            else:
                raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Unknown prompt: {name}"))
            
            if response is None:
                raise McpError(ErrorData(code=INTERNAL_ERROR, message="An Unknown error occured."))


        except (Exception) as e:
            return GetPromptResult(
                description=f"Failed to search: {str(e)}",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=str(e)),
                    )
                ],
            )

        return GetPromptResult(
            description=f"Search results for: {arguments['query']}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=format_results(response.model_dump())),
                )
            ],
        )

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

if __name__ == "__main__":
    import asyncio
    import os
    
    api_key = os.getenv("DAPPIER_API_KEY")
    if not api_key:
        raise ValueError("DAPPIER_API_KEY environment variable is required")
        
    asyncio.run(serve(api_key))
