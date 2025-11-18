import json  
import nodriver as uc
import asyncio

async def main():

    browser = await uc.start(headless=False)

    page = await browser.get('https://www.scrapingcourse.com/cloudflare-challenge')

    await asyncio.sleep(30)

    origin = await page.evaluate("window.location.origin")

    cookies = await browser.cookies.get_all()

    cookies_formatted = [
        {
            "name" : c.name,
            "value" : c.value,
            "domain" : c.domain,
            "path" : c.path,
            "expires" : c.expires if c.expires is not None else -1.0,
            "httpOnly" : c.http_only,
            "secure" : c.secure,
            "sameSite" : c.same_site.name.capitalize() if c.same_site else "Lax"
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
    
    print("cookies and local storage saved to auth.json wherever tf it is")

    await asyncio.sleep(5)

    await browser.stop()


if __name__ == '__main__':
    uc.loop().run_until_complete(main())
