"""Command line interface for MCPify."""

import argparse
import json
import os
import sys
from pathlib import Path

from .detect import BaseDetector, CamelDetector, OpenaiDetector
from .validate import print_validation_results, validate_config_file
from .wrapper import MCPWrapper


def _get_output_filename(project_path: Path, suffix: str = "") -> str:
    """Generate output filename based on project path."""
    # Use the resolved directory name for "." paths
    if project_path.name == "." or not project_path.name:
        project_name = project_path.resolve().name
    else:
        project_name = project_path.name

    if suffix:
        return f"{project_name}-{suffix}.json"
    else:
        return f"{project_name}.json"


def _run_detection(
    detector: BaseDetector, project_path: Path, output_file: Path
) -> None:
    """Common detection logic for all detector types."""
    print(f"Analyzing project: {project_path}")

    try:
        # Detect the API
        config = detector.detect_project(str(project_path))

        # Write configuration to file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

        print(f"✅ API specification extracted to {output_file}")
        print(f"📊 Detected {len(config.get('tools', []))} tools")
        backend_type = config.get("backend", {}).get("type", "unknown")
        print(f"🔧 Project type: {backend_type}")

        # Validate the generated configuration
        from .validate import validate_config_dict

        result = validate_config_dict(config)

        if result.is_valid and not result.warnings:
            print("✅ Generated configuration is valid")
        else:
            print(f"\n📋 Validation: {result.get_summary()}")
            if result.warnings:
                print("\n⚠️  Warnings:")
                for warning in result.warnings:
                    print(f"  • {warning.field}: {warning.message}")

    except Exception as e:
        print(f"❌ Error during detection: {e}")
        sys.exit(1)


def openai_detect_command(args: argparse.Namespace) -> None:
    """Handle the openai-detect command."""
    project_path = Path(args.project_path)

    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = Path(_get_output_filename(project_path, "openai"))

    # Create OpenAI detector (let it handle env var checking)
    try:
        detector = OpenaiDetector(openai_api_key=args.openai_key)
        print("🤖 Using OpenAI GPT-4 for intelligent detection...")
        _run_detection(detector, project_path, output_file)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating OpenAI detector: {e}")
        sys.exit(1)


def camel_detect_command(args: argparse.Namespace) -> None:
    """Handle the camel-detect command."""
    project_path = Path(args.project_path)

    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = Path(_get_output_filename(project_path, "camel"))

    # Create Camel-AI detector
    try:
        detector = CamelDetector(model_name=args.model_name)
        print("🐪 Using Camel-AI ChatAgent for intelligent detection...")
        _run_detection(detector, project_path, output_file)
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("💡 Install camel-ai with: pip install camel-ai")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating Camel-AI detector: {e}")
        sys.exit(1)


def detect_command(args: argparse.Namespace) -> None:
    """Handle the detect command with auto-selection strategy."""
    project_path = Path(args.project_path)

    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = Path(_get_output_filename(project_path))

    print("🎯 Auto-detecting best strategy...")

    detector: BaseDetector
    # Try Camel-AI if available (most advanced)
    try:
        detector = CamelDetector()
        print("🐪 Using Camel-AI detection (best available)...")
        _run_detection(detector, project_path, output_file)
        return
    except Exception as e:
        print(f"⚠️  Camel-AI detection failed: {e}")
        print("📉 Falling back to OpenAI detection...")

    # Try OpenAI if API key is available (either via CLI or env var)
    if args.openai_key or os.getenv("OPENAI_API_KEY"):
        try:
            detector = OpenaiDetector(openai_api_key=args.openai_key)
            print("🤖 Using OpenAI detection...")
            _run_detection(detector, project_path, output_file)
            return
        except Exception as e:
            print(f"⚠️  OpenAI detection failed: {e}")
            print("📉 No more fallback strategies available")

    # No more fallback options
    print(
        "❌ No detection strategies available. Please ensure you have API keys for OpenAI or Camel-AI."
    )
    sys.exit(1)


def view_command(args: argparse.Namespace) -> None:
    """Visually display the API specification."""
    config_file = Path(args.config_file)

    if not config_file.exists():
        print(f"❌ Error: Configuration file does not exist: {config_file}")
        sys.exit(1)

    print(f"Viewing configuration: {config_file}")

    try:
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)

        print(f"\n📋 API Specification: {config.get('name', 'Unknown')}")
        print(f"📝 Description: {config.get('description', 'No description')}")

        # Show backend information
        backend = config.get("backend", {})
        backend_type = backend.get("type", "unknown")
        print(f"🔧 Backend Type: {backend_type}")

        print(f"\n🛠️  Tools ({len(config.get('tools', []))}):")

        for tool in config.get("tools", []):
            print(f"  • {tool.get('name', 'Unknown')}")
            desc = tool.get("description", "No description")
            print(f"    Description: {desc}")
            print(f"    Args: {tool.get('args', [])}")
            if tool.get("parameters"):
                print("    Parameters:")
                for param in tool["parameters"]:
                    name = param.get("name", "Unknown")
                    ptype = param.get("type", "unknown")
                    desc = param.get("description", "No description")
                    print(f"      - {name} ({ptype}): {desc}")
            print()

        # Validate the configuration and show results
        from .validate import print_validation_results, validate_config_dict

        result = validate_config_dict(config)
        print("📊 Validation Results:")
        print_validation_results(result, verbose=args.verbose)

    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in config file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error viewing configuration: {e}")
        sys.exit(1)


def serve_command(args: argparse.Namespace) -> None:
    """Serve MCP server directly."""
    config_file = Path(args.config_file)

    if not config_file.exists():
        print(f"❌ Error: Configuration file does not exist: {config_file}")
        sys.exit(1)

    try:
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)

        # Direct serve mode
        print(f"🚀 Starting MCP server for {config.get('name', 'Unknown')}...")
        print(f"📡 Mode: {args.mode}")

        wrapper = MCPWrapper(str(config_file))

        if args.mode == "stdio":
            # Use existing wrapper for stdio mode
            wrapper.run()
        elif args.mode == "streamable-http":
            # Use wrapper with HTTP mode
            mcp_server = wrapper.server()

            # Start backend if needed
            if wrapper.adapter:
                import asyncio

                asyncio.run(wrapper.start_backend())

            try:
                print(f"🌐 Starting HTTP server on {args.host}:{args.port}")
                mcp_server.settings.host = args.host
                mcp_server.settings.port = args.port
                mcp_server.run(transport="streamable-http")
            finally:
                if wrapper.adapter:
                    import asyncio

                    asyncio.run(wrapper.stop_backend())
        else:
            print(f"❌ Error: Unsupported mode '{args.mode}'")
            sys.exit(1)

    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in config file: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


def validate_command(args: argparse.Namespace) -> None:
    """Handle the validate command."""
    config_file = Path(args.config_file)

    if not config_file.exists():
        print(f"❌ Error: Configuration file does not exist: {config_file}")
        sys.exit(1)

    print(f"Validating configuration: {config_file}")

    try:
        # Validate the configuration
        result = validate_config_file(config_file)

        # Print results
        print_validation_results(result, verbose=args.verbose)

        # Exit with appropriate code
        if not result.is_valid:
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error during validation: {e}")
        sys.exit(1)


def ui_command(args) -> None:
    """Launch the web UI for repository analysis."""
    try:
        import subprocess
        from pathlib import Path

        # Get the path to the UI app
        ui_app_path = Path(__file__).parent / "ui" / "app.py"

        if not ui_app_path.exists():
            print(f"❌ UI app not found at {ui_app_path}")
            print("Make sure the UI components are properly installed.")
            sys.exit(1)

        # Prepare streamlit arguments
        streamlit_args = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(ui_app_path),
            "--server.address",
            args.host,
            "--server.port",
            str(args.port),
        ]

        if args.dev:
            streamlit_args.extend(
                ["--server.runOnSave", "true", "--server.allowRunOnSave", "true"]
            )

        print(f"🚀 Starting MCPify UI at http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server")

        # Run streamlit as subprocess
        subprocess.run(streamlit_args)

    except ImportError:
        print("❌ Streamlit is not installed.")
        print("Install it with: pip install 'mcpify[ui]'")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 MCPify UI stopped")
    except Exception as e:
        print(f"❌ Failed to start UI: {e}")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description=(
            "MCPify - Automatically detect APIs and generate MCP server configurations"
        )
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Main detect command (auto-selection)
    detect_parser = subparsers.add_parser(
        "detect", help="Auto-detect APIs using best available strategy"
    )
    detect_parser.add_argument("project_path", help="Path to the project directory")
    detect_parser.add_argument(
        "--output", "-o", help="Output file path (default: <project-name>.json)"
    )
    detect_parser.add_argument(
        "--openai-key", help="OpenAI API key for enhanced detection if available"
    )

    # OpenAI detection command
    openai_parser = subparsers.add_parser(
        "openai-detect", help="Use OpenAI GPT-4 for intelligent API detection"
    )
    openai_parser.add_argument("project_path", help="Path to the project directory")
    openai_parser.add_argument(
        "--output", "-o", help="Output file path (default: <project-name>-openai.json)"
    )
    openai_parser.add_argument(
        "--openai-key", help="OpenAI API key (or set OPENAI_API_KEY env var)"
    )

    # Camel-AI detection command
    camel_parser = subparsers.add_parser(
        "camel-detect", help="Use Camel-AI ChatAgent for intelligent API detection"
    )
    camel_parser.add_argument("project_path", help="Path to the project directory")
    camel_parser.add_argument(
        "--output", "-o", help="Output file path (default: <project-name>-camel.json)"
    )
    camel_parser.add_argument(
        "--model-name", default="gpt-4", help="Model name to use (default: gpt-4)"
    )

    # View command
    view_parser = subparsers.add_parser(
        "view", help="View and validate MCP configuration file"
    )
    view_parser.add_argument(
        "config_file", help="Path to the configuration file to view"
    )
    view_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed validation results",
    )

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start MCP server")
    serve_parser.add_argument("config_file", help="Path to the configuration file")
    serve_parser.add_argument(
        "--mode",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Server mode (default: stdio)",
    )
    serve_parser.add_argument(
        "--host",
        default="localhost",
        help="Host for HTTP mode (default: localhost)",
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for HTTP mode (default: 8080)",
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate MCP configuration file"
    )
    validate_parser.add_argument(
        "config_file", help="Path to the configuration file to validate"
    )
    validate_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed validation results",
    )

    # UI command
    ui_parser = subparsers.add_parser(
        "ui", help="Launch the web UI for repository analysis"
    )
    ui_parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind the UI server (default: localhost)",
    )
    ui_parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port for the UI server (default: 8501)",
    )
    ui_parser.add_argument(
        "--dev",
        action="store_true",
        help="Run in development mode with auto-reload",
    )

    args = parser.parse_args()

    if args.command == "detect":
        detect_command(args)
    elif args.command == "openai-detect":
        openai_detect_command(args)
    elif args.command == "camel-detect":
        camel_detect_command(args)
    elif args.command == "view":
        view_command(args)
    elif args.command == "serve":
        serve_command(args)
    elif args.command == "validate":
        validate_command(args)
    elif args.command == "ui":
        ui_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
