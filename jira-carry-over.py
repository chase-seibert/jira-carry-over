import argparse
from collections import defaultdict
from datetime import datetime

import colorama
import lib_jira
import settings


def kwargs_or_default(setting_value):
    if setting_value:
        return dict(default=setting_value)
    return dict(required=True)


def auth(args):
    lib_jira.test_auth(
        server=args.server,
        username=args.username,
        password=args.password)
    lib_jira.save_credentials()


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def report(args):
    issues_per_assignee = defaultdict(set)
    issues_carried_over_per_assignee = defaultdict(set)
    total_issues, total_points = 0, 0
    sprints = lib_jira.get_sprints(args.board, args.since)
    # TODO filter out sprints by date
    for sprint in sprints:
        for issue in lib_jira.get_issues(sprint.id):
            issue_sprints = getattr(issue.fields, settings.JIRA_CUSTOM_FIELD_SPRINT)
            if not issue.fields.assignee:
                continue
            issues_per_assignee[issue.fields.assignee.name].add(issue)
            if len(issue_sprints) >= 2:
                issues_carried_over_per_assignee[issue.fields.assignee.name].add(issue)
            total_issues += 1
    for name, issues in issues_per_assignee.items():
        carrier_over = issues_carried_over_per_assignee.get(name, [])
        points = sum([getattr(i.fields, settings.JIRA_CUSTOM_FIELD_STORY_POINTS) for i in issues])
        total_points += points
        print '%s%s: completed %s stories for %s points, carried over %s/%s' % (
            colorama.Fore.CYAN,
            name,
            len(issues),
            points,
            len(carrier_over),
            len(issues))
        for issue in carrier_over:
            print '   %s/browse/%s' % (settings.JIRA_BASE_URL, issue.key)
        print ''
    print '%s=== Totals ===' % (colorama.Fore.CYAN)
    print 'Sprints: %s' % ', '.join([s.name for s in sprints])
    print 'Completed stories: %s' % total_issues
    print 'Carried over stories: %s' % sum(len(issues) for issues in issues_carried_over_per_assignee.values())
    print 'Story points: %s' % int(total_points)
    print 'Points per sprint: %s' % int(total_points / len(sprints))


if __name__ == '__main__':
    colorama.init(autoreset=True)

    parser = argparse.ArgumentParser(prog='jira-carry-over')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_auth = subparsers.add_parser('auth', help='Authenticate to JIRA')
    parser_auth.add_argument('--server', help='JIRA Server URL',
        **kwargs_or_default(settings.JIRA_BASE_URL))
    parser_auth.add_argument('--username', help='JIRA username',
        **kwargs_or_default(settings.JIRA_USERNAME))
    parser_auth.add_argument('--password', help='JIRA password',
        **kwargs_or_default(settings.JIRA_PASSWORD))
    parser_auth.set_defaults(func=auth)

    parser_report = subparsers.add_parser('report', help='Report per user')
    parser_report.add_argument('--board', help='JIRA Board ID',
        **kwargs_or_default(settings.JIRA_BOARD_ID))
    parser_report.add_argument('--since', help='Date in YYYY-MM-DD', type=valid_date)
    parser_report.set_defaults(func=report)

    args = parser.parse_args()
    args.func(args)
