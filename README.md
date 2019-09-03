# GitLeaks

## Info

Gitleaks is a tool used to extract sensitive data from public git repo.

Sensitive Data:

- Subdomains
- Credentials
- AWS Keys
- Email IDs

## Approach

- Search the organization on this <code> <https://github.com/search?q="$ORGANIZATION"> </code>
- Parse response to filter unique repositories.
  - Create a hash of all repositories with data as :

```json
{
    0 : {
            "name": "REPO-NAME",
            "link": "REPO-LINK",
            "starts": "STARS",
            "language": "LANGUAGE",
            "commits": "REPO-COMMIT",
            "last-update": "LAST-COMMIT"
        }
}
```

- Visit each repositories and traverse through all folder and generate all raw link. (Imp: Raw link are in format of "$REPO-LINK/raw/master") OR use a github scraper tool.
  - Example of raw link of a code (<https://$REPO-LINK/raw/master/$FOLDER-NAME/$FILE-NAME>)

```json
{
    0: {
        "file-name": "FILE-NAME",
        "raw-link": "RAW-LINK"
    }
}
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

## Issues

- Too many request (status-code : 429)

```bash
Request URL: https://github.com/search?q=gitrob&type=Repositories
Request Method: GET
Status Code: 429 Too Many Requests
Remote Address: 13.234.210.38:443
Referrer Policy: no-referrer-when-downgrade
```

- Need to authenticate to search code(specifically)

## [Limitations](https://help.github.com/en/articles/searching-code)

- You must be signed in to search for code across all public repositories.
- Only the default branch is indexed for code search. In most cases, this will be the master branch.
- Only files smaller than 384 KB are searchable.
- Only repositories with fewer than 500,000 files are searchable.
- Users who are signed in can search all public repositories.

## Pagination Issues

[Pagination Documentation](https://developer.github.com/v3/#pagination)
- Github paginate an api result when the return data is vast(> 100)
- It return multiple items with sending the link for next page of pagination
- We can traverse through the link to get all results using this [approach](https://developer.github.com/v3/guides/traversing-with-pagination/)

## TODO

- Get code data without authentication
  - Search for repo instead of code
  - Create a temprory user(can use protonmail which does need any personal data to create.)
  - Dig deeper in commits, issues and forked pull requests.

## Behavior

- Without Sleep

```json
[  
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   }
]
```

- With Sleep

```json
[  
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':429
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=go',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godigit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   },
   {  
      'url':'https://github.com/search?q=godisit',
      'status':200
   }
]
```
