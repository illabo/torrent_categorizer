## Torrent categorizer

Jupyter notebook to teach model to tell apart tv-shows and movies by its metadata from torrent file.

- Uses Fastai ULMFiT.
- Notebook was used on Google Colab so Google Drive was connected to store results and offload models. You may need a different way to connect the storage on other services.
- Model `export.pkl` file is in another repository: https://bitbucket.org/illabo/torclassr.


## Crawler: scripts to collect dataset

Please check the paths to store data beforehand! Find `/home/nas/` and replace it with the directory where to store the torrent files. Also manually create subdirectories in that directory or add this step to script.
```
mkdir -p tordata/series tordata/movies
```

- `crawler.py`

Contains scripts to scrape some popular torrent sites to collect magnet links and save 'em into two column csv file. First column is the category ("movies" or "series"). Second column is the magnet link.

- `download_torrent_files.py`

Should be run on the machine same machine with aria2 torrent client in rpc mode. Downloads torrent files by magnet links and stores the files in directories named after category ("movies" or "series"). 

- `clean_dataset_out.py`

Reads torrent metadata from files, cleans it for better learning and stores it in two column csv file. First column is the category ("movies" or "series"). Second column is the the data to learn on.