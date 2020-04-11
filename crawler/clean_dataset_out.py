import csv
import string
from bencoder import bdecode
from os import listdir

base_dir = "/home/nas/tordata/"
keys = ["series", "movies"]
output_file_name = "torrent_meta_dataset.csv"


def prepare_metadata_string(torrent):
    info = torrent.get('info')
    if info and info.get('pieces'):
        del torrent['info']['pieces']
    return str(info).replace('.', ' ').translate(str.maketrans('', '', string.punctuation))


def read_torrent_from_filepath(path):
    f = open(path, 'rb')
    content = None
    try:
        f_cont = f.read()
        content = bdecode(f_cont)
    finally:
        f.close()
    return content

# based on https://stackoverflow.com/questions/33137741/fastest-way-to-convert-a-dicts-keys-values-from-bytes-to-str-in-python3
def bytes_values_to_str(data):
    if isinstance(data, bytes):
        return data.decode('utf-8', 'ignore')
    if isinstance(data, dict):
        return dict(map(bytes_values_to_str, data.items()))
    if isinstance(data, (tuple, list)):
        return list(map(bytes_values_to_str, data))
    return data


def main():
    with open(base_dir+output_file_name, 'w', encoding='utf-8') as out_f:
        csv_writer = csv.writer(out_f)
        for k in keys:
            dir_content = listdir(base_dir+k)
            for f in dir_content:
                tor_info = bytes_values_to_str(
                    read_torrent_from_filepath(base_dir+k+"/"+f))
                if tor_info:
                    clean_str = prepare_metadata_string(tor_info)
                    # included soundtracks link while crawling to collect dataset 
                    # that wasn't intended
                    # dirty fix:
                    if clean_str.strip() \
                    and not ' ost ' in clean_str \
                    and not ' OST ' in clean_str \
                    and not 'oundtrack' in clean_str \
                    and not 'SOUNDTRACK' in clean_str:
                        csv_writer.writerow([k, clean_str])

if __name__ == '__main__':
    main()