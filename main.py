import asyncio
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import random
window_amount = 1
windowless = False
page = 'PUT_SITE_URL_HERE'
async def run_browser(driver):
    try:
        driver.get(page)
        print(f"Loaded Site > {page}")
        await asyncio.sleep(5)
        try:
            center_x = 10
            center_y = 10
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), center_x, center_y)
            actions.click()
            actions.perform()
            print("Clicked Ad")
            await asyncio.sleep(10)
            driver.quit()
            await main()
        except Exception as e:
            driver.quit()
            await main()
            print(e)
    finally:
        driver.quit()

async def main():
    chrome_service = ChromeService(executable_path=r'CHROME_DRIVER_LOCATION_GOES_HERE')
    proxy_list = []
    with open('proxies.txt', 'r') as file:
        proxy_list = file.read().splitlines()

    while True:
        try:
            tasks = []
            for _ in range(window_amount):
                if windowless == True:
                    print("Windowless Mode Selected")
                    options = webdriver.ChromeOptions()
                    proxy = random.choice(proxy_list)
                    options.add_argument("--headless")
                    options.add_argument(f'--proxy-server={proxy}')
                    print(f"Using Proxy {proxy}")
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                    options.add_argument(f'user-agent={user_agent}')
                    driver = webdriver.Chrome(service=chrome_service, options=options)
                    tasks.append(asyncio.create_task(run_browser(driver)))
                else:
                    print("Window Mode Selected")
                    options = webdriver.ChromeOptions()
                    proxy = random.choice(proxy_list)
                    options.add_argument(f'--proxy-server={proxy}')
                    print(f"Using Proxy {proxy}")
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                    options.add_argument(f'user-agent={user_agent}')
                    driver = webdriver.Chrome(service=chrome_service, options=options)
                    tasks.append(asyncio.create_task(run_browser(driver)))    
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)
            print("Restarting")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
if __name__ == '__main__':
    asyncio.run(main())


