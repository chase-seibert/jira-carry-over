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
