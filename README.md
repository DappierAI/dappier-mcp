# Dappier MCP Server

Enable fast, free real-time web search and access premium data from trusted media brands—news, financial markets, sports, entertainment, weather, and more. Build powerful AI agents with Dappier.

<a href="https://smithery.ai/server/@DappierAI/dappier-mcp" target="_blank"><img alt="Smithery Badge" src="https://smithery.ai/badge/@DappierAI/dappier-mcp"></a>


<a href="https://glama.ai/mcp/servers/@DappierAI/dappier-mcp" target="_blank">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@DappierAI/dappier-mcp/badge" />
</a>

<br>
<br>

> Explore a wide range of data models in our marketplace at [marketplace.dappier.com](https://marketplace.dappier.com/marketplace).

## Video Walkthrough

<a href="https://youtu.be/JyfexpTmPbg" target="_blank" rel="noopener noreferrer">
  <img src="https://img.youtube.com/vi/JyfexpTmPbg/maxresdefault.jpg" alt="Watch the setup walkthrough">
</a>

> **Click the image to watch** the full video guide on setting up Dappier MCP with Claude Desktop.

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

## Features

The Dappier MCP Remote Server provides powerful real-time capabilities out of the box — no training or fine-tuning needed. Use it to build live, interactive tools powered by the latest web data, financial markets, or AI-curated content.

### Real-Time Web Search  
**Model ID:** `am_01j06ytn18ejftedz6dyhz2b15`  

Search the live web using Dappier’s AI-powered index. Get real-time access to:

- Breaking news from across the globe  
- Weather forecasts and local updates  
- Travel alerts and flight info  
- Trending topics and viral content  
- Online deals and shopping highlights  

Ideal for use cases like news agents, travel planners, alert bots, and more.

### Stock Market Insights  
**Model ID:** `am_01j749h8pbf7ns8r1bq9s2evrh`  

This model delivers instant access to market data, financial headlines, and trade insights. Perfect for portfolio dashboards, trading copilots, and investment tools.

It provides:

- Real-time stock prices  
- Financial news and company updates  
- Trade signals and trends  
- Market movement summaries  
- AI-curated analysis using live data from Polygon.io  

### AI-Powered Content Recommendations  

Choose from several domain-specific AI models tailored for content discovery, summarization, and feed generation.

#### Sports News  
**Model ID:** `dm_01j0pb465keqmatq9k83dthx34`  
Stay updated with real-time sports headlines, game recaps, and expert analysis.

#### Lifestyle Updates  
**Model ID:** `dm_01j0q82s4bfjmsqkhs3ywm3x6y`  
Explore curated lifestyle content — covering wellness, entertainment, and everyday inspiration.

#### iHeartDogs AI  
**Model ID:** `dm_01j1sz8t3qe6v9g8ad102kvmqn`  
Your intelligent dog care assistant — access training tips, health advice, and behavior insights.

#### iHeartCats AI  
**Model ID:** `dm_01j1sza0h7ekhaecys2p3y0vmj`  
An expert AI for all things feline — from nutrition to playtime to grooming routines.

#### GreenMonster  
**Model ID:** `dm_01j5xy9w5sf49bm6b1prm80m27`  
Discover sustainable lifestyle ideas, ethical choices, and green innovations.

#### WISH-TV AI  
**Model ID:** `dm_01jagy9nqaeer9hxx8z1sk1jx6`  
Tap into hyperlocal news, politics, culture, health, and multicultural updates.

Each recommendation includes:

- A clear title and concise summary  
- The original publication date  
- The trusted source and domain  
- Image preview (if available)  
- A relevance score for prioritization

Advanced options let you:

- Tune the search algorithm (`semantic`, `most_recent`, `trending`, etc.)  
- Focus results on a specific domain (`ref`)  
- Adjust how many results you want (`similarity_top_k`, `num_articles_ref`)  

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
