# First the flatten_json package needs to be installed.
import re
from csv import writer
from json import load
from os import listdir

import pandas as pd
from flatten_json import flatten

# Read files with university data.
lists = listdir("/Users/jesusllanogarcia/Desktop/Projecto/Scival")
data = [[] for i in range(len(lists))]
for i in range(len(lists)):
    with open("/Users/jesusllanogarcia/Desktop/Projecto/Scival/%s" % lists[i], "r") as read_file:
        data[i] = load(read_file)

# Create a file in which to save the processed data.
universities_csv = open('/Users/jesusllanogarcia/Desktop/Projecto/universities_data.csv', 'w')
csvwriter = writer(universities_csv)

# Transform the json into a flat arrange (dic_flattened) so it can be easily transformed into a dataframe (df).
dic_flattened = (flatten(d) for d in data)

df = pd.DataFrame(dic_flattened)

df = df.drop(['uri'], axis=1)

# save the headers in a variable as a list.
names = list(df.columns)
names2 = list(names)

# obtain the type of metric that correspond with each column and save it (new).
new = []
for i in range(11):
    for j in range(len(names)):
        if 'metrics_%d_metricType' % i in names[j]:
            new.append(df.at[0, names[j]])

# Change the names so they include the metric.
count = 0
for name in new:
    print('{%i:' % count + str(name) + '}')
    count += 1
for i in range(11):
    for j in range(len(names)):
        if 'metrics_%d_' % i in names[j]:
            names[j] = names[j].replace('metrics_%d_' % i, new[i] + '_')

# Rename the colums of the table accordingly to the type of Metric.
for i in range(len(names)):
    df = df.rename(columns={names2[i]: names[i]})

for name in new:
    df = df.drop(['{}_metricType'.format(name)], axis=1)

names = list(df.columns)
names2 = list(names)

for name in new:
    for j in range(4, len(names)):
        if '{}_values_'.format(name) in names[j] and not 'ByYear' in names[j]:
            print('names:', names[j])
            value = df.at[0, names[j]]
            value = str(value)
            value = value.replace(' ', '')
            print(value)
        if '{}_values_'.format(name) in names[j]:
            names[j] = re.sub(r'values_.', str(value), names[j])

print(names)

for i in range(len(names)):
    df = df.rename(columns={names2[i]: names[i]})

collabtypes = df.filter(regex='_collabType$')
collabtypes = collabtypes.vexalues
print(collabtypes[1])
df = df[df.columns.drop(list(df.filter(regex='_collabType$')))]
df = df[df.columns.drop(list(df.filter(regex='_threshold')))]
df = df[df.columns.drop(list(df.filter(regex='_2009')))]
dr = df[df.columns.drop(list(df.filter(regex='_impactType')))]

for i in range(10, 14):
    df = df[df.columns.drop(list(df.filter(regex='_20{}'.format(i))))]

df.to_csv('/Users/jesusllanogarcia/Desktop/Projecto/universities_data-uri2.csv')
