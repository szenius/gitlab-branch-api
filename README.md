# GitLab Branch API Wrapper

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