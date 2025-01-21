import requests

def get_articles():

    received_urls = []

    url = "https://newsapi.org/v2/everything"

    query = "Vance"

    params = {
        "from": "2024-10-17",
        "to" : "2024-10-23",
        "apiKey": "fd6a136b863e41ae91b3e66ad876ff31",
        "q" : query,
        "language" : "en",
        "page" : 0,
    }

    for i in range(1, 3):

        params["page"] = i
        response = requests.get(url, params).json()
        print(response["totalResults"])

        for article in response["articles"]:
            if article["url"] != "https://removed.com":
                received_urls.append(article["url"])


    return received_urls


urls = get_articles()

with open("urls.txt", "w") as f:
    for url in urls:
        f.write(str(url + "\n"))
