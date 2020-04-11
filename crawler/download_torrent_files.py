import csv
import json
import requests

def main():
    with open("magnets.csv","r") as file:
        reader = csv.reader(file, delimiter=",")
        for idx, line in enumerate(reader):
            key, magnet = line
            data = json.dumps({
                "jsonrpc":"2.0",
                "method":"aria2.addUri",
                "id":idx,
                "params":[
                    [magnet],
                    {
                        "bt-metadata-only":"true",
                        "bt-save-metadata":"true",
                        "dir":"/home/nas/tordata/%s"%key}
                    ]})
            print(requests.post("http://localhost:6800/jsonrpc", data=data, headers={'Content-type': 'application/json'}).text)

if __name__ == '__main__':
    main()