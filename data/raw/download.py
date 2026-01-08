import pandas as pd
import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi


api = KaggleApi()
api.authenticate()


api.dataset_download_files(
    'karkavelrajaj/amazon-sales-dataset',
    path='.',
    unzip=True
)




df = pd.read_csv("amazon.csv")
print(df.head(5))



df.to_csv("../raw/amazon.csv", index=False)

