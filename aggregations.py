import csv
import pandas as pd

data = pd.read_csv("apartments.tsv", sep="\t")

groups = data.groupby("location")
#number of announcements per location for all announ whether it has a price or not
print(groups.agg(num_of_announcements=("title", "count")))

#to compute avg price per location we need to
#1. filter out announcements that don't have the price
#2. convert the price column to int
data_with_price = data[data["price"]!="Contattal'utente"]
data_with_price["price"] = pd.to_numeric(data_with_price["price"])
groups = data_with_price.groupby("location")

#number of announcments (with price) per location and avg price
print(groups.agg(num_of_announcements=("title", "count"), avg_price=("price", "mean")))

