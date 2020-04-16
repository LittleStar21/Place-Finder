import json, requests
from bs4 import BeautifulSoup
from random import randint

api_key = "Your API"

def main():
	places = searchPlace()

	# Print places name
	for i in range(len(places)):
		print(f"{i + 1}. {places[i]['name']}")
	print()

	# Get user's choice
	userChoice = getUserNumber(len(places))
	print()

	# Get distance's info
	distInfo = getDist(str(places[userChoice - 1]["geometry"]["location"]["lat"]), str(places[userChoice - 1]["geometry"]["location"]["lng"]))
	
	print()
	print(f"Name: {places[userChoice - 1]['name']}")
	print(f"Address: {places[userChoice - 1]['formatted_address']}")
	
	if "rating" in places[userChoice - 1]:
		print(f"Rating: {places[userChoice - 1]['rating']}")

	if distInfo["rows"][0]["elements"][0]["status"] == "OK":
		print(f"Distance: {distInfo['rows'][0]['elements'][0]['distance']['text']}")
		print(f"Duration: {distInfo['rows'][0]['elements'][0]['duration']['text']}")
	elif distInfo["rows"][0]["elements"][0]["status"] == "ZERO_RESULTS":
		print("No route can be found")
	print()
	
	printQuote()


def searchPlace():
	# Returns a list of the places
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
	while True:
		search = input("Search: ")
		respObj = requests.get(f"{url}query={search}&key={api_key}&opennow=True")
		resp = respObj.json()

		if resp["status"] == "OK":
			return resp["results"]
		else:
			print("No results found, please type more specifically")

def getUserNumber(n):
	# Returns the number of the user's choice
	while True:
		try:
			userChoice = int(input("Which place are you interested in?\nEnter the number: "))
			if userChoice < 1 or userChoice > n:
				print("No such choice are available")
			else:
				return userChoice
		except ValueError:
			print("Please enter a valid number")

def getDist(destLat, destLong):
	# Returns a dict of distances related info
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
	while True:
		origin = input("From: ")
		respObj = requests.get(f"{url}origins={origin}&destinations={destLat},{destLong}&key={api_key}")
		resp = respObj.json()

		if resp["status"] == "OK":
			if resp["rows"][0]["elements"][0]["status"] == "NOT_FOUND":
				print("Please insert your loaction specifically")
			else:
				return resp
		else:
			print("Invalid request")

def printQuote():
	# Prints a quote
	result = requests.get("https://www.goodreads.com/quotes")
	soup = BeautifulSoup(result.text, "html.parser")

	quotes = soup.find_all("div", {"class": "quoteText"})
	authors = soup.find_all("span", {"class": "authorOrTitle"})

	number = randint(0, len(quotes) - 1)
	quote = quotes[number].get_text().strip()
	print(quote[:quote.find("”") + 1])
	print(authors[number].get_text().strip())

if __name__ == "__main__":
	main()