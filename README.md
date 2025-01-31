# Dappier MCP Server

A Model Context Protocol (MCP) server that connects any LLM or Agentic AI to real-time, rights-cleared, proprietary data from trusted sources. Dappier enables your AI to become an expert in anything by providing access to specialized models, including Real-Time Web Search, News, Sports, Financial Stock Market Data, Crypto Data, and exclusive content from premium publishers. Explore a wide range of data models in our marketplace at [marketplace.dappier.com](https://marketplace.dappier.com/marketplace).

## Features

- **Real-Time Web Search**: Access real-time Google web search results, including the latest news, weather, stock prices, travel, deals, and more.
- **Stock Market Data**: Get real-time financial news, stock prices, and trades from Polygon.io, with AI-powered insights and up-to-the-minute updates.
- **AI-Powered Recommendations**: Personalized content discovery across Sports, Lifestyle News, and niche favorites like I Heart Dogs, I Heart Cats, Green Monster, WishTV, and many more.
- **Structured JSON Responses**: Rich metadata for articles, including titles, summaries, images, and source URLs.
- **Flexible Customization**: Choose from predefined data models, similarity filtering, reference domain filtering, and search algorithms.

## Tools

### 1. Real-Time Data Search
- **Name**: `dappier_real_time_search`
- **Description**: Retrieves direct answers to real-time queries using AI-powered search. This includes web search results, financial information, news, weather, stock market updates, and more.
- **Parameters**:
  - `query` (string, required): The user-provided input string for retrieving real-time data.
  - `ai_model_id` (string, optional): The AI model ID to use for the query. Defaults to `am_01j06ytn18ejftedz6dyhz2b15` (Real-Time Data).

### 2. AI Recommendations
- **Name**: `dappier_ai_recommendations`
- **Description**: Provides AI-powered content recommendations based on structured data models. Returns a list of articles with titles, summaries, images, and source URLs.
- **Parameters**:
  - `query` (string, required): The user-provided input string for AI recommendations.
  - `data_model_id` (string, optional): The data model ID to use for recommendations. Defaults to `dm_01j0pb465keqmatq9k83dthx34` (Sports News).
  - `similarity_top_k` (integer, optional): The number of top documents to retrieve based on similarity. Defaults to `9`.
  - `ref` (string, optional): The site domain where AI recommendations should be displayed. Defaults to `None`.
  - `num_articles_ref` (integer, optional): The minimum number of articles to return from the specified reference domain (`ref`). Defaults to `0`.
  - `search_algorithm` (string, optional): The search algorithm to use for retrieving articles. Options: `most_recent`, `semantic`, `most_recent_semantic`, `trending`. Defaults to `most_recent`.

## Setup Instructions

### 1. Get Dappier API Key
Head to [Dappier](https://platform.dappier.com/profile/api-keys) to sign up and generate an API key.

### 2. Install Dependencies
Install `uv` first.

**MacOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install Dappier MCP Server
```bash
pip install mcp-dappier
```

Or if you have `uv` installed:
```bash
uv pip install mcp-dappier
```

### 4. Configure Claude Desktop
Update your Claude configuration file (`claude_desktop_config.json`) with the following content:

```json
{
  "mcpServers": {
    "dappier": {
      "command": "uvx",
      "args": ["dappier-mcp"],
      "env": {
        "DAPPIER_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Configuration file location:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## Examples

### Real-Time Data Search
- **Query**: "How is the weather today in Austin, TX?"
- **Query**: "What is the latest news for Meta?"
- **Query**: "What is the stock price for AAPL?"

### AI Recommendations
- **Query**: "Show me the latest sports news."
- **Query**: "Find trending articles on sustainable living."
- **Query**: "Get pet care recommendations from IHeartDogs AI."

## Debugging

Run the MCP inspector to debug the server:
```bash
npx @modelcontextprotocol/inspector uvx dappier-mcp
```

## Contributing

We welcome contributions to expand and improve the Dappier MCP Server. Whether you want to add new search capabilities, enhance existing functionality, or improve documentation, your input is valuable.

For examples of other MCP servers and implementation patterns, see:
[https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

Pull requests are welcome! Feel free to contribute new ideas, bug fixes, or enhancements.