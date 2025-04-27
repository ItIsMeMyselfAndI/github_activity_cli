# How It Works
Fetch the recent activity of the specified GitHub user using the GitHub API.

# Usage
Provide the GitHub username as an argument when running the CLI.

Basic report:
```powershell
github-activity <username>
```
Detailed report:
```powershell
github-activity <username> <token>
```

# Sample Basic Output
```powershell
====================================================================
                        Recent Activities      
====================================================================

- Followed ItIsMeMyselfAndI/github_activity_cli
- Pushed new commit(s) to "ItIsMeMyselfAndI/github_activity_cli"
- Created new repository "ItIsMeMyselfAndI/github_activity_cli" 
- Changed visibility to public in "ItIsMeMyselfAndI/github_activity_cli"
- Opened a new issue in "ItIsMeMyselfAndI/github_activity_cli"
- Starred "ItIsMeMyselfAndI/github_activity_cli"
- ...

====================================================================
```

# Sample Detailed Output
```powershell
====================================================================
                        Recent Activities      
====================================================================

- Followed ItIsMeMyselfAndI/github_activity_cli
- Pushed 3 commit(s) to "ItIsMeMyselfAndI/github_activity_cli"
    at 2025-04-15T16:41:24Z
- Created new repository "ItIsMeMyselfAndI/github_activity_cli" 
    at 2025-04-15T16:41:24Z
- Changed visibility to public in "ItIsMeMyselfAndI/github_activity_cli"
    at 2025-04-15T16:41:24Z
- Opened a new issue in "ItIsMeMyselfAndI/github_activity_cli"
    at 2025-04-15T16:41:24Z
- Starred "ItIsMeMyselfAndI/github_activity_cli"
- ...

====================================================================
```

# Project URL
```powershell
https://roadmap.sh/projects/github-user-activity
```