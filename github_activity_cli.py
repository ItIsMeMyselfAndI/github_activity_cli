import requests
import sys
import os

WIDTH = os.get_terminal_size().columns

class GithubActivity:
    @staticmethod
    def getInvalidUsernameMessage(url:str) -> tuple:
        response = requests.get(url).json()
        try:
            if "Not Found" in response["message"]:
                error = "[!] Invalid username.\n\tCheck username and try again."
            elif "API rate limit" in response["message"]:
                error = "[!] API rate limit exceeded.\n\tWait and try again later."
            else:
                error = "[!] Unexpected error occurred.\n\tTry again."
        except KeyError:
            return None
        message = (
            f"{"="*WIDTH}\n"
            f"\n{error}\n\n"
            f"{"="*WIDTH}\n"
        )
        return message

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
    def getBasicEvents(url:str) -> list:
        response = requests.get(url + "/events").json()
        events = []
        for event in response:
            events.append({event["type"]:event["repo"]["name"]})
        return events
    
    @staticmethod
    def _getUserRepos(url:str) -> list:
        response = requests.get(url).json()
        repos = [(repo["name"], repo["url"]) for repo in response]
        return repos
    
    @staticmethod
    def getDetailedEvents(url:str, token:str) -> list:
        # detailed
        repos = GithubActivity._getUserRepos(url + "/repos")
        headers = {"Authorization": f"Bearer {token}"}
        events = []
        for i, repo in enumerate(repos):
            if i != 4:
                continue
            response = requests.get(repo[1] + "/events", headers=headers).json()
            pushes_count = 0
            publics_count = 0
            for push in response:
                if push["type"] == "PushEvent":
                    pushes_count += 1
                elif push["type"] == "PublicEvent":
                    publics_count += 1
                print(push)
                print()

            event = None
            if pushes_count > 0:
                event = {repo[0]:{
                    "PushEvents":pushes_count,
                }}
            if publics_count > 0:
                event[repo[0]]["PublicEvents"] = publics_count
            event.append(event)
        return events
            


        

        


def _isValidArgv(argv:list) -> bool:
    message = (
        f"{"="*WIDTH}\n"
        "\n[!] Invalid command.\n"
        "\tCheck README.md file.\n\n"
        f"{"="*WIDTH}"
    )
    if (len(argv) <= 1) or (len(argv) > 3):
        print(message)
        return False
    return True

def main() -> None:
    if not _isValidArgv(sys.argv):
        return

    base_url = f"https://api.github.com"
    username, token = (sys.argv[1], None) if len(sys.argv) == 2 else (sys.argv[1], sys.argv[2])
    user_endpoint = f"{base_url}/users/{username}"
    repo_endpoint = f"{base_url}/repos/{username}"
    search_url = f"{base_url}/"

    message = GithubActivity.getInvalidUsernameMessage(user_endpoint)
    if message:
        print(message)
        return
    
    # following = GithubActivity.getUsernames(user_endpoint + "/following")
    # print(following)
    # print()
    # starred = GithubActivity.getFullNames(user_endpoint + "/starred")
    # print(starred)
    # print()
    # watching = GithubActivity.getFullNames(user_endpoint + "/subscriptions")
    # print(watching)
    # print()
    # my_events = GithubActivity.getEvents(user_endpoint)
    # print(my_events)
    # print()
    # print(GithubActivity.getBasicEvents(user_endpoint))
    # print()
    GithubActivity.getDetailedEvents(user_endpoint, token)


if __name__ == "__main__":
    print()
    main()
    print()