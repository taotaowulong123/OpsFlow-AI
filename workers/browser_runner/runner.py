from typing import Any


class BrowserRunner:
    """Manages a Playwright browser lifecycle for running automation actions."""

    def __init__(self) -> None:
        self._browser = None
        self._playwright = None

    async def _ensure_browser(self) -> Any:
        if self._browser is None:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=True)
        return self._browser

    async def run_action(self, action_type: str, params: dict[str, Any]) -> dict[str, Any]:
        try:
            browser = await self._ensure_browser()
            page = await browser.new_page()

            result: dict[str, Any] = {"success": True, "action": action_type}

            if action_type == "navigate":
                await page.goto(params.get("url", ""))
                result["title"] = await page.title()

            elif action_type == "click":
                await page.goto(params.get("url", "")) if params.get("url") else None
                await page.click(params.get("selector", ""))

            elif action_type == "fill":
                await page.goto(params.get("url", "")) if params.get("url") else None
                await page.fill(params.get("selector", ""), params.get("value", ""))

            elif action_type == "screenshot":
                await page.goto(params.get("url", "")) if params.get("url") else None
                path = params.get("path", "screenshot.png")
                await page.screenshot(path=path)
                result["screenshot_path"] = path

            elif action_type == "extract_text":
                await page.goto(params.get("url", "")) if params.get("url") else None
                selector = params.get("selector", "body")
                result["text"] = await page.text_content(selector)

            else:
                result = {"success": False, "error": f"Unknown action: {action_type}"}

            await page.close()
            return result

        except ImportError:
            return {"success": False, "error": "Playwright is not installed."}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    async def close(self) -> None:
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
