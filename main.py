from fastmcp import FastMCP
from browser import toolcalls, BrowserHandler

if __name__ == "__main__":
    mcp = FastMCP()
    browser = BrowserHandler(headless=False)
    # network is still being made/fixed
    #browser.network = NetworkHandler()

    toolcalls(mcp, browser, "browser")
    #toolcalls(mcp, browser.network, "browser.network")

    mcp.run(transport="http")
