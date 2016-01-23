#! /usr/bin/python
#Basic Webcrawler to Build Upon

# Imports
import requests
import os
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import csv
from urllib.parse import quote


# Insert Bitly Access Token
bitly_access_token = ''
bitly_prefix = 'https://api-ssl.bitly.com/v3/shorten?access_token=' + bitly_access_token + '&longurl='


def spider():
    # Request User Input
    set = input("What Set do you wish to crawl? \n")
    pages = input("How many pages?(Default=3) \n")

    # Set Page Count Default
    if pages == "":
        pages = 3
    else:
        pages = int(pages)

    # Enter URL here to Crawl
    url_prefix = "http://gatherer.wizards.com/Pages/Search/Default.aspx?page="
    # Default Page 0 = First Page
    page = 0
    # Add in necessary %20 in place of Spaces for URL
    user_input = set.replace(" ", "%20").strip()
    url_suffix = "&set=[%22"+user_input+"%22]"
    # Create Base Array for CSV output
    csv_array = []
    # Create PrettyTable for Text output
    x = PrettyTable(["Name", "Rarity", "Price", "Type", "Link"])
    # Poll over all pages defined by user
    while page < pages:
        url = url_prefix + str(page) + url_suffix
        # Grab full HTML Source Code from URL
        source_code = requests.get(url)
        # Convert to Plain Text
        plain = source_code.text
        # Create Soup (Filtering) object
        soup = BeautifulSoup(plain, 'html.parser')
        # Card Data
        card_data = soup.findAll('tr',class_='cardItem')
        for card in card_data:
            # Title of Card from the link text
            title = card.find(class_='cardTitle').a.text
            if title != 'Forest' and title != 'Island' and title != 'Swamp' and title!= 'Mountain' and title != 'Plains':
                price = find_price(set, title)
            else:
                price = 'N/A'
            # Link to card from HTML href
            link = card.find('a').get('href')
            full_link = "http://gatherer.wizards.com/Pages/" + link[3:]
            # Escape URL for Shortening
            escaped_url = quote(full_link)
            # Call Shorten API
            response = requests.get(bitly_prefix + escaped_url)
            # Collect Shortened URL from DICT
            short_link = response.json()['data']['url']
            # Type of card and remove blank leading spaces and extra characters
            type = card.find(class_='typeLine').text.strip().replace("\r\n","").replace(" ", "")
            # Find Rarity Title
            rarity_descripton = card.find(class_='rightCol').a.img['title']
            # Locate and retrieve only text between '(' and ')'
            find_rarity_start = rarity_descripton.find('(') + 1
            find_rarity_stop = rarity_descripton.rfind(')')
            rarity = rarity_descripton[find_rarity_start:find_rarity_stop]
            # Create Array with information
            array = [title, rarity, price,  type, short_link]
            # Append Array to its respective Master Array
            x.add_row(array)
            csv_array.append(array)
        page += 1
    # Print to Consol for User
    print(x)
    # Output to Text File
    text_file = open("Magic/" + set + ".txt", "w")
    text_file.write(str(x))
    text_file.close()
    # Output to CSV File
    csv_file = open("Magic/" + set + ".csv", "w")
    wr = csv.writer(csv_file)
    wr.writerows(csv_array)
    csv_file.close()
    exit()


def find_price(set_name, card_name):

    # Find URL
    urlbase = "http://www.mtggoldfish.com/price/"
    set = set_name.strip().replace(" ", "+")
    # Strip all symbols not allowed in URL
    card = card_name.strip().replace(" ","+").replace("\'","").replace("," , "").replace("Æ", "Ae")
    url = urlbase + set + "/" + card + "#online"
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    # Pull specific Div nested inside of another Div
    price = soup.findAll('div', class_='paper')[0].find('div', class_='price-box-price').text
    # Return Price in proper format
    return('$ ' + price)


# Define Main Function
def main():
    os.system('clear')
    spider()

main()
