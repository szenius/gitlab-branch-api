import sys
import csv
import requests
import json
import urllib

def delete_branches(repo_domain_map_filename, delete_list_filename):
    # Read repo-domain mapping JSON file
    repo_domain_map = {}
    with open(repo_domain_map_filename, 'r') as f:
        repo_domain_map = json.load(f)

    # Read delete list CSV file
    with open(delete_list_filename, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            # Delete branch
            url = "{}/api/v4/projects/{}/repository/branches/{}".format(repo_domain_map[row["repo_id"]]["domain"], row["repo_id"], row["branch_name"].replace("/", "%2F"))
            response = requests.delete(url, headers={"PRIVATE-TOKEN": repo_domain_map[row["repo_id"]]["access_token"]})

            if response.status_code != 204:
                print("Failed to delete branch {} authored by {} from repo {}: {}".format(row["branch_name"], row["author_name"], row["repo_id"], response.text))
                continue
            print("Deleted branch {} authored by {} from repo {}".format(row["branch_name"], row["author_name"], row["repo_id"]))


if __name__ == "__main__":
    repo_domain_map_filename = sys.argv[1]
    delete_list_filename = sys.argv[2]
    delete_branches(repo_domain_map_filename, delete_list_filename)
