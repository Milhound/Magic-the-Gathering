import requests


# Find an individual card by id
def find_card():
    url = "http://api.deckbrew.com/mtg/cards?page="
    page = 0
    while page <= 136:
        cards = requests.get(url+str(page)).json()
        for card in cards:
            print(card['name'] + " - " + card['types'][0])

        page += 1


# Find card set by 3 letter code
def find_card_by_set(set):
    page = 0
    url = "http://api.deckbrew.com/mtg/cards?set="
    set_url = str(set)
    print(url + set_url)
    while page <= 2:
        page_url = "&page=" + str(page)
        cards = requests.get(url + set_url + page_url).json()
        for card in cards:
            try:
                print(card['name'] + " - " + card['types'][0] + " (" +card['power'] + "/" + card['toughness'] + ")")
            except KeyError:
                print(card['name'] + " - " + card['types'][0])
        page += 1


# List all possible sets
def list_card_sets():
    url = "http://api.deckbrew.com/mtg/sets"
    sets = requests.get(url).json()
    for set in sets:
        print(set['name']+" - \"%s\"" % set['id'])


# find_card_by_set('bfz') # Set codes can be found by running list_card_sets()
# list_card_sets()
