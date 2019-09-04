## Approach

- Search the organization on this <code> <https://github.com/search?q="$ORGANIZATION"> </code>
- Parse response to filter unique repositories.
  - Create a hash of all repositories with data as :

```json
[
    {
        "name": "REPO-NAME",
        "link": "REPO-LINK",
        "starts": "STARS",
        "language": "LANGUAGE",
        "commits": "REPO-COMMIT",
        "last-update": "LAST-COMMIT"
    }
]
```

- Visit each repositories and traverse through all folder and generate all raw link. (Imp: Raw link are in format of "$REPO-LINK/raw/master") OR use a github scraper tool.

- Example of raw link of a code (<https://$REPO-LINK/raw/master/$FOLDER-NAME/$FILE-NAME>)

```json
[
    {
        "file-name": "FILE-NAME",
        "raw-link": "RAW-LINK"
    }
]
```

- Parse each raw data to extract for sensitve data and put it in hash.

```json
{
    "data": {
        "name": "NAME",
        "value": "VALUE",
        "source": "SOURCE"
    }
}
```