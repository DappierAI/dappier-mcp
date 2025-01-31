# Dappier MCP Server  

[![smithery badge](https://smithery.ai/badge/dappier)](https://smithery.ai/server/dappier)

## Setup Instructions  

### Install `uv` First  

**MacOS/Linux:**  
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**  
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

### **Setup with Claude Desktop**  

```json
# claude_desktop_config.json
# Find location via:
# Hamburger Menu -> File -> Settings -> Developer -> Edit Config
{
  "mcpServers": {
    "dappier": {
      "command": "uvx",
      "args": ["dappier"],
      "env": {
        "DAPPIER_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

---

### **Installing via Smithery**  

Alternatively, you can install **Dappier for Claude Desktop** automatically via [Smithery](https://smithery.ai/server/dappier):  

```bash
npx -y @smithery/cli install dappier --client claude
```

---

### **Ask Claude a Question Using Dappier AI**  

e.g.  
- `"Find trending articles on AI advancements."`  
- `"What are the latest stock market trends?"`  
- `"Show me sports news from the past 24 hours."`  

---

### **Debugging**  

Run:  
```bash
npx @modelcontextprotocol/inspector uvx dappier
```

---

## **Local/Dev Setup Instructions**  

### **Clone Repo**  
```bash
git clone https://github.com/dappier-ai/dappier-mcp.git
```

### **Install Dependencies**  

First, install `uv` (if not already installed):  

**MacOS/Linux:**  
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**  
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install MCP server dependencies:  

```bash
cd dappier-mcp

# Create virtual environment and activate it
uv venv

source .venv/bin/activate  # MacOS/Linux
# OR
.venv/Scripts/activate  # Windows

# Install dependencies
uv sync
```

---

### **Setup with Claude Desktop**  

#### **Using MCP CLI SDK**  
```bash
# If you haven't installed the MCP CLI SDK:
pip install mcp[cli]

mcp install /ABSOLUTE/PATH/TO/PARENT/FOLDER/dappier-mcp/src/dappier/server.py -v "DAPPIER_API_KEY=API_KEY_HERE"
```

#### **Manual Setup**  

```json
# claude_desktop_config.json
# Find location via:
# Hamburger Menu -> File -> Settings -> Developer -> Edit Config
{
  "mcpServers": {
    "dappier": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/dappier-mcp",
        "run",
        "dappier"
      ],
      "env": {
        "DAPPIER_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

---

### **Ask Claude a Question Using Dappier AI**  

e.g.  
- `"Find trending articles on AI advancements."`  
- `"What are the latest stock market trends?"`  
- `"Show me sports news from the past 24 hours."`  

---

### **Debugging**  

Run:  
```bash
# If MCP CLI installed (`pip install mcp[cli]`)
mcp dev /ABSOLUTE/PATH/TO/PARENT/FOLDER/dappier-mcp/src/dappier/server.py

# If not
npx @modelcontextprotocol/inspector \
      uv \
      --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/dappier-mcp \
      run \
      dappier
```

Then access **MCP Inspector** at `http://localhost:5173`.  
You may need to add your **Dappier API Key** (`DAPPIER_API_KEY`) in the inspector's environment variables.  

---

### 🚀 **Dappier is Now Ready!**  
You're now set up to use **Dappier AI with Claude Desktop** for AI-powered recommendations and real-time search.  
