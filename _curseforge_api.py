from requests import get
from requests.exceptions import RequestException


def _get_from_curseforge(
        route: str,
        api_key: str
):
    try:
        response = get(
            url=f'https://api.curseforge.com{route}',
            headers={
                'Accept': 'application/json',
                'x-api-key': api_key
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            return False
    except RequestException:
        return False


def get_mod_files(
        mod_id: str,
        api_key: str
):
    return _get_from_curseforge(
        f'/v1/mods/{mod_id}/files',
        api_key
    )
