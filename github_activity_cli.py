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
            f"{"="*WIDTH}"
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

    def getIssues(url:str) -> list:
            response = requests.get(url).json()
            issues = [{"repo":issue["repo"], "created_at":issue["created_at"] , 
                 "updated_at":issue["updated_at"]} for issue in response]
            return issues

    @staticmethod
    def getBasicEvents(url:str) -> list:
        response = requests.get(url + "/events").json()
        events = []
        for event in response:
            events.append({"type":event["type"], "repo":event["repo"]["name"]})
        return events
    
    @staticmethod
    def _getUserRepos(url:str, headers) -> list:
        response = requests.get(url, headers=headers).json()
        repos = [repo["url"] for repo in response]
        return repos
    
    @staticmethod
    def getDetailedEvents(url:str, token:str) -> list:
        headers = {"Authorization": f"Bearer {token}"}
        repos = GithubActivity._getUserRepos(url + "/repos", headers)
        events = []
        for repo_url in repos:
            response = requests.get(repo_url + "/events", headers=headers).json()
            if len(response) == 0:
                continue
            for event in response:
                details = {
                    "name":event["repo"]["name"], "type":event["type"],
                    "timestamp":event["created_at"], "url":event["repo"]["url"]
                }
                if event["type"] == "PushEvent":
                    details["commits"] = event["payload"]["size"]
                events.append(details)
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
    
    following = GithubActivity.getUsernames(user_endpoint + "/following")
    print(following)
    print()
    starred = GithubActivity.getFullNames(user_endpoint + "/starred")
    print(starred)
    print()
    watching = GithubActivity.getFullNames(user_endpoint + "/subscriptions")
    print(watching)
    print()
    events = GithubActivity.getBasicEvents(user_endpoint)
    print(events)
    print()
    events = GithubActivity.getDetailedEvents(user_endpoint, token)
    print(events)
    print()


if __name__ == "__main__":
    print()

    message = (
        f"{"="*WIDTH}\n"
        "\n[!] API rate limit exceeded.\n"
        "\tTry again later.\n\n"
        f"{"="*WIDTH}"
    )
    # try:
    main()
    # except TypeError:
    #     print(message)

    print()