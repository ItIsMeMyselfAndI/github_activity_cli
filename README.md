# Usage
Provide the GitHub username as an argument when running the CLI.

Detailed report:
```powershell
github-activity <username>
```
Summarized report:
```powershell
github-activity summary <username> 
```

# How It Works
Fetch the recent activity of the specified GitHub user using the GitHub API.

# Sample Detailed Output
```powershell
====================================================================
                        Recent Activities      
====================================================================

- Pushed new commit to ItIsMeMyselfAndI/github_activity_cli
    at 13:09:04 (Apr 21, 2025)
- Pushed new commit to ItIsMeMyselfAndI/github_activity_cli
    at 09:14:56 (Apr 15, 2025)
- Created ItIsMeMyselfAndI/github_activity_cli
    at 09:14:56 (Apr 15, 2025)
- Starred ItIsMeMyselfAndI/github_activity_cli
- Followed ItIsMeMyselfAndI/github_activity_cli
- Opened a new issue in ItIsMeMyselfAndI/github_activity_cli
    at 23:48:22 (Mar 30, 2025)
- ...

====================================================================
```

# Sample Summarized Output
```powershell
====================================================================
                        Recent Activities      
====================================================================

- Pushed 3 commits to ItIsMeMyselfAndI/github_activity_cli
- Created 3 repositories 
- Opened a new issue in ItIsMeMyselfAndI/github_activity_cli
- Starred ItIsMeMyselfAndI/github_activity_cli
- ...

====================================================================
```

# Project URL
```powershell
https://roadmap.sh/projects/github-user-activity
```