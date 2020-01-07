# GitLab Branch API Wrapper
Made a wrapper around the [GitLab Branches API](https://docs.gitlab.com/ee/api/branches.html) for cleaning up branches, and committed the wrapper here on GitHub. 

DAS RITE FITE MI

## List branches to delete
```
python3 list_branches_to_delete.py <domain> <repo_id> <access_token> <whitelist_filename>
```
* `domain`: e.g. https://gitlab.com
* `repo_id`: Check in your repo main page, under the name of the repository. Should be a number.
* `access_token`: Refer to the GitLab [docs](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) for how to generate this token.
* `whitelist_filename`: Name of a .txt file, where each new line has a branch name.

Branches that fulfill the following conditions will be listed:
* Last committed 3 months or more ago
* **AND** Not protected
* **AND** Not default
* **AND** Not in provided whitelist

An output file with name format `branches_to_delete_repo<repo_id>_<timestamp>.csv` will be produced. This file will contain all branches to be deleted according to the criteria above.

## Delete branches
> Please proceed with caution! Don't delete your master branch!

```
python3 delete_branches.py <repo_domain_map_filename> <delete_list_filename>
```
* `repo_domain_map_filename`: JSON mapping of repo_id to its domain and access token. Should follow this format:
  ```
  {
    "repo_id_1": {
        "access_token": "some token",
        "domain": "https://gitlab.com"
    },
    "repo_id_2": {
        "access_token": "some token",
        "domain": "https://gitlab.com"
    }
  }
  ```
* `delete_list_filename`: CSV file, where each row represents a branch to delete. Headers should be as such: 
  ```
  repo_id,branch_name,author_name
  ```