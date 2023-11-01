from json import load, dump
from os import makedirs, listdir
from os.path import exists, join
from shutil import rmtree
from zipfile import ZipFile

from wget import download

REBALANCE_RANGE = [
    75,
    50,
    25
]


def _download_data():
    with open('metadata.json', 'r', encoding='UTF-8') as metadata_file:
        metadata = load(metadata_file)
    download(metadata['downloadUrl'], 'tac.jar')


def _extract_data():
    if not exists('data/tac/guns'):
        makedirs('data/tac/guns')
    with ZipFile('tac.jar', 'r') as tac_file:
        for file_info in tac_file.infolist():
            if file_info.filename.startswith('data/tac/guns/'):
                tac_file.extract(file_info)


def _clear_data():
    if exists('data/tac/guns'):
        rmtree('data/tac/guns')


def _pack_data(
        pack_name: str
):
    with ZipFile(join('dist', pack_name), 'w') as pack_file:
        pack_file.write('pack.mcmeta', 'pack.mcmeta')
        pack_file.write('pack.png', 'pack.png')
        data_list = listdir('data/tac/guns')
        for data_file_name in data_list:
            pack_file.write(join('data/tac/guns', data_file_name), join('data/tac/guns', data_file_name))


def _data_rebalance(
        percentage: int
):
    data_list = listdir('data/tac/guns')
    for data_file_name in data_list:
        with open(join('data/tac/guns', data_file_name), 'r', encoding='UTF-8') as data_file:
            data_json = load(data_file)
        data_json['projectile']['damage'] = round(float(data_json['projectile']['damage']) * (percentage / 100.0))
        with open(join('data/tac/guns', data_file_name), 'w', encoding='UTF-8') as data_file:
            dump(data_json, data_file, ensure_ascii=False, indent=4)


def data_process():
    _download_data()
    if not exists('dist'):
        makedirs('dist')
    for rebalance_param in REBALANCE_RANGE:
        _extract_data()
        _data_rebalance(rebalance_param)
        with open('metadata.json', 'r', encoding='UTF-8') as metadata_file:
            metadata = load(metadata_file)
        _pack_data(f'{metadata["displayName"].lower().strip().replace(' ', '_')}_rebalanced_{str(rebalance_param)}.zip')
        _clear_data()
