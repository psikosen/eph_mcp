# MCP Configuration for Claude Desktop

## Add this to your Claude Desktop config file

### For macOS:
Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

### For Windows:
Location: `%APPDATA%\Claude\claude_desktop_config.json`

### For Linux:
Location: `~/.config/Claude/claude_desktop_config.json`

## Configuration to Add:

```json
{
  "mcpServers": {
    "eph-mcp": {
      "command": "python3",
      "args": [
        "/Users/user/Downloads/cur_pro/eph_mcp_fastmcp.py"
      ],
      "env": {
        "TOKENIZERS_PARALLELISM": "false"
      }
    }
  }
}
```

## Alternative Configuration (if you have other MCP servers):

```json
{
  "mcpServers": {
    "eph-mcp": {
      "command": "python3",
      "args": [
        "/Users/user/Downloads/cur_pro/eph_mcp_fastmcp.py"
      ],
      "env": {
        "TOKENIZERS_PARALLELISM": "false"
      }
    },
    "your-other-server": {
      "command": "...",
      "args": ["..."]
    }
  }
}
```

## If you want to use the module version instead:

```json
{
  "mcpServers": {
    "eph-mcp": {
      "command": "python3",
      "args": [
        "-m",
        "eph_mcp.server"
      ],
      "cwd": "/Users/user/Downloads/cur_pro",
      "env": {
        "PYTHONPATH": "/Users/user/Downloads/cur_pro",
        "TOKENIZERS_PARALLELISM": "false"
      }
    }
  }
}
```

## Steps to Configure:

1. **Locate your Claude config file**:
   ```bash
   # On macOS, open the config directory:
   open ~/Library/Application\ Support/Claude/
   ```

2. **Edit or create `claude_desktop_config.json`**:
   ```bash
   # Create/edit the file:
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```
 