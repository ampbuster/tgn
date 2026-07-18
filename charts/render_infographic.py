"""
Render the v10.2 mobile-friendly infographic HTML to a long, 800px wide JPEG.
Uses Playwright headless Chromium for high-fidelity rendering.
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def render_infographic():
    html_path = Path("/workspace/github/charts/v10-infographic/mobile.html").resolve()
    output_jpeg = Path("/workspace/github/charts/tgn-infographic-mobile-v10.2.jpg")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile-friendly: 800px wide viewport
        context = await browser.new_context(
            viewport={"width": 800, "height": 1200},
            device_scale_factor=2,  # High-DPI for sharp text
        )
        page = await context.new_page()
        await page.goto(f"file://{html_path}")
        # Wait for fonts to load
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        # Get full page height
        height = await page.evaluate("document.body.scrollHeight")
        print(f"Page height: {height}px")
        # Resize viewport to fit all content
        await page.set_viewport_size({"width": 800, "height": int(height) + 50})
        await page.wait_for_timeout(500)
        # Screenshot the full page
        await page.screenshot(
            path=str(output_jpeg),
            full_page=True,
            type="jpeg",
            quality=92,
        )
        await browser.close()
    print(f"Saved: {output_jpeg}")
    print(f"File size: {output_jpeg.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    asyncio.run(render_infographic())
