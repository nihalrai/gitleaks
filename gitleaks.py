import os
import json
import urllib
import requests
import traceback


from utils import run_command, mkdir


class Gitleaks:

    def __init__(self, query, token):
        self.query  = query
        self.token  = token
        
        self.github = Github(self.token)
    
    def run(self):
        print json.dumps(self._search(), indent=4)
    
    def _search(self):
        
        try:
            repos = self._fetch_query_match_repositories()
            
            if not repos:
                return None
            
            return self._clone_it(repos)
            
            # final_output = self.get_output(data, output)

            # if not final_output:
            #     return output
            
            # print final_output["data"]
            # # Search in clone repo to get sensitive data
            # matched = git_grep(final_output["data"])
            # print matched
            # if matched:
            #     final_output["sensitive-info"] = matched
            
            # return final_output
        
        except Exception as e:
            print str(e)
            traceback.print_exc()
    
    # fetch query or keyword found repositories
    def _fetch_query_match_repositories(self):
        
        response = self.github.search_in_code(self.query)
        
        if not response or "items" not in response:
            return {}
        
        repos = []
        items = response["items"]
        
        for item in items:
            
            if "repository" not in item:
                continue
            
            repo = {}
            
            if "name" in item["repository"]:
                repo["name"] = item["repository"]["name"]
            
            if "html_url" in item["repository"]:
                repo["link"] = item["repository"]["html_url"]
            
            if "commits_url" in item["repository"]:
                repo["last_commit"] = self.github.fetch_last_commit_hash(item["repository"]["commits_url"])
            
            print repo
            
            if repo not in repos:
                repos.append(repo)
            
            break
        
        return repos
    
    def _clone_it(self, repositories):
        
        root = mkdir(self.query)
        
        if not root:
            return None
        
        for repository in repositories:
            path = Git().clone(repository, root)
            repository['path'] = path
        
        return repositories
    
    # def get_output(self, data, output):
    #
    #     # Create a unique folder using sha1 hash of self.query
    #     folder = make_folder(self.query)
    #
    #     if not folder:
    #         return False
    #
    #     count, data = clone_repo(data, folder)
    #
    #     # No repositories is cloned
    #     if count == 0:
    #         return False
    #
    #     output["type"] = "success"
    #     output["clone-path"] = folder
    #
    #     output["data"] = data
    #     output["clone-stats"] = "%s of %s are cloned" % (count, len(data))
    #
    #     return output


class Github:
    
    # Github API Endpoint
    API = "https://api.github.com"
    
    def __init__(self, token):
        self.token = token
        
        # authenticate takes up one request count
        self._authenticate()
    
    def _authenticate(self):
        
        response = self._request_url(self.API)
        
        self._is_bad_token(response)\
            ._is_rate_limit_exceeded(response)
    
    def _is_bad_token(self, response):
        
        if response.status_code == 401:
            content = json.loads(response.content)
        
            if 'message' in content\
                    and 'bad credentials' in content.message.lower():
                raise BadTokenException("Invalid token: %s" % self.token, content)
        
        return self
    
    def _is_rate_limit_exceeded(self, response):
        
        if response.status_code == 403:
            content = json.loads(response.content)
            
            if 'message' in content and content.message == 'api rate limit exceeded':
                raise RateLimitExceededException("Rate Limit Exceeded for token: %s" % self.token, content)
        
        return self
    
    def search_in_code(self, query):
        
        url = self._prepare_search_in_code_url(query)
        response = self._request_url(url)
        
        if response.status_code in range(200, 300):
            
            content = json.loads(response.content)
            """
            In case of pagination the header return in response consist of link key
            that usually have keys like last, previous and next
            which further have key named url
            {
                'prev': {
                    'url': 'https://api.github.com/search/code?q=go&page=1',
                    'rel': 'prev'
                },
                'last': {
                    'url': 'https://api.github.com/search/code?q=go&page=34',
                    'rel': 'last'},
                'first': {
                    'url': 'https://api.github.com/search/code?q=go&page=1',
                    'rel': 'first'
                },
                'next': {
                    'url': 'https://api.github.com/search/code?q=go&page=3',
                    'rel': 'next'
                }
            }
            """
            
            if response.links \
                    and 'last' in response.links \
                    and 'url' in response.links['last']:
                
                last_page = response.links['last']['url'].split('=')[-1]
                
                for page in range(2, int(last_page) + 1):
                    try:
                        response = self._request_url(url + "&page=%s" % page)
                        
                        if response.status_code in range(200, 300):
                            content.update(json.loads(response.content))
                    except Exception as e:
                        print str(e)
                        traceback.print_exc()
                        continue
            
            return content
        
        return {}
    
    def _prepare_search_in_code_url(self, query):
        return "%s/search/code?%s" % (self.API,
                                      urllib.urlencode({'q': '%s' % query}))
    
    def _request_url(self, url):
        
        response = requests.get(url,
                                headers=self._get_headers(),
                                allow_redirects=False,
                                timeout=30)
        
        return response
    
    def _get_headers(self):
        
        return {
            "Accept": "application / vnd.github.v3 + json",
            "Authorization": "token %s" % self.token
        }
    
    @staticmethod
    def _is_ok_response(response):
        
        return True if response.status_code in range(200, 300) else False
    
    def fetch_last_commit_hash(self, url):
        
        commit_url  = url.replace("{/sha}", "")
        response    = self._request_url(commit_url)
        commit_sha  = ''
        
        if self._is_ok_response(response):
            content     = json.loads(response.content)
            last_commit = content[0]
            
            # Response of commits_url is a list of details of all commits
            if "sha" in last_commit:
                commit_sha = last_commit["sha"]
        
        return commit_sha


class GithubException(Exception):
    def __init__(self, message, response):
        
        super(GithubException, self).__init__(message)
        self.response = response


class BadTokenException(GithubException):
    pass


class RateLimitExceededException(GithubException):
    pass


class Git:
    
    # Git binary path
    GIT_PATH = "git"
    
    def __init__(self):
        pass
    
    def clone(self, repository, destination):
        
        repository_path  = os.path.join(destination, repository["name"])
        
        clone = run_command("%s clone %s %s" % (self.GIT_PATH,
                                                "%s.git" % repository["link"],
                                                repository_path))
        
        if not clone:
            return FailedToCloneRepositoryException("Failed to clone the repository: %s" % repository['name'])
        
        last_commit = self.get_last_commit_hash(repository_path)
        
        if not last_commit or repository['last_commit'] != last_commit:
            return FailedToCloneRepositoryException("Last commit doesn't match: Repository (%s) != Cloned (%s)"
                                                    % (repository['last_commit'],
                                                       last_commit))
        
        return repository_path
    
    def get_last_commit_hash(self, repository_path):
        
        if not os.path.exists(repository_path):
            return None
        
        last_commit = run_command("%s -C %s rev-parse HEAD" % (self.GIT_PATH, repository_path))
        
        # run_command method returns bool type if failed
        last_commit = last_commit.strip("\n") if type(last_commit) == str else ""
        
        # Hash of last commit and detected commit will be equate to avoid same commit
        if not last_commit:
            return None
        
        # HEAD means the repo is either not completely cloned or the git tree is not correct
        if last_commit == "HEAD":
            return None
        
        return last_commit


class FailedToCloneRepositoryException(Exception):
    pass
