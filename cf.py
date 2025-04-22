import asyncio
from playwright.async_api import async_playwright

async def bypass_cf(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=False 更容易通过验证
        context = await browser.new_context()
        page = await context.new_page()

        print(f"访问 {url} 并等待 Cloudflare 验证通过...")
        await page.goto(url, wait_until="networkidle")  # 等待页面加载和 CF 验证
        await asyncio.sleep(8)  # 多等待几秒，确保验证结束

        content = await page.content()
        print("页面内容片段：", content[:500])  # 打印前500字符
        await browser.close()

if __name__ == "__main__":
    url = "https://api.trace.moe/"  # 替换成你要访问的网址
    asyncio.run(bypass_cf(url))