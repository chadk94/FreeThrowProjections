import pandas
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
import csv
import time
from selenium.webdriver.support import expected_conditions as EC


def GetLines():
    '''A function that returns all outstanding FreeThrows Made Lines'''

    # List of tags that prizepicks uses in their projections - that we want to keep
    attribute_tags = ['description', 'line_score', 'stat_type',]
    relationship_tags = ['league', 'name', 'position', 'team']

    # projection_tags = ['id'] + relationship_tags + attribute_tags
    projection_tags = relationship_tags + attribute_tags

    url = 'https://api.prizepicks.com/projections'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent={}".format(user_agent))
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')

    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

    browser.get(url)
    browser.implicitly_wait(10)
    # browser.get_screenshot_as_file('main-page.png')

    content = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.XPATH, "/html/body/pre"))
    content_json = json.loads(content.text)

    player_info = content_json['included']
    data = content_json['data']

    with open('projections.csv', mode='w', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=projection_tags, extrasaction='ignore', dialect='excel')
        writer.writeheader()

    # print(csv.list_dialects())

    # For each projection get the player name + info and store it all in a csv
        for projection in data:
            if projection['type'] == 'projection':
                id = projection['relationships']['new_player']['data']['id']
                for player in player_info:
                    if player['type'] == 'new_player':
                        if player['id'] == id:
                            # print(player['attributes'])
                            projection['relationships']['new_player']['data'] = player['attributes']
                            del projection['relationships']['stat_type']
                            del projection['relationships']['projection_type']
                            row = {
                                'id': projection['id']
                            }
                            for attribute in projection['attributes']:
                                row[attribute] = projection['attributes'][attribute]

                            for relationship in projection['relationships']:
                                if relationship == 'new_player':
                                    for key in projection['relationships']['new_player']['data']:
                                        row[key] = projection['relationships']['new_player']['data'][key]
                                else:
                                    row[relationship] = projection['relationships'][relationship]

                            writer.writerow(row)
    lines=pandas.read_csv("projections.csv")
    filter1 = lines['league'] == "WNBA"
    filter2 = lines['stat_type'] == "Free Throws Made"
    lines = lines.where(filter1 & filter2)
    lines=lines.dropna()
    excel = lines[["name", "line_score", "description"]]
    excel = excel.reset_index(drop=True)
    print(excel)
    return excel

def GetLines2():
    #added an alterntiv direct scrape for when havingapi issues
    driver = webdriver.Chrome()
    driver.get("https://app.prizepicks.com/")

    driver.find_element(By.CLASS_NAME, "close").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='NBA']").click()
    time.sleep(2)

    # Wait for the stat-container element to be present and visible
    stat_container = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

    # Find all stat elements within the stat-container
    # i.e. categories is the list ['Points','Rebounds',...,'Turnovers']
    categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')

    # Initialize empty list to store data
    nbaPlayers = []

    # Iterate over each stat element
    for category in categories:
        # Click the stat element
        line = '-' * len(category)
        print(line + '\n' + category + '\n' + line)
        if category != 'Free Throws Made':
            continue
        driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

        projections = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

        for projection in projections:
            names = projection.find_element(By.XPATH, './/div[@class="name"]').text
            points = projection.find_element(By.XPATH, './/div[@class="presale-score"]').get_attribute('innerHTML')
            opp = projection.find_element(By.XPATH, './/div[@class="opponent"]').text.replace('\n', '')
            print(names, points, opp[-3:])

            players = {'Name': names, 'Line': points, 'Opponent': opp[-3:]}

            nbaPlayers.append(players)
    return nbaPlayers