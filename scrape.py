import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Selenium options
options = Options()
options.add_argument("--headless")  # Run the browser in headless mode, without opening a window

# Set up the WebDriver
driver = webdriver.Chrome(service=Service("path/to/chromedriver"), options=options)

driver.get("https://play.stan.com.au/sport/tennis")

# Get the page source
page_source = driver.page_source

# Close the WebDriver
driver.quit()

# Regular expressions to extract the asset elements
asset_regex = r'<li class="entry">(.*?)</li>'

# Extract the asset elements using regular expressions
asset_matches = re.findall(asset_regex, page_source, re.DOTALL)

# Process the asset elements and extract the desired data
asset_list = []
for i, asset_html in enumerate(asset_matches, start=1):
    name_regex = r'alt="(.*?)"'
    id_regex = r'data-event-value="(.*?)"'
    image_regex = r'data-url="(.*?)"'
    start_date_regex = r'data-url=".*?~liveStartDate=(.*?)~.*?"'
    end_date_regex = r'data-url=".*?~liveEndDate=(.*?)~.*?"'

    asset_name_match = re.search(name_regex, asset_html)
    asset_id_match = re.search(id_regex, asset_html)
    asset_image_match = re.search(image_regex, asset_html)
    live_start_date_match = re.search(start_date_regex, asset_html)
    live_end_date_match = re.search(end_date_regex, asset_html)

    # Check if matches are found and extract the data
    if asset_name_match:
        asset_name = asset_name_match.group(1).strip()
    else:
        asset_name = "N/A"

    if asset_id_match:
        asset_id = asset_id_match.group(1)
    else:
        asset_id = "N/A"

    if asset_image_match:
        asset_image = asset_image_match.group(1)
    else:
        asset_image = "N/A"

    if live_start_date_match:
        live_start_date = live_start_date_match.group(1)
    else:
        live_start_date = "N/A"

    if live_end_date_match:
        live_end_date = live_end_date_match.group(1)
    else:
        live_end_date = "N/A"

    # Skip the asset with the name 'Wimbledon' or live start date more than 24 hours in the future
    if asset_name == "Wimbledon":
        continue

    current_timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    if live_start_date != "N/A" and int(live_start_date) - current_timestamp > 24 * 60 * 60 * 1000:
        continue

    # Check if the asset already exists in the HTML
    asset_exists = False
    for existing_asset in asset_list:
        if existing_asset["Asset ID"] == asset_id:
            asset_exists = True
            existing_asset["Asset Name"] = asset_name
            existing_asset["Asset Image"] = asset_image
            existing_asset["Live Start Date"] = live_start_date
            existing_asset["Live End Date"] = live_end_date
            break

    # Add the asset to the list if it doesn't exist
    if not asset_exists:
        asset_data = {
            "Asset Number": i,
            "Asset Name": asset_name,
            "Asset ID": asset_id,
            "Asset Image": asset_image,
            "Live Start Date": live_start_date,
            "Live End Date": live_end_date
        }
        asset_list.append(asset_data)

# Generate the asset elements for the HTML
asset_elements = ''
for asset_data in asset_list:
    asset_number = asset_data["Asset Number"]
    asset_name = asset_data["Asset Name"]
    asset_image = asset_data["Asset Image"]
    live_start_date = asset_data["Live Start Date"]
    live_end_date = asset_data["Live End Date"]

    # Skip the asset if the live end date is not "0"
    if live_end_date != "0":
        continue

    asset_element = f'''
      <div class="asset" id="asset-{asset_number}" draggable="true">
        <img class="asset-image" src="{asset_image}" alt="Asset Image">
        <div class="name">{asset_name}</div>
        <div class="livestart-date">{live_start_date}</div>
        <div class="liveend-date">{live_end_date}</div>
      </div>
    '''

    asset_elements += asset_element

# Read the HTML file
with open('index.html', 'r') as file:
    html_content = file.read()

# Delete existing asset elements in the HTML
html_content = re.sub(r'<div class="asset".*?</div>', '', html_content, flags=re.DOTALL)

# Find the position to insert the asset elements
insert_position = html_content.find('<script')

# Insert the asset elements into the HTML
updated_html_content = html_content[:insert_position] + asset_elements + html_content[insert_position:]

# Write the updated HTML content to the file
with open('public/index.html', 'w') as file:
    file.write(updated_html_content)

print('Asset data has been updated in the HTML file.')
