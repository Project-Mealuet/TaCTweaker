from json import dump, load
from re import fullmatch

from _curseforge_api import get_mod_files

PACK_FORMAT_MAP = {
    '1.16.5': 6,
    '1.18.2': 8
}


def update(
        api_key: str
):
    api_response = get_mod_files('491264', api_key)
    if api_response:
        latest_file_metadata = api_response['data'][0]
        with open('files_list.json', 'r', encoding='UTF-8') as mod_list_file:
            mod_list = load(mod_list_file)
        if str(latest_file_metadata['id']) in mod_list:
            return False
        mod_list.append(str(latest_file_metadata['id']))
        for version in latest_file_metadata['gameVersions']:
            if fullmatch(r'1\.[1-9]{1,2}\.?[1-9]{0,2}', version):
                with open('pack.mcmeta', 'w', encoding='UTF-8') as pack_mcmeta:
                    dump(
                        {
                            'pack': {
                                'description': 'TaC guns re-balanced for Mealuet Server.',
                                'pack_format': PACK_FORMAT_MAP[version]
                            }
                        },
                        pack_mcmeta,
                        ensure_ascii=False,
                        indent=4
                    )
                break
        metadata = {
            'id': latest_file_metadata['id'],
            'displayName': latest_file_metadata['displayName'],
            'downloadUrl': latest_file_metadata['downloadUrl']
        }
        with open('metadata.json', 'w', encoding='UTF-8') as metadata_file:
            dump(metadata, metadata_file, ensure_ascii=False)
        with open('files_list.json', 'w', encoding='UTF-8') as mod_list_file:
            dump(mod_list, mod_list_file, ensure_ascii=False, indent=4)
        return True
    else:
        return False
