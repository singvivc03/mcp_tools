from mcp.server.fastmcp import FastMCP

from .chess_api import get_player_profile, get_player_stats

mcp = FastMCP('Chess.com')

@mcp.tool()
def get_chess_player_profile(username: str):
    """Get the public profile for a chess.com player by username"""
    return get_player_profile(username)

@mcp.tool()
def get_chess_player_stats(username: str):
    """Get the public stats for a chess.com player by username"""
    return get_player_stats(username)

def main():
    mcp.run('stdio')

if __name__ == '__main__':
    main()