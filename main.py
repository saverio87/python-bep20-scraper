from selenium import webdriver
from time import sleep
import praw
import re

# Variables

USERNAME = ""
PASSWORD = ""

# Limit of submissions per subreddit
NUMBER_OF_SUBMISSIONS = '10'
# Creating client object for Reddit
reddit = praw.Reddit(
    client_id="3_RyX8HoZn59Lw",
    client_secret="aHMyns1xzUvBrvPmLFD67CBg1hQVcQ",
    password=PASSWORD,
    username=USERNAME,
    user_agent="testscript by ...",
)

# Links
subreddits = [
    'SatoshiStreetDegens',
    'moonshotcrypto',
    'CryptoMoonshots2',
    'CryptoMoonShotsDaily',
    'lowmarketcap',
    'SatoshiStreetDegens',
    'SatoshiStreetBets',
    'SatoshiCryptoBets',
    'SatoshiStreetBetsDE',
    'CryptoCurrencyStBets',
    'SatoshiBets'
]

base_url = 'https://charts.bogged.finance/?token='

# Functions

# Finding BEP20 addresses in subreddit submissions


def scrape_bep20():
    all_addresses = []
    regex = re.compile(r"""0x\w{40}""", re.VERBOSE)

    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).hot(limit=NUMBER_OF_SUBMISSIONS):
            # format text and make it lowercase to avoid duplicates
            submissionText = submission.selftext.lower()
            addresses = regex.findall(submissionText)
            for address in addresses:
                if not any(address in el for el in all_addresses):
                    all_addresses.append(address)
                else:
                    pass

    return all_addresses

# Scraping info relative to said addresses, specifically:
# TOKEN SYMBOL
# LIQUIDITY
# MARKET CAP


def scrape_info(addresses):

    driver = webdriver.Chrome("./chromedriver", options=None)

    for address in addresses:
        url = base_url + address
        print("Fetching {} data, please wait ...".format(url))

        driver.get(url)
        sleep(10)

        try:
            token_symbol = driver.find_element_by_css_selector(
                "body > div > div.flex-1.flex.flex-col.overflow-hidden > main > div > div > div > div > div.row-span-1.col-span-12.text-white.justify-between.flex.flex-col.lg\:flex-row.lg\:items-center > div.flex.flex-row.mr-4.w-full.overflow-y-hidden.overflow-x-hidden.flex-wrap.sm\:px-0.px-2 > div.my-1.flex.flex-row.space-x-3.sm\:space-x-6.mr-6.mb-3.md\:mb-0 > span.flex.flex-row > span > h4")
            market_cap = driver.find_element_by_css_selector(
                "body > div > div.flex-1.flex.flex-col.overflow-hidden > main > div > div > div > div > div.row-span-1.col-span-12.text-white.justify-between.flex.flex-col.lg\:flex-row.lg\:items-center > div.flex.flex-row.mr-4.w-full.overflow-y-hidden.overflow-x-hidden.flex-wrap.sm\:px-0.px-2 > div.my-1.flex.flex-row.justify-start.space-x-3.md\:pt-0.pt-3.sm\:space-x-6.w-full.md\:w-auto.border-t.md\:border-t-0.border-gray-200.dark\:border-gray-700 > span:nth-child(3) > h4")
            liquidity = driver.find_element_by_css_selector(
                "body > div > div.flex-1.flex.flex-col.overflow-hidden > main > div > div > div > div > div.row-span-1.col-span-12.text-white.justify-between.flex.flex-col.lg\:flex-row.lg\:items-center > div.flex.flex-row.mr-4.w-full.overflow-y-hidden.overflow-x-hidden.flex-wrap.sm\:px-0.px-2 > div.my-1.flex.flex-row.justify-start.space-x-3.md\:pt-0.pt-3.sm\:space-x-6.w-full.md\:w-auto.border-t.md\:border-t-0.border-gray-200.dark\:border-gray-700 > span:nth-child(2) > h4")

            with open('Tokens-info.txt', 'a') as file:
                file.write("TOKEN: {}\n".format(token_symbol.text))
                file.write("ADDRESS: {}\n".format(address))
                file.write("MARKET CAP: {}\n".format(market_cap.text))
                file.write("LIQUIDITY: {}\n".format(liquidity.text))
                file.write("--------\n")
                file.write("\n")

        except Exception as e:
            print("The following error has occurred:")
            print(e)
            pass

    driver.quit()


def main():
    addresses = scrape_bep20()
    scrape_info(addresses)


main()
