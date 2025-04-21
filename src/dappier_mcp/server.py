from typing import Annotated, Optional, Literal
import os

from pydantic import Field
from mcp.server.fastmcp import FastMCP
from dappier import Dappier
from dappier.types import AIRecommendationsResponse

mcp = FastMCP("dappier-mcp")
api_key = os.getenv("DAPPIER_API_KEY")
if not api_key:
    raise ValueError("DAPPIER_API_KEY environment variable is required")
client = Dappier(api_key=api_key)


@mcp.tool()
def dappier_real_time_search(
    query: Annotated[str, Field(description="The search query to retrieve real-time information.")],
    ai_model_id: Annotated[
        Literal["am_01j06ytn18ejftedz6dyhz2b15", "am_01j749h8pbf7ns8r1bq9s2evrh"],
        Field(
            description=(
                "The AI model ID to use for the query.\n\n"
                "Available AI Models:\n"
                "- am_01j06ytn18ejftedz6dyhz2b15: (Real-Time Data) Access real-time Google web search results, including "
                "the latest news, stock market data, news, weather, travel, deals, and more. Use this model when no stock ticker symbol is provided.\n"
                "- am_01j749h8pbf7ns8r1bq9s2evrh: (Stock Market Data) Access real-time financial news, stock prices, "
                "and trades from Polygon.io, with AI-powered insights and up-to-the-minute updates. Use this model only when a stock ticker symbol is provided.\n\n"
            ),
        )
    ]
) -> str:
    """
    Retrieve real-time search data from Dappier by processing an AI model that supports two key capabilities:

    - Real-Time Web Search:  
    Access the latest news, stock market data, weather, travel information, deals, and more using model `am_01j06ytn18ejftedz6dyhz2b15`.  
    Use this model when no stock ticker symbol is provided.

    - Stock Market Data:  
    Retrieve real-time financial news, stock prices, and trade updates using model `am_01j749h8pbf7ns8r1bq9s2evrh`.  
    Use this model only when a stock ticker symbol is provided.

    Based on the provided `ai_model_id`, the tool selects the appropriate model and returns search results.
    """
    try:
        response = client.search_real_time_data(query=query, ai_model_id=ai_model_id)
        return response.message
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def dappier_ai_recommendations(
    query: Annotated[
        str, 
        Field(description="The input string for AI-powered content recommendations.")
    ],
    data_model_id: Annotated[
        Literal[
            "dm_01j0pb465keqmatq9k83dthx34",
            "dm_01j0q82s4bfjmsqkhs3ywm3x6y",
            "dm_01j1sz8t3qe6v9g8ad102kvmqn",
            "dm_01j1sza0h7ekhaecys2p3y0vmj",
            "dm_01j5xy9w5sf49bm6b1prm80m27",
            "dm_01jagy9nqaeer9hxx8z1sk1jx6",
        ],
        Field(
            description=(
                "The data model ID to use for recommendations.\n\n"
                "Available Data Models:\n"
                "- dm_01j0pb465keqmatq9k83dthx34: (Sports News) Real-time news, updates, and personalized content "
                "from top sports sources like Sportsnaut, Forever Blueshirts, Minnesota Sports Fan, LAFB Network, "
                "Bounding Into Sports and Ringside Intel.\n"
                "- dm_01j0q82s4bfjmsqkhs3ywm3x6y: (Lifestyle News) Real-time updates, analysis, and personalized content "
                "from top sources like The Mix, Snipdaily, Nerdable and Familyproof.\n"
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

def format_results(response: AIRecommendationsResponse) -> str:
    """
    Helper function to format the API response into a human-readable string.
    """
    if response.status != "success":
        return "The API response was not successful."

    query = response.response.query or "No query provided"
    results = response.response.results or []

    formatted_text = f"Search Query: {query}\n\n"
    for idx, result in enumerate(results, start=1):
        formatted_text += (
            f"Result {idx}:\n"
            f"Title: {result.title or 'No title'}\n"
            f"Author: {result.author or 'Unknown author'}\n"
            f"Published on: {result.pubdate or 'No date available'}\n"
            f"Source: {result.site or 'Unknown site'} ({result.site_domain or 'No domain'})\n"
            f"URL: {result.source_url or 'No URL available'}\n"
            f"Image URL: {result.image_url or 'No URL available'}\n"
            f"Summary: {result.summary or 'No summary available'}\n"
            f"Score: {result.score or 'No score available'}\n\n"
        )
    return formatted_text

def main():
    """
    Entry point for the Dappier MCP server.
    
    This function initializes the FastMCP server and starts it, so that the server can begin
    processing incoming tool requests.
    """
    try:
        mcp.run()
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}")

if __name__ == "__main__":
    if not os.getenv("DAPPIER_API_KEY"):
        raise ValueError("DAPPIER_API_KEY environment variable is required")
    
    main()
