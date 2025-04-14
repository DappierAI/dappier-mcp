from typing import Annotated, Any, Dict, Optional, Literal
import os
import time

from pydantic import BaseModel, Field

# Synchronous MCP server, following the kagimcp style.
from mcp.server.fastmcp import FastMCP

from mcp.shared.exceptions import McpError
from mcp.types import (
    Tool,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    ErrorData,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)

# Dappier API client integration
from dappier import Dappier

# Initialize the FastMCP server instance and create the Dappier client.
mcp = FastMCP("dappier-mcp")
api_key = os.getenv("DAPPIER_API_KEY")
if not api_key:
    raise ValueError("DAPPIER_API_KEY environment variable is required")
client = Dappier(api_key=api_key)


@mcp.tool(
    annotations={
        "title": "Dappier Real-Time Search",
        "readOnlyHint": True,
        "openWorldHint": True,
    }
)
def dappier_real_time_search(
    query: Annotated[str, Field(description="The search query to retrieve real-time information.")],
    ai_model_id: Annotated[
        Literal["am_01j06ytn18ejftedz6dyhz2b15", "am_01j749h8pbf7ns8r1bq9s2evrh"],
        Field(
            description=(
                "The AI model ID to use for the query.\n\n"
                "Available AI Models:\n"
                "- am_01j06ytn18ejftedz6dyhz2b15: (Real Time Data) Access real-time Google web search results, including "
                "the latest news, weather, travel, deals, and more.\n"
                "- am_01j749h8pbf7ns8r1bq9s2evrh: (Stock Market Data) Access real-time financial news, stock prices, "
                "and trades from Polygon.io, with AI-powered insights and up-to-the-minute updates.\n\n"
            ),
        )
    ]
) -> str:
    """
    Retrieve real-time search data from Dappier by processing an AI model that supports two key capabilities:

    - Real-Time Web Search:  
    Access the latest news, weather, travel information, deals, and more using model `am_01j06ytn18ejftedz6dyhz2b15`.

    - Stock Market Data:  
    Retrieve real-time financial news, stock prices, and trade updates using model `am_01j749h8pbf7ns8r1bq9s2evrh`.

    Based on the provided `ai_model_id`, the tool selects the appropriate model and returns search results.
    """
    try:
        response = client.search_real_time_data(query=query, ai_model_id=ai_model_id)
        return format_results(response)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool(
    annotations={
        "title": "Dappier AI Recommendations",
        "readOnlyHint": True,
        "openWorldHint": True,
    }
)
def dappier_ai_recommendations(
    query: Annotated[
        str, 
        Field(description="The input string for AI-powered content recommendations.")
    ],
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
            description=(
                "The data model ID to use for recommendations.\n\n"
                "Available Data Models:\n"
                "- dm_01j0pb465keqmatq9k83dthx34: (Sports News) Real-time news, updates, and personalized content "
                "from top sports sources like Sportsnaut, Forever Blueshirts, Minnesota Sports Fan, LAFB Network, "
                "Bounding Into Sports, and Ringside Intel.\n"
                "- dm_01j0q82s4bfjmsqkhs3ywm3x6y: (Lifestyle News) Real-time updates, analysis, and personalized content "
                "from top sources like The Mix, Snipdaily, Nerdable, and Familyproof.\n"
                "- dm_01j1sz8t3qe6v9g8ad102kvmqn: (iHeartDogs AI) A dog care expert with access to thousands of articles "
                "on health, behavior, lifestyle, grooming, ownership, and more from the industry-leading pet community "
                "iHeartDogs.com.\n"
                "- dm_01j1sza0h7ekhaecys2p3y0vmj: (iHeartCats AI) A cat care expert with access to thousands of articles on "
                "health, behavior, lifestyle, grooming, ownership, and more from the industry-leading pet community "
                "iHeartCats.com.\n"
                "- dm_01j5xy9w5sf49bm6b1prm80m27: (GreenMonster) A helpful guide to making conscious and compassionate "
                "choices that benefit people, animals, and the planet.\n"
                "- dm_01jagy9nqaeer9hxx8z1sk1jx6: (WISH-TV AI) Covers sports, politics, breaking news, multicultural news, "
                "Hispanic language content, entertainment, health, and education.\n\n"
            ),
        )
    ],
    similarity_top_k: Annotated[
        int, 
        Field(default=9, description="Number of top similar articles to retrieve based on semantic similarity.")
    ] = 9,
    ref: Annotated[
        Optional[str],
        Field(default=None, description="The site domain where recommendations should be prioritized.")
    ] = None,
    num_articles_ref: Annotated[
        int,
        Field(default=0, description="Minimum number of articles to return from the reference domain.")
    ] = 0,
    search_algorithm: Annotated[
        Literal["most_recent", "semantic", "most_recent_semantic", "trending"],
        Field(default="most_recent", description="The search algorithm to use for retrieving articles.")
    ] = "most_recent"
) -> str:
    """
    Fetch AI-powered recommendations from Dappier by processing the provided query with a selected data model that tailors results to specific interests.

    - **Sports News (dm_01j0pb465keqmatq9k83dthx34):**  
    Get real-time news, updates, and personalized content from top sports sources.

    - **Lifestyle News (dm_01j0q82s4bfjmsqkhs3ywm3x6y):**  
    Access current lifestyle updates, analysis, and insights from leading lifestyle publications.

    - **iHeartDogs AI (dm_01j1sz8t3qe6v9g8ad102kvmqn):**  
    Tap into a dog care expert with access to thousands of articles covering pet health, behavior, grooming, and ownership.

    - **iHeartCats AI (dm_01j1sza0h7ekhaecys2p3y0vmj):**  
    Utilize a cat care specialist that provides comprehensive content on cat health, behavior, and lifestyle.

    - **GreenMonster (dm_01j5xy9w5sf49bm6b1prm80m27):**  
    Receive guidance for making conscious and compassionate choices benefiting people, animals, and the planet.

    - **WISH-TV AI (dm_01jagy9nqaeer9hxx8z1sk1jx6):**  
    Get recommendations covering sports, breaking news, politics, multicultural updates, and more.

    Based on the chosen `data_model_id`, the tool processes the input query and returns a formatted summary including article titles, summaries, images, source URLs, publication dates, and relevance scores.
    """
    try:
        response = client.get_ai_recommendations(
            query=query,
            data_model_id=data_model_id,
            similarity_top_k=similarity_top_k,
            ref=ref or "",
            num_articles_ref=num_articles_ref,
            search_algorithm=search_algorithm,
        )
        return format_results(response)
    except Exception as e:
        return f"Error: {str(e)}"

def format_results(response: Dict[str, Any]) -> str:
    """
    Helper function to format the API response into a human-readable string.
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
        formatted_text += (
            f"Result {idx}:\n"
            f"Title: {result.get('title', 'No title')}\n"
            f"Author: {result.get('author', 'Unknown author')}\n"
            f"Published on: {result.get('pubdate', 'No date available')}\n"
            f"Source: {result.get('site', 'Unknown site')} ({result.get('site_domain', 'No domain')})\n"
            f"URL: {result.get('source_url', 'No URL available')}\n"
            f"Image URL: {result.get('image_url', 'No URL available')}\n"
            f"Summary: {result.get('summary', 'No summary available')}\n"
            f"Score: {result.get('score', 'No score available')}\n\n"
        )
    return formatted_text

@mcp.list_tools()
def list_tools() -> list[Tool]:
    """
    Return a list of available tools for discovery.
    """
    return [
        Tool(
            name="dappier_real_time_search",
            description=(
                "Retrieve real-time search data from Dappier using an AI model that supports two capabilities:\n\n"
                "• Real-Time Web Search: Get the latest news, weather, stock prices, travel info, deals, etc. "
                "using model 'am_01j06ytn18ejftedz6dyhz2b15'.\n"
                "• Stock Market Data: Obtain financial news, stock prices, and trade updates using model "
                "'am_01j749h8pbf7ns8r1bq9s2evrh'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to retrieve real-time information."
                    },
                    "ai_model_id": {
                        "type": "string",
                        "enum": [
                            "am_01j06ytn18ejftedz6dyhz2b15",
                            "am_01j749h8pbf7ns8r1bq9s2evrh"
                        ],
                        "default": "am_01j06ytn18ejftedz6dyhz2b15",
                        "description": (
                            "The AI model ID to use for the query. Options:\n"
                            "- 'am_01j06ytn18ejftedz6dyhz2b15': For general web search results (news, weather, travel, deals, etc.)\n"
                            "- 'am_01j749h8pbf7ns8r1bq9s2evrh': For stock market data (financial news, stock prices, trades)"
                        )
                    }
                },
                "required": ["query"]
            },
            annotations={
                "title": "Dappier Real-Time Search",
                "readOnlyHint": True,
                "openWorldHint": True
            }
        ),
        Tool(
            name="dappier_ai_recommendations",
            description=(
                "Fetch AI-powered content recommendations from Dappier using a selected data model tailored to specific topics.\n\n"
                "Options include Sports News, Lifestyle News, iHeartDogs AI, iHeartCats AI, GreenMonster, and WISH-TV AI."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The input query for generating content recommendations."
                    },
                    "data_model_id": {
                        "type": "string",
                        "enum": [
                            "dm_01j0pb465keqmatq9k83dthx34",
                            "dm_01j0q82s4bfjmsqkhs3ywm3x6y",
                            "dm_01j1sz8t3qe6v9g8ad102kvmqn",
                            "dm_01j1sza0h7ekhaecys2p3y0vmj",
                            "dm_01j5xy9w5sf49bm6b1prm80m27",
                            "dm_01jagy9nqaeer9hxx8z1sk1jx6"
                        ],
                        "default": "dm_01j0pb465keqmatq9k83dthx34",
                        "description": (
                            "The data model ID to use for recommendations. Options:\n"
                            "- 'dm_01j0pb465keqmatq9k83dthx34': Sports News\n"
                            "- 'dm_01j0q82s4bfjmsqkhs3ywm3x6y': Lifestyle News\n"
                            "- 'dm_01j1sz8t3qe6v9g8ad102kvmqn': iHeartDogs AI\n"
                            "- 'dm_01j1sza0h7ekhaecys2p3y0vmj': iHeartCats AI\n"
                            "- 'dm_01j5xy9w5sf49bm6b1prm80m27': GreenMonster\n"
                            "- 'dm_01jagy9nqaeer9hxx8z1sk1jx6': WISH-TV AI"
                        )
                    },
                    "similarity_top_k": {
                        "type": "integer",
                        "default": 9,
                        "description": "Number of top similar articles to retrieve."
                    },
                    "ref": {
                        "type": "string",
                        "default": "",
                        "description": "Reference site domain to prioritize in results."
                    },
                    "num_articles_ref": {
                        "type": "integer",
                        "default": 0,
                        "description": "Minimum number of articles to return from the reference domain."
                    },
                    "search_algorithm": {
                        "type": "string",
                        "enum": ["most_recent", "semantic", "most_recent_semantic", "trending"],
                        "default": "most_recent",
                        "description": "The search algorithm to use (most_recent, semantic, most_recent_semantic, trending)."
                    }
                },
                "required": ["query"]
            },
            annotations={
                "title": "Dappier AI Recommendations",
                "readOnlyHint": True,
                "openWorldHint": True
            }
        )
    ]

@mcp.call_tool()
def call_tool(name: str, arguments: dict) -> list:
    """
    Execute the specified tool with the provided arguments.
    Returns a list of content objects (e.g., TextContent) for LLM consumption.
    """
    try:
        if name == "dappier_real_time_search":
            result = dappier_real_time_search(
                query=arguments["query"],
                ai_model_id=arguments.get("ai_model_id", "am_01j06ytn18ejftedz6dyhz2b15")
            )
            return [TextContent(type="text", text=result)]
        elif name == "dappier_ai_recommendations":
            result = dappier_ai_recommendations(
                query=arguments["query"],
                data_model_id=arguments.get("data_model_id", "dm_01j0pb465keqmatq9k83dthx34"),
                similarity_top_k=int(arguments.get("similarity_top_k", 9)),
                ref=arguments.get("ref", ""),
                num_articles_ref=int(arguments.get("num_articles_ref", 0)),
                search_algorithm=arguments.get("search_algorithm", "most_recent")
            )
            return [TextContent(type="text", text=result)]
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]




# Define reusable prompt templates.
PROMPTS = {
    "dappier_real_time_search": Prompt(
        name="dappier_real_time_search",
        description=(
            "Retrieve real-time search data from Dappier by processing a concise, keyword-focused query "
            "using an appropriate AI model.\n\n"
            "Arguments:\n"
            "  - query: The search query to retrieve real-time information.\n"
            "  - ai_model_id (optional): The AI model ID to use. Options:\n"
            "      * 'am_01j06ytn18ejftedz6dyhz2b15' for general web search results (news, weather, travel, deals, etc.)\n"
            "      * 'am_01j749h8pbf7ns8r1bq9s2evrh' for stock market data (financial news, stock prices, trades).\n"
            "Default is 'am_01j06ytn18ejftedz6dyhz2b15'."
        ),
        arguments=[
            PromptArgument(
                name="query",
                description="The search query to retrieve real-time information.",
                required=True
            ),
            PromptArgument(
                name="ai_model_id",
                description=(
                    "The AI model ID to use. Options:\n"
                    "- 'am_01j06ytn18ejftedz6dyhz2b15': For general web search results (news, weather, travel, deals, etc.)\n"
                    "- 'am_01j749h8pbf7ns8r1bq9s2evrh': For stock market data (financial news, stock prices, trades)\n"
                    "Default is 'am_01j06ytn18ejftedz6dyhz2b15'."
                ),
                required=False
            )
        ]
    ),
    "dappier_ai_recommendations": Prompt(
        name="dappier_ai_recommendations",
        description=(
            "Fetch AI-powered content recommendations from Dappier using a selected data model tailored to specific topics.\n\n"
            "Arguments:\n"
            "  - query: The input query for generating content recommendations.\n"
            "  - data_model_id (optional): The data model ID to use. Options:\n"
            "      * 'dm_01j0pb465keqmatq9k83dthx34': Sports News\n"
            "      * 'dm_01j0q82s4bfjmsqkhs3ywm3x6y': Lifestyle News\n"
            "      * 'dm_01j1sz8t3qe6v9g8ad102kvmqn': iHeartDogs AI\n"
            "      * 'dm_01j1sza0h7ekhaecys2p3y0vmj': iHeartCats AI\n"
            "      * 'dm_01j5xy9w5sf49bm6b1prm80m27': GreenMonster\n"
            "      * 'dm_01jagy9nqaeer9hxx8z1sk1jx6': WISH-TV AI\n"
            "Default is 'dm_01j0pb465keqmatq9k83dthx34'.\n"
            "  - similarity_top_k (optional): Number of top similar articles to retrieve (default: 9).\n"
            "  - ref (optional): Reference site domain to prioritize in results.\n"
            "  - num_articles_ref (optional): Minimum number of articles from the reference domain (default: 0).\n"
            "  - search_algorithm (optional): The search algorithm to use (options: most_recent, semantic, "
            "most_recent_semantic, trending)."
        ),
        arguments=[
            PromptArgument(
                name="query",
                description="The input query for generating content recommendations.",
                required=True
            ),
            PromptArgument(
                name="data_model_id",
                description=(
                    "The data model ID to use. Options:\n"
                    "- 'dm_01j0pb465keqmatq9k83dthx34': Sports News\n"
                    "- 'dm_01j0q82s4bfjmsqkhs3ywm3x6y': Lifestyle News\n"
                    "- 'dm_01j1sz8t3qe6v9g8ad102kvmqn': iHeartDogs AI\n"
                    "- 'dm_01j1sza0h7ekhaecys2p3y0vmj': iHeartCats AI\n"
                    "- 'dm_01j5xy9w5sf49bm6b1prm80m27': GreenMonster\n"
                    "- 'dm_01jagy9nqaeer9hxx8z1sk1jx6': WISH-TV AI\n"
                    "Default is 'dm_01j0pb465keqmatq9k83dthx34'."
                ),
                required=False
            ),
            PromptArgument(
                name="similarity_top_k",
                description="Number of top similar articles to retrieve (default: 9).",
                required=False
            ),
            PromptArgument(
                name="ref",
                description="Reference site domain to prioritize in results (optional).",
                required=False
            ),
            PromptArgument(
                name="num_articles_ref",
                description="Minimum number of articles from the reference domain (default: 0).",
                required=False
            ),
            PromptArgument(
                name="search_algorithm",
                description="The search algorithm to use (options: most_recent, semantic, most_recent_semantic, trending).",
                required=False
            )
        ]
    )
}

@mcp.list_prompts()
def list_prompts() -> list[Prompt]:
    """
    Return a list of available prompts.
    """
    return list(PROMPTS.values())

@mcp.get_prompt()
def get_prompt(name: str, arguments: Optional[Dict[str, Any]] = None) -> GetPromptResult:
    """
    Generate and return a prompt response based on the selected prompt name and provided arguments.
    
    This function validates required arguments and then delegates prompt generation by invoking the corresponding tool function.
    The result is returned as a formatted prompt message for client presentation.
    """
    if name not in PROMPTS:
        raise ValueError(f"Prompt not found: {name}")

    # Ensure that the 'query' argument is provided for both prompts
    if not arguments or "query" not in arguments:
        raise ValueError("The 'query' argument is required.")

    if name == "dappier_real_time_search":
        result = dappier_real_time_search(
            query=arguments["query"],
            ai_model_id=arguments.get("ai_model_id", "am_01j06ytn18ejftedz6dyhz2b15")
        )
        description = f"Real-time search results for: {arguments['query']}"
        message_text = result

    elif name == "dappier_ai_recommendations":
        result = dappier_ai_recommendations(
            query=arguments["query"],
            data_model_id=arguments.get("data_model_id", "dm_01j0pb465keqmatq9k83dthx34"),
            similarity_top_k=int(arguments.get("similarity_top_k", 9)),
            ref=arguments.get("ref", ""),
            num_articles_ref=int(arguments.get("num_articles_ref", 0)),
            search_algorithm=arguments.get("search_algorithm", "most_recent")
        )
        description = f"Content recommendations for: {arguments['query']}"
        message_text = result

    else:
        raise ValueError(f"Unsupported prompt: {name}")

    return GetPromptResult(
        description=description,
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=message_text
                )
            )
        ]
    )

def main():
    """
    Entry point for the Dappier MCP server.
    
    This function initializes the FastMCP server and starts it, so that the server can begin
    processing incoming tool and prompt requests.
    """
    try:
        # You may want to include additional logging or configuration here if desired.
        print("Starting the Dappier MCP server...")
        mcp.run()
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}")

if __name__ == "__main__":
    # Ensure that the DAPPIER_API_KEY environment variable is set before starting the server.
    if not os.getenv("DAPPIER_API_KEY"):
        raise ValueError("DAPPIER_API_KEY environment variable is required")
    
    main()
