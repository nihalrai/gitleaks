import os
import json
import subprocess
import hashlib
import traceback

# Threads count required to clone repositories
thread_count = 5


def run_command(command):
    
    try:
        cmd    = subprocess.Popen(command,
                                  shell=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  executable='C:\\Program Files\\Git\\bin\\bash')
        output = cmd.communicate()
        
        if cmd.returncode != 0 or output[1]:
            return False
        
        return output[0].strip("\n")
    
    except Exception as e:
        print str(e)
        traceback.print_exc()
        return False


def mkdir(file_name):
    
    path = os.path.join("/tmp", hashlib.sha1(file_name).hexdigest())
    
    if os.path.exists(path):
        return path
    
    run_command("mkdir %s" % path)
    
    if not os.path.exists(path):
        return False
    
    return path


# def git_grep(repo_data):
#
#     # Grep output to return
#     output = {}
#     # List of repo_path
#     repo_path = []
#
#     for data in repo_data:
#         if data.has_key("cloned-path"):
#             repo_path.append(data["cloned-path"])
#
#     # https://github.com/dxa4481/truffleHog/blob/dev/scripts/searchOrg.py#L10
#     search = {
#         "regex": {
#             "subdomain": r"/^[a-zA-Z0-9][a-zA-Z0-9.-]+[a-zA-Z0-9]$/",
#             "slack-token": r"(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
#             "aws-keys": r"AKIA[0-9A-Z]{16}",
#             "email-id": r"\S+@\S+"
#         },
#         "patterns": [
#             "password",
#             "credentials",
#             "username",
#             "*.api.*",
#             "*.key.*",
#             "token"
#         ]
#     }
#
#     for key, value in search["regex"].items():
#         match = []
#         for data in repo_data:
#             repo_path = data["cloned-path"]
#             result = run_command("%s -C %s grep -i %s" % (GIT_PATH, repo_path, value))
#             if result:
#                 match.append(result)
#         if len(match) > 0:
#             output[key] = match
#
#     match = []
#     for value in search["patterns"]:
#         for data in repo_data:
#             repo_path = data["cloned-path"]
#             result = run_command("%s -C %s grep -i -e %s" % (GIT_PATH, repo_path, value))
#             if result and type(result) == dict:
#                 match.append(result)
#     output["patterns-match"] = match
#
#     return output
