from json import load
from os import system, listdir
from os.path import join
from time import localtime

from requests import post
from requests.exceptions import RequestException


def _commit_files_list(
        github_token: str
):
    system('git config user.name "Build Bot"')
    system('git config user.email "bot@mealuet.com"')
    system('git add files_list.json')
    with open('metadata.json', 'r', encoding='UTF-8') as metadata_file:
        metadata = load(metadata_file)
    system(f'git commit -m "TaC updated - ID{metadata['id']}"')
    system(f'git push https://{github_token}@github.com/kressety/TaCGunsRebalance.git')


def _post_to_github(
        route: str,
        github_token: str,
        params: dict = None,
        headers_add: dict = None,
        data=None,
        base_name: str = 'api.github.com'
):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {github_token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    if headers_add:
        for key in headers_add:
            headers[key] = headers_add[key]
    try:
        response = post(
            url=f'https://{base_name}{route}',
            headers=headers,
            json=params,
            data=data
        )
        if response.status_code == 201:
            return response.json()
        else:
            return False
    except RequestException:
        return False


def _post_release(
        github_token: str
):
    assets_names = listdir('dist')
    with open('metadata.json', 'r', encoding='UTF-8') as metadata_file:
        metadata = load(metadata_file)
    time_now = localtime()
    release_create = _post_to_github(
        route='/repos/kressety/TaCGunsRebalance/releases',
        github_token=github_token,
        params={
            'tag_name': f'ID{metadata["id"]}',
            'target_commitish': 'main',
            'name': metadata['displayName'],
            'body': f'Built at {time_now.tm_year}-{time_now.tm_mon}-{time_now.tm_mday} '
                    f'{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}',
            'draft': False,
            'prerelease': False,
            'generate_release_notes': True
        }
    )
    if release_create is not False:
        for asset_name in assets_names:
            with open(join('dist', asset_name), 'rb') as asset_file:
                _post_to_github(
                    route=f'/repos/kressety/TaCGunsRebalance/releases/{release_create["id"]}/assets?name={asset_name}',
                    github_token=github_token,
                    headers_add={
                        'Content-Type': 'application/octet-stream'
                    },
                    data=asset_file,
                    base_name='uploads.github.com'
                )


def github_release(
        github_token: str
):
    _commit_files_list(github_token)
    _post_release(github_token)
