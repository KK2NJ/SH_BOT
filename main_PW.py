import json  
import nodriver as uc
import asyncio

async def main():

    browser = await uc.start(headless=False)

    page = await browser.get('https://www.scrapingcourse.com/cloudflare-challenge')

    await asyncio.sleep(180)

    origin = await page.evaluate("window.location.origin")

    cookies = await browser.cookies.get_all()

    cookies_formatted = [
        {
            "name" : c.name,
            "value" : c.value,
            "domain" : c.domain,
            "path" : c.path,
            "expires" : c.expires if c.expires is not None else -1.0,
            "httpOnly" : c.httpOnly,
            "secure" : c.secure,
            "sameSite" : c.sameSite.name.capitalize() if c.sameSite else "Lax"
        }
        for c in cookies
    ]

    local_storage_items = await page.get_local_storage()
    local_storage = [
        {"name": key, "value": value}
        for key, value in local_storage_items.items()
    ]

    data = {
        "cookies": cookies_formatted,
        "origins": [
            {
                "origin": origin,
                "local_storage": local_storage
            }
        ]
    }

    with open("auth.json", "w") as f:
        json.dump(data, f, indent=2)
    

    await asyncio.sleep(5)

    await browser.stop()


if __name__ == '__main__':
    uc.loop().run_until_complete(main())
