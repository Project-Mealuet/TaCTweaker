from os import environ

from _data_process import data_process
from _github_api import github_release
from _update import update

if __name__ == '__main__':
    github_token = environ['GH_TOKEN']
    curseforge_api_key = environ['CURSEFORGE_API_KEY']

    if update(curseforge_api_key):
        data_process()
        github_release(github_token)
