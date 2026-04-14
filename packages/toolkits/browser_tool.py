from typing import Any

from packages.toolkits.base import BaseTool


class BrowserTool(BaseTool):
    name = "browser_action"
    description = "Automate browser actions using Playwright."
    risk_level = "high"

    async def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        action = params.get("action", "")
        if not action:
            return {"success": False, "error": "No action specified."}

        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()

                result: dict[str, Any] = {"success": True, "action": action}

                if action == "navigate":
                    url = params.get("url", "")
                    await page.goto(url)
                    result["url"] = url
                    result["title"] = await page.title()

                elif action == "click":
                    selector = params.get("selector", "")
                    await page.click(selector)
                    result["selector"] = selector

                elif action == "fill":
                    selector = params.get("selector", "")
                    value = params.get("value", "")
                    await page.fill(selector, value)
                    result["selector"] = selector

                elif action == "screenshot":
                    path = params.get("path", "screenshot.png")
                    await page.screenshot(path=path)
                    result["screenshot_path"] = path

                elif action == "get_text":
                    selector = params.get("selector", "body")
                    text = await page.text_content(selector)
                    result["text"] = text

                else:
                    result = {"success": False, "error": f"Unknown action: {action}"}

                await browser.close()
                return result

        except ImportError:
            return {"success": False, "error": "Playwright is not installed."}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
