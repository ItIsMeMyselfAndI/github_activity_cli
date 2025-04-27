import requests
import sys
import os

WIDTH = os.get_terminal_size().columns

class GithubActivity:
    @staticmethod
    def _requestValidResponse(url:str) -> list:
        response = requests.get(url).json()
        try:
            if "Not Found" in response["message"]:
                print(url)
                print(response)
                error = "[!] Invalid username.\n\tCheck username and try again."
            elif "API rate limit" in response["message"]:
                error = "[!] API rate limit exceeded.\n\tWait and try again later."
            else:
                error = "[!] Unexpected error occurred.\n\tTry again."
        except TypeError:
            return response
        message = (
            f"{"="*WIDTH}\n"
            f"\n{error}\n\n"
            f"{"="*WIDTH}\n"
        )
        print(message)
        exit(0)

    @staticmethod
    def getEvents(url:str) -> list:
        response = GithubActivity._requestValidResponse(url)
        events = []
        for event in response:
            details = {
                "repo":event["repo"]["name"], "type":event["type"],
                "timestamp":event["created_at"]
            }
            if event["type"] == "PushEvent":
                details["size"] = event["payload"]["size"]
            elif event["type"] in ["CreateEvent", "DeleteEvent"]:
                details["ref_type"] = event["payload"]["ref_type"]
            elif event["type"] in ["PullRequestEvent", "IssuesEvent", "MemberEvent"]:
                details["action"] = event["payload"]["action"]
            events.append(details)
        return events

    @staticmethod
    def getUsernames(url:str) -> list:
        response = GithubActivity._requestValidResponse(url)
        usernames = [{"type":"following", "username":user["login"]} for user in response]
        return usernames 

    @staticmethod
    def formatActivities(activities:list) -> str:
        f_activities = []
        for activity in activities:
            match activity["type"]:
                case "PushEvent":
                    line = f"- Pushed {activity["size"]} commit(s) in \"{activity["repo"]}\""
                case "PullRequestEvent":
                    line = f"- {activity["action"].title()} a pull request in \"{activity["repo"]}\""
                case "PullRequestReviewEvent":
                    line = f"- Reviewed a pull request in {activity["repo"]}"
                case "PullRequestReviewCommentEvent":
                    line = f"- Commented on a pull request review in \"{activity["repo"]}\""
                case "IssuesEvent":
                    line = f"- {activity["action"].title()} an issue in \"{activity["repo"]}\""
                case "IssueCommentEvent":
                    line = f"- Commented on an issue in \"{activity["repo"]}\""
                case "ForkEvent":
                    line = f"- Forked \"{activity["repo"]}\""
                case "WatchEvent":
                    line = f"- Starred \"{activity["repo"]}\""
                case "CreateEvent":
                    line = f"- Created a new {activity["ref_type"]} \"{activity["repo"]}\""
                case "DeleteEvent":
                    line = f"- Deleted a {activity["ref_type"]} in \"{activity["repo"]}\""
                case "ReleaseEvent":
                    line = f"- Published a new release in \"{activity["repo"]}\""
                case "PublicEvent":
                    line = f"- Changed visibility to public in \"{activity["repo"]}\""
                case "MemberEvent":
                    line = f"- {activity["action"].title()} a member in \"{activity["repo"]}\""
                case "GollumEvent":
                    line = f"- Edited a wiki page in \"{activity["repo"]}\""
                case "following":
                    line = f"- Followed \"{activity["username"]}\""
            if activity["type"] != "following":
                line += f" at {activity["timestamp"]}"
            f_activities.append(line)
        return "\n\n".join(f_activities)

        
def _isValidArgv(argv:list) -> bool:
    message = (
        f"{"="*WIDTH}\n"
        "\n[!] Invalid command.\n"
        "\tCheck README.md file.\n\n"
        f"{"="*WIDTH}"
    )
    if (len(argv) <= 1) or (len(argv) > 2):
        print(message)
        return False
    return True

def main() -> None:
    if not _isValidArgv(sys.argv):
        return

    base_url = f"https://api.github.com"
    username = sys.argv[1]
    user_endpoint = f"{base_url}/users/{username}"

    events = GithubActivity.getEvents(user_endpoint + "/events")
    following = GithubActivity.getUsernames(user_endpoint + "/following")

    activities = events + following
    if len(activities) == 0:
        formatted = "No recent activities as of this moment"
    else:
        formatted = GithubActivity.formatActivities(activities)

    display = (
        f"{"="*WIDTH}\n\n"
        f"{"Recent Activities".center(WIDTH)}\n\n"
        f"{"="*WIDTH}\n\n"
        f"{formatted}\n\n"
        f"{"="*WIDTH}"
    )
    print(display)

if __name__ == "__main__":
    print()
    main()
    print()