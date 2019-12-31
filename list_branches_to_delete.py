from datetime import datetime, timedelta
import requests
import sys
import json
import csv

NOW = datetime.utcnow()
MONTHS_BEFORE_STALE = 3
OUTFILENAME_TEMPLATE = "branches_to_delete_repo{}_{}.csv"


def list_branches_to_delete(domain, repo_id, access_token, whitelist_filename):
    candidates = []
    page = 1

    # Read whitelist
    whitelist = []
    if whitelist_filename is not None:
        with open(whitelist_filename, 'r') as f:
            lines = f.readlines()
            whitelist = [line.rstrip('\n') for line in lines]
        print("Read {} whitelisted branches from file {}".format(
            len(whitelist), whitelist_filename))
    else:
        print("No whitelist file was provided")

    while True:
        # Get branches from GitLab repository
        url = "{}/api/v4/projects/{}/repository/branches?page={}".format(
            domain, repo_id, page)
        response = requests.get(url, headers={"PRIVATE-TOKEN": access_token})
        if response.status_code != 200:
            print("Error getting branches from GitLab for page {}: {}".format(
                page, response))
            break
        branches = response.json()
        print("Found {} branches on page {}".format(len(branches), page))
        if len(branches) == 0:
            break
        page += 1

        # Find candidate branches to delete based on criteria
        for branch in branches:
            if is_branch_to_delete(branch, whitelist):
                candidates.append(get_candidate_row(repo_id, branch))

    # Write filtered list to file
    outfilename = OUTFILENAME_TEMPLATE.format(
        repo_id, NOW.strftime('%Y%m%d%H%M%S%f'))
    print("Found {} branches to delete".format(len(candidates)))
    print("Writing list to file {}".format(outfilename))
    with open(outfilename, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(
            ["repo_id", "branch_name", "author_name", "branch_info"])
        for candidate in candidates:
            csv_writer.writerow(candidate)


def is_branch_to_delete(branch, whitelist):
    return is_stale_branch(branch) \
        and not is_protected(branch) \
        and not is_default(branch) \
        and not is_whitelisted(branch, whitelist)


def is_stale_branch(branch):
    return datetime.strptime(branch["commit"]["committed_date"], "%Y-%m-%dT%H:%M:%S.000+00:00") + timedelta(days=MONTHS_BEFORE_STALE/12*365) < NOW


def is_protected(branch):
    return bool(branch["protected"])


def is_default(branch):
    return bool(branch["default"])


def is_whitelisted(branch, whitelist):
    return branch["name"] in whitelist


def get_candidate_row(repo_id, branch):
    return [repo_id, branch["name"], branch["commit"]["author_name"], branch]


if __name__ == "__main__":
    domain = sys.argv[1]
    repo_id = sys.argv[2]
    access_token = sys.argv[3]
    whitelist_filename = sys.argv[4] if len(sys.argv) == 5 else None
    now = datetime.utcnow()
    list_branches_to_delete(
        domain, repo_id, access_token, whitelist_filename)
