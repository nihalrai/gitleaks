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
