# jira-carry-over - Report on JIRA stories carried over sprint to sprint

## Quickstart

```bash
virtualenv .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
python jira-carry-over.py --help
```

### Authenticate to JIRA

Even if you use single sign on to authenticate to JIRA normally, you also have
a regular username and password. You can set it by going to
`Profile -> Change Password`. Once you have your password, you can authenticate
on the command-line.

```bash
>python jira-carry-over.py auth --server https://my-jira-host --username my-username@my-domain.com --password my-password
Successfully connected to: https://my-jira-host
Version: 7.8.0
Connected as: Your Name
Wrote credentials to ~/.jirarc
```

If successful, the credentials will be cached in `~/.jirarc` so that you don't
need to provide them again.


#### Query for Issues Carried Over

You can get your board ID from the 'RapidView' ID present in JIRA sprint board urls.

```bash
python jira-carry-over.py report --board 446 --since 2019-01-01
```

Example output:

```bash
user1@example.com: completed 1 stories for 3.0 points, carried over 0/1

user2@example.com: completed 5 stories for 8.0 points, carried over 0/5

user3@example.com: completed 7 stories for 12.5 points, carried over 0/7

user4@example.com: completed 15 stories for 18.5 points, carried over 0/15

user5@example.com: completed 13 stories for 20.0 points, carried over 1/13
   https://jira.corp.example.com/browse/MYPROJ-479

user6@example.com: completed 1 stories for 0.0 points, carried over 1/1
   https://jira.corp.example.com/browse/MYPROJ-440

user7@example.com: completed 7 stories for 14.0 points, carried over 0/7

user8@example.com: completed 2 stories for 3.0 points, carried over 1/2
   https://jira.corp.example.com/browse/MYPROJ-422

user9@example.com: completed 12 stories for 21.5 points, carried over 4/12
   https://jira.corp.example.com/browse/MYPROJ-443
   https://jira.corp.example.com/browse/MYPROJ-443
   https://jira.corp.example.com/browse/MYPROJ-65
   https://jira.corp.example.com/browse/MYPROJ-65

 === Totals ===
 Sprints: Sprint1, Sprint2, Sprint3, Sprint4
 Completed stories: 63
 Carried over stories: 7
 Story points: 100
 Points per sprint: 25
```

## Settings

You can create a `settings_override.py` file, and populate the following
settings:

### JIRA_BASE_URL, JIRA_USERNAME, JIRA_PASSWORD

The URL of your JIRA instance. This can be used instead of using `auth`
and creating a `~/.jirarc` file.

```python
JIRA_BASE_URL = 'https://my-jira-host'
JIRA_USERNAME = 'my-username@my-domain.com'
JIRA_PASSWORD = 'my-password'
```

### JIRA_BOARD_ID

The JIRA sprint board ID, from the sprint board URL 'RapidView' argument.

```python
JIRA_BOARD_ID = 1234
```

### JIRA_CUSTOM_FIELD_SPRINT

The JIRA field that stores the sprint value for an issue.

```python
JIRA_CUSTOM_FIELD_SPRINT = 'customfield_10004'
```

### JIRA_STORY_POINTS_FIELD

The JIRA field that stores the story point value for an issue.

```python
JIRA_STORY_POINTS_FIELD = 'customfield_10006'
```
