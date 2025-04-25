import requests
import sys
import os

WIDTH = os.get_terminal_size().columns

class GithubActivity:

    @staticmethod
    def getUsernames(url:str) -> list:
        response = requests.get(url).json()
        usernames = [user["login"] for user in response]
        return usernames
    
    @staticmethod
    def getFullNames(url:str) -> list:
        response = requests.get(url).json()
        usernames = [user["full_name"] for user in response]
        return usernames
    
    @staticmethod
    def getEvents(url:str) -> list:
        response = requests.get(url).json()
        events = []
        for event in response:
            events.append({event["type"]:event["repo"]["name"]})
        return events

    @staticmethod
    def getEventsSummary(url:str) -> list:
        pass

    




def main(username:str) -> None:
    base_url = f"https://api.github.com"
    user_url = f"{base_url}/users/{username}"
    search_url = f"{base_url}/"

    following = GithubActivity.getUsernames(user_url + "/following")
    print(following)
    print()
    starred = GithubActivity.getFullNames(user_url + "/starred")
    print(starred)
    print()
    watching = GithubActivity.getFullNames(user_url + "/subscriptions")
    print(watching)
    print()
    my_events = GithubActivity.getEvents(user_url + "/events")
    print(my_events)
    print()


if __name__ == "__main__":
    username = sys.argv[1]
    print()
    try:
        main(username)
    except TypeError:
        print("="*WIDTH)
        print("\n[!] API rate limit exceeded.")
        print("\tTry again later.\n")
        print("="*WIDTH)
    print()