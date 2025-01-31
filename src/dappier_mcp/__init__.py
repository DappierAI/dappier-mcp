from .server import serve


def main():
    """MCP Dappier Server - Use Dappier RAG models for MCP"""
    import argparse
    import asyncio
    import os
    
    parser = argparse.ArgumentParser(
        description="give a model the ability to perform AI-powered web search using Dappier"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Dappier API key (can also be set via DAPPIER_API_KEY environment variable)",
    )

    args = parser.parse_args()
    
    # Check for API key in args first, then environment
    api_key = args.api_key or os.getenv("DAPPIER_API_KEY")
    if not api_key:
        parser.error("Dappier API key must be provided either via --api-key or DAPPIER_API_KEY environment variable")
    
    asyncio.run(serve(api_key))


if __name__ == "__main__":
    main()
