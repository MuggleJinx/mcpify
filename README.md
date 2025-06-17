[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/camel-ai-mcpify-badge.png)](https://mseep.ai/app/camel-ai-mcpify)

# MCPify - Export all projects as MCP servers!

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MCPify** is a powerful tool that automatically detects APIs in existing projects and transforms them into [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers. This enables seamless integration of your existing command-line tools, web APIs, and applications with AI assistants and other MCP-compatible clients.

## 🚀 Features

- **Intelligent API Detection**: Multiple advanced detection strategies
  - **🤖 OpenAI Detection**: Use GPT-4 for intelligent API analysis and tool extraction
  - **🐪 Camel-AI Detection**: Leverage Camel-AI's ChatAgent framework for comprehensive analysis
  - **🔍 AST Detection**: Static code analysis using Abstract Syntax Trees
  - **🎯 Auto-Selection**: Automatically choose the best available detection strategy
- **Multiple Project Types**: Support for various project architectures
  - **CLI Tools**: Detect argparse, click, typer-based command-line interfaces
  - **Web APIs**: Support for Flask, Django, and FastAPI applications with route detection
  - **Interactive Commands**: Identify command-based interactive applications
  - **Python Modules**: Extract callable functions and methods
- **Flexible MCP Server**: Multiple ways to start and control MCP servers
- **Multiple Backend Support**: Works with command-line tools, HTTP APIs, Python modules, and more
- **Configuration Validation**: Built-in validation system to ensure correct configurations
- **Parameter Detection**: Automatically extract route parameters, query parameters, and CLI arguments
- **Zero Code Changes**: Transform existing projects without modifying their source code
- **Professional Architecture**: Clean separation between detection, configuration, and server execution

## 📦 Installation

### Using pip (recommended)

```bash
pip install mcpify
```

### From source

```bash
git clone https://github.com/your-username/mcpify.git
cd mcpify
pip install -e .
```

### Optional Dependencies

For enhanced detection capabilities:

```bash
# For OpenAI-powered detection
pip install openai
export OPENAI_API_KEY="your-api-key"

# For Camel-AI powered detection
pip install camel-ai
```

## 🏗️ Project Architecture

```
mcpify/
├── mcpify/                    # Core package
│   ├── cli.py                 # CLI interface with detection commands
│   ├── __main__.py            # Module entry point
│   ├── wrapper.py             # MCP protocol wrapper
│   ├── backend.py             # Backend adapters
│   ├── detect/                # Detection module
│   │   ├── __init__.py        # Module exports
│   │   ├── base.py            # Base detector class
│   │   ├── ast.py             # AST-based detection
│   │   ├── openai.py          # OpenAI-powered detection
│   │   ├── camel.py           # Camel-AI detection
│   │   ├── factory.py         # Detector factory
│   │   └── types.py           # Type definitions
│   └── validate.py            # Configuration validation
├── examples/                  # Example projects
├── docs/                      # Documentation
└── tests/                     # Test suite
```

## 🛠️ Quick Start

### 1. Intelligent API Detection

MCPify offers multiple detection strategies. Use the best one for your needs:

```bash
# Auto-detection (recommended): Automatically selects the best available strategy
mcpify detect /path/to/your/project --output config.json

# OpenAI-powered detection: Most intelligent, requires API key
mcpify openai-detect /path/to/your/project --output config.json

# Camel-AI detection: Advanced agent-based analysis
mcpify camel-detect /path/to/your/project --output config.json

# AST detection: Fast, no API key required
mcpify ast-detect /path/to/your/project --output config.json
```

### 2. View and validate the configuration

```bash
mcpify view config.json
mcpify validate config.json
```

### 3. Start the MCP server

```bash
# Method 1: Using mcpify CLI (recommended)
mcpify serve config.json

# Method 2: Direct module invocation
python -m mcpify serve config.json

# HTTP mode for web integration
mcpify serve config.json --mode streamable-http --port 8080
```

## 🎯 Detection Strategies

### Auto-Detection (Recommended)

The auto-detect command intelligently selects the best available strategy:

```bash
mcpify detect /path/to/project
```

**Selection Priority:**
1. **Camel-AI** (if installed) - Most comprehensive analysis
2. **OpenAI** (if API key available) - Intelligent LLM-based detection
3. **AST** (always available) - Reliable static analysis fallback

### OpenAI Detection 🤖

Uses GPT-4 for intelligent project analysis:

```bash
# With API key parameter
mcpify openai-detect /path/to/project --openai-key YOUR_API_KEY

# Using environment variable
export OPENAI_API_KEY="your-api-key"
mcpify openai-detect /path/to/project
```

**Advantages:**
- Understands complex code patterns and context
- Generates detailed descriptions and parameter information
- Excellent at identifying non-obvious API endpoints
- Handles multiple programming languages

### Camel-AI Detection 🐪

Uses Camel-AI's ChatAgent framework for comprehensive analysis:

```bash
# Install camel-ai first
pip install camel-ai

# Set OpenAI API key (required by Camel-AI)
export OPENAI_API_KEY="your-api-key"

# Run detection
mcpify camel-detect /path/to/project --model-name gpt-4
```

**Advantages:**
- Advanced agent-based reasoning
- Deep project structure understanding
- Excellent for complex multi-file projects
- Sophisticated parameter extraction

### AST Detection 🔍

Fast, reliable static code analysis:

```bash
mcpify ast-detect /path/to/project
```

**Advantages:**
- No API key required
- Fast execution
- Reliable for standard patterns (argparse, Flask routes)
- Works offline

## 📋 Usage Scenarios

### For Developers (API Detection & Testing)
```bash
# Detect and test your APIs with different strategies
mcpify detect my-project --output my-project.json           # Auto-select best
mcpify openai-detect my-project --output my-project-ai.json # AI-powered
mcpify ast-detect my-project --output my-project-ast.json   # Static analysis

# Compare results
mcpify view my-project.json
mcpify serve my-project.json
```

### For AI-Enhanced Detection
```bash
# Use OpenAI for intelligent analysis
export OPENAI_API_KEY="your-key"
mcpify openai-detect complex-project --output smart-config.json

# Use Camel-AI for advanced agent analysis
pip install camel-ai
mcpify camel-detect complex-project --output agent-config.json
```

### For Production Deployment
```bash
# Generate configuration with best available strategy
mcpify detect production-app --output prod-config.json

# Deploy as HTTP server
mcpify serve prod-config.json --mode streamable-http --host 0.0.0.0 --port 8080
```

## 🔧 Backend Types & Examples

### FastAPI/Flask Web Applications
```json
{
  "name": "my-web-api",
  "description": "Web API server",
  "backend": {
    "type": "fastapi",
    "base_url": "http://localhost:8000"
  },
  "tools": [
    {
      "name": "get_user",
      "description": "Get user information",
      "endpoint": "/users/{user_id}",
      "method": "GET",
      "parameters": [
        {
          "name": "user_id",
          "type": "string",
          "description": "User ID"
        }
      ]
    }
  ]
}
```

### Python Modules
```json
{
  "name": "my-python-tools",
  "description": "Python module backend",
  "backend": {
    "type": "python",
    "module_path": "./my_module.py"
  },
  "tools": [
    {
      "name": "calculate",
      "description": "Perform calculation",
      "function": "calculate",
      "parameters": [
        {
          "name": "expression",
          "type": "string",
          "description": "Mathematical expression"
        }
      ]
    }
  ]
}
```

### Command-Line Tools
```json
{
  "name": "my-cli-tool",
  "description": "Command line tool backend",
  "backend": {
    "type": "commandline",
    "config": {
      "command": "python3",
      "args": ["./my_script.py"],
      "cwd": "."
    }
  },
  "tools": [
    {
      "name": "process_data",
      "description": "Process data with CLI tool",
      "args": ["--process", "{input_file}"],
      "parameters": [
        {
          "name": "input_file",
          "type": "string",
          "description": "Input file path"
        }
      ]
    }
  ]
}
```

## ⚙️ Detection Configuration

### Available Detection Commands

```bash
# Auto-detection with strategy selection
mcpify detect <project_path> [--output <file>] [--openai-key <key>]

# Specific detection strategies
mcpify openai-detect <project_path> [--output <file>] [--openai-key <key>]
mcpify camel-detect <project_path> [--output <file>] [--model-name <model>]
mcpify ast-detect <project_path> [--output <file>]

# Configuration management
mcpify view <config_file> [--verbose]
mcpify validate <config_file> [--verbose]
mcpify serve <config_file> [--mode <mode>] [--host <host>] [--port <port>]
```

### Supported Backend Types
- **`fastapi`**: FastAPI web applications
- **`flask`**: Flask web applications
- **`python`**: Python modules and functions
- **`commandline`**: Command-line tools and scripts
- **`external`**: External programs and services

### Server Modes
- **`stdio`**: Standard input/output (default MCP mode)
- **`streamable-http`**: HTTP Server-Sent Events mode

### Parameter Types
- `string`, `integer`, `number`, `boolean`, `array`
- Automatic type detection from source code
- Custom validation rules
- Enhanced type inference with AI detection

## 🚀 Server Configuration

### Command Line Options

```bash
# Basic usage
mcpify serve config.json

# Specify server mode
mcpify serve config.json --mode stdio              # Default mode
mcpify serve config.json --mode streamable-http    # HTTP mode

# Configure host and port (HTTP mode only)
mcpify serve config.json --mode streamable-http --host localhost --port 8080
mcpify serve config.json --mode streamable-http --host 0.0.0.0 --port 9999

# Real examples with provided configurations
mcpify serve examples/python-server-project/server.json
mcpify serve examples/python-server-project/server.json --mode streamable-http --port 8888
mcpify serve examples/python-cmd-tool/cmd-tool.json --mode stdio
```

### Server Modes Explained

#### STDIO Mode (Default)
- Uses standard input/output for communication
- Best for local MCP clients and development
- No network configuration needed

```bash
mcpify serve config.json
# or explicitly
mcpify serve config.json --mode stdio
```

#### Streamable HTTP Mode
- Uses HTTP with Server-Sent Events
- Best for web integration and remote clients
- Requires host and port configuration

```bash
# Local development
mcpify serve config.json --mode streamable-http --port 8080

# Production deployment
mcpify serve config.json --mode streamable-http --host 0.0.0.0 --port 8080
```

## 📁 Examples

Explore the `examples/` directory for ready-to-use configurations:

```bash
# Try different detection strategies on examples
mcpify detect examples/python-server-project --output server-auto.json
mcpify openai-detect examples/python-cmd-tool --output cmd-openai.json
mcpify ast-detect examples/python-server-project --output server-ast.json

# View example configurations
mcpify view examples/python-server-project/server.json
mcpify view examples/python-cmd-tool/cmd-tool.json

# Test with examples - STDIO mode (default)
mcpify serve examples/python-server-project/server.json
mcpify serve examples/python-cmd-tool/cmd-tool.json

# Test with examples - HTTP mode
mcpify serve examples/python-server-project/server.json --mode streamable-http --port 8888
mcpify serve examples/python-cmd-tool/cmd-tool.json --mode streamable-http --port 9999
```

## 🧪 Development

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=mcpify --cov-report=html

# Run specific tests
python -m pytest tests/test_detect.py -v
```

### Development Setup
```bash
git clone https://github.com/your-username/mcpify.git
cd mcpify
pip install -e ".[dev]"

# Install optional dependencies for full functionality
pip install openai camel-ai

python -m pytest tests/ -v
```

### Available Commands

#### MCPify CLI Commands
```bash
# Detection commands
mcpify detect <project_path> [--output <file>] [--openai-key <key>]
mcpify openai-detect <project_path> [--output <file>] [--openai-key <key>]
mcpify camel-detect <project_path> [--output <file>] [--model-name <model>]
mcpify ast-detect <project_path> [--output <file>]

# Configuration commands
mcpify view <config_file> [--verbose]
mcpify validate <config_file> [--verbose]

# Server commands
mcpify serve <config_file> [--mode <mode>] [--host <host>] [--port <port>]
```

## 🚀 Deployment Options

### 1. Package Installation
```bash
pip install mcpify
# Use mcpify serve for all scenarios
```

### 2. Module Invocation
```bash
# Run as Python module
python -m mcpify serve config.json
python -m mcpify serve config.json --mode streamable-http --port 8080
```

### 3. Docker Deployment
```dockerfile
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install .
# Optional: Install AI detection dependencies
# RUN pip install openai camel-ai
CMD ["mcpify", "serve", "config.json", "--mode", "streamable-http", "--host", "0.0.0.0", "--port", "8080"]
```

### 4. Production HTTP Server
```bash
# Start HTTP server for production
mcpify serve config.json --mode streamable-http --host 0.0.0.0 --port 8080

# With custom configuration
mcpify serve config.json --mode streamable-http --host 127.0.0.1 --port 9999
```

## 🤝 Contributing

We welcome contributions! Please see our development setup above and:

- Fork the repository
- Create a feature branch
- Add tests for new functionality
- Submit a pull request

### Code Quality
```bash
# Linting and formatting
ruff check mcpify/
ruff format mcpify/

# Type checking
mypy mcpify/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Model Context Protocol](https://modelcontextprotocol.io/) - The protocol specification
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Official Python implementation
- [OpenAI API](https://openai.com/api/) - For AI-powered detection
- [Camel-AI](https://github.com/camel-ai/camel) - Multi-agent framework for advanced detection

## 📞 Support

- **Documentation**: See `docs/usage.md` for detailed usage instructions
- **Examples**: Check the `examples/` directory for configuration templates
- **Issues**: [GitHub Issues](https://github.com/your-username/mcpify/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/mcpify/discussions)
