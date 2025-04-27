# Dappier MCP Server

Enable fast, free real-time web search and access premium data from trusted media brands—news, financial markets, sports, entertainment, weather, and more. Build powerful AI agents with Dappier.

<a href="https://smithery.ai/server/@DappierAI/dappier-mcp"><img alt="Smithery Badge" src="https://smithery.ai/badge/@DappierAI/dappier-mcp"></a>


<a href="https://glama.ai/mcp/servers/@DappierAI/dappier-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@DappierAI/dappier-mcp/badge" />
</a>

<br>
<br>

> Explore a wide range of data models in our marketplace at [marketplace.dappier.com](https://marketplace.dappier.com/marketplace).

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

## Getting Started

Get Dappier API Key. Head to [Dappier](https://platform.dappier.com/profile/api-keys) to sign up and generate an API key.


## Installing via Smithery

To install dappier-mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@DappierAI/dappier-mcp):

```bash
npx -y @smithery/cli install @DappierAI/dappier-mcp --client claude
```

## Installation

Install `uv` first.

**MacOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Certainly! Here's the updated markdown with instructions on how to access and edit the configuration files for Claude Desktop, Cursor, and Windsurf via their respective applications:

---

## Usage

### Claude Desktop

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

> **Hint**: You may need to provide the full path to the `uvx` executable in the `command` field. You can obtain this by running `which uvx` on macOS/Linux or `where uvx` on Windows.

**Configuration file location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Accessing via application:**
- **macOS**:
  1. Open the Claude Desktop application.
  2. In the menu bar, click on `Claude` > `Settings`.
  3. Navigate to the `Developer` tab.
  4. Click on `Edit Config` to open the configuration file in your default text editor.
- **Windows**:
  1. Open the Claude Desktop application.
  2. Click on the gear icon to access `Settings`.
  3. Navigate to the `Developer` tab.
  4. Click on `Edit Config` to open the configuration file in your default text editor.

> **Note**: If the `Developer` tab is not visible, ensure you're using the latest version of Claude Desktop. 

---

### Cursor

Update your Cursor configuration file (`mcp.json`) with the following content:

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

> **Hint**: You may need to provide the full path to the `uvx` executable in the `command` field. You can obtain this by running `which uvx` on macOS/Linux or `where uvx` on Windows.

**Configuration file location:**
- **Global Configuration**:
  - **macOS**: `~/.cursor/mcp.json`
  - **Windows**: `%USERPROFILE%\.cursor\mcp.json`
- **Project-Specific Configuration**:
  - Place the `mcp.json` file inside the `.cursor` directory within your project folder: `<project-root>/.cursor/mcp.json`

**Accessing via application:**
1. Open the Cursor application.
2. Navigate to `Settings` > `MCP`.
3. Click on `Add New Global MCP Server`.
4. The application will open the `mcp.json` file in your default text editor for editing.

> **Note**: On Windows, if the project-level configuration is not recognized, consider adding the MCP server through the Cursor settings interface. 

---

### Windsurf

Update your Windsurf configuration file (`mcp_config.json`) with the following content:

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

> **Hint**: You may need to provide the full path to the `uvx` executable in the `command` field. You can obtain this by running `which uvx` on macOS/Linux or `where uvx` on Windows.

**Configuration file location:**
- **macOS**: `~/.codeium/windsurf/mcp_config.json`
- **Windows**: `%USERPROFILE%\.codeium\windsurf\mcp_config.json`

**Accessing via application:**
1. Open the Windsurf application.
2. Navigate to `Settings` > `Cascade`.
3. Scroll down to the `Model Context Protocol (MCP) Servers` section.
4. Click on `View raw config` to open the `mcp_config.json` file in your default text editor.

> **Note**: After editing the configuration file, click the `Refresh` button in the MCP Servers section to apply the changes. 


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
