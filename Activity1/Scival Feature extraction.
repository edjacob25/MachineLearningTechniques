from json import load
from csv import writer
from os import listdir
import pandas as pd
import numpy as np
from flatten_json import flatten
import re

metrics = {0: 'ScholarlyOutput', 1: 'CitedPublications', 2: 'AcademicCorporateCollaboration',
           3: 'AcademicCorporateCollaborationImpact', 4: 'Collaboration', 5: 'CitationCount',
           6: 'CitationsPerPublication', 7: 'CollaborationImpact', 8: 'FieldWeightedCitationImpact',
           9: 'PublicationsInTopJournalPercentiles', 10: 'OutputsInTopCitationPercentiles'}

Academiccollabtypes = {0: 'Academic-corporatecollaboration', 1: 'Noacademic-corporatecollaboration'}

Collabtypes = {0: 'Institutionalcollaboration', 1: 'Internationalcollaboration', 2: 'Nationalcollaboration', 3: 'Singleauthorship',}

thresholds = [1, 5, 10, 25]



data = pd.read_csv('/Users/jesusllanogarcia/Desktop/Projecto/universities_data-uri2.csv').iloc[:, 1:]

#Split data into data with values per year and data with percentages by year.
d = []
for i in range(11):
    d1 = data.filter(regex='^{}'.format(metrics[i]))
    d.append(d1.filter(regex='valueByYear'))

p = []
for i in range(11):
    d1 = data.filter(regex='^{}'.format(metrics[i]))
    d1 = d1.filter(regex='percentageByYear')
    print(d1.empty)
    if not d1.empty:
        p.append(d1.filter(regex='percentageByYear'))

print(d)

for i in range(len(p)):
    print("p: ",p[i].columns)

#Overall calculation for data by year.
overall = []
for i in range(11):
    if not(i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        overall.append(d[i].mean(axis=1))
    else:
        overall.append(0)
print("overall:", overall)

#Overall calculation for data by year according to percetange threshold.
overallthres = []
for i in range(9,11):
    for threshold in thresholds:
        d9 = d[i].filter(regex='_{}_'.format(threshold))
        overallthres.append(d9.mean(axis=1))

print('overallthres: ', overallthres)

#Overall calculation for data by year according to type of academic collaboration.
overallAcadCollab = []
for i in range(2,4):
    for j in range(2):
        d9 = d[i].filter(regex='{}_{}_'.format(metrics[i],Academiccollabtypes[j]))
        print("D9:", d9)
        overallAcadCollab.append(d9.mean(axis=1))

print("overallACollab: ", overallAcadCollab)

#Overall calculation for data by year according to type of collaboration.
overallCollab = []
for j in range(4):
    d4 = d[4].filter(regex='Collaboration_{}_'.format(Collabtypes[j]))
    overallCollab.append(d4.mean(axis=1))

for j in range(4):
    d7 = d[7].filter(regex='_{}_'.format(Collabtypes[j]))
    overallCollab.append(d7.mean(axis=1))

print("overallCollab:", overallCollab)


#Add the Overall by year to the dataframe.
for i in range(11):
    if not(i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        data['overall{}'.format(metrics[i])] = overall[i]

#Add the Overall top journal and top citations percentages by year to the dataframe.
i = 0
for threshold in thresholds:
    data['overall{}_thres{}'.format(metrics[9],threshold)] = overallthres[i]
    data['overall{}_thres{}'.format(metrics[10], threshold)] = overallthres[i+4]
    i += 1

#Add the Overall Academiccollabs by year to the dataframe.
for j in range(2):
    data['overall{}_{}'.format(metrics[2],Academiccollabtypes[j])] = overallAcadCollab[j]

for j in range(2):
    data['overall{}_{}'.format(metrics[3],Academiccollabtypes[j])] = overallAcadCollab[j+2]

#Add the Overall Collab by year to the dataframe.
for j in range(4):
    data['overall{}_{}'.format(metrics[4],Collabtypes[j])] = overallCollab[j]

for j in range(4):
    data['overall{}_{}'.format(metrics[7],Collabtypes[j])] = overallCollab[j+4]

print('data: ', data.filter(regex = '^overallAcademicCorporateCollaborationImpact+'))
print('data: ', data.filter(regex = '^overallAcademicCorporateCollaboration_+'))


#Calculate and Add the Overallpercentage by year.
data["overall{}_percentage".format(metrics[1])] = p[0].mean(axis=1)


print(data.filter(regex='overall{}'.format(metrics[1])))


#Overall calculation top journal and top citations for percentile by year according to a percetange threshold.
overallthres = []
for i in range(3,5):
    for threshold in thresholds:
        d9 = p[i].filter(regex='_{}_'.format(threshold))
        overallthres.append(d9.mean(axis=1))

print('overallthresper: ', overallthres)

#Overall calculation for percentile by year according to type of academic collaboration.
overallAcadCollab = []
for j in range(2):
    p1 = p[1].filter(regex='{}_{}_'.format(metrics[2],Academiccollabtypes[j]))
    print("D9:", p1)
    overallAcadCollab.append(p1.mean(axis=1))

print("overallACollabper: ", overallAcadCollab)

#Overall calculation for Cited publications percentile by year according to type of collaboration.
overallCollab = []
for j in range(4):
    p2 = p[2].filter(regex='Collaboration_{}_'.format(Collabtypes[j]))
    overallCollab.append(p2.mean(axis=1))

print("overallCollabper:", overallCollab)

#Add the Overall top journal and top citations percentile by year to the dataframe.
i = 0
for threshold in thresholds:
    data['overall{}_thres{}_percent'.format(metrics[9],threshold)] = overallthres[i]
    data['overall{}_thres{}_percent'.format(metrics[10], threshold)] = overallthres[i+4]
    i += 1

#Add the Overall Academiccollabs percentile by year to the dataframe.
for j in range(2):
    data['overall{}_{}_percent'.format(metrics[2],Academiccollabtypes[j])] = overallAcadCollab[j]

#Add the Overall Collab percentile by year to the dataframe.
for j in range(4):
    data['overall{}_{}'.format(metrics[4],Collabtypes[j])] = overallCollab[j]


#stand calculation for data by year.
stand = []
for i in range(11):
    if not(i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        stand.append(d[i].std(axis=1))
    else:
        stand.append(0)
print("stand:", stand)

#stand calculation for data by year according to percetange threshold.
standthres = []
for i in range(9,11):
    for threshold in thresholds:
        d9 = d[i].filter(regex='_{}_'.format(threshold))
        standthres.append(d9.std(axis=1))

print('standthres: ', standthres)

#stand calculation for data by year according to type of academic collaboration.
standAcadCollab = []
for i in range(2,4):
    for j in range(2):
        d9 = d[i].filter(regex='{}_{}_'.format(metrics[i],Academiccollabtypes[j]))
        print("D9:", d9)
        standAcadCollab.append(d9.std(axis=1))

print("standACollab: ", standAcadCollab)

#stand calculation for data by year according to type of collaboration.
standCollab = []
for j in range(4):
    d4 = d[4].filter(regex='Collaboration_{}_'.format(Collabtypes[j]))
    standCollab.append(d4.std(axis=1))

for j in range(4):
    d7 = d[7].filter(regex='_{}_'.format(Collabtypes[j]))
    standCollab.append(d7.std(axis=1))

print("standCollab:", standCollab)


#Add the stand by year to the dataframe.
for i in range(11):
    if not(i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        data['stand{}'.format(metrics[i])] = stand[i]

#Add the stand top journal and top citations percentages by year to the dataframe.
i = 0
for threshold in thresholds:
    data['stand{}_thres{}'.format(metrics[9],threshold)] = standthres[i]
    data['stand{}_thres{}'.format(metrics[10], threshold)] = standthres[i+4]
    i += 1

#Add the stand Academiccollabs by year to the dataframe.
for j in range(2):
    data['stand{}_{}'.format(metrics[2],Academiccollabtypes[j])] = standAcadCollab[j]

for j in range(2):
    data['stand{}_{}'.format(metrics[3],Academiccollabtypes[j])] = standAcadCollab[j+2]

#Add the stand Collab by year to the dataframe.
for j in range(4):
    data['stand{}_{}'.format(metrics[4],Collabtypes[j])] = standCollab[j]

for j in range(4):
    data['stand{}_{}'.format(metrics[7],Collabtypes[j])] = standCollab[j+4]

print('data: ', data.filter(regex = '^standAcademicCorporateCollaborationImpact+'))
print('data: ', data.filter(regex = '^standAcademicCorporateCollaboration_+'))


#Calculate and Add the standpercentage by year.
data["stand{}_percentage".format(metrics[1])] = p[0].std(axis=1)


print(data.filter(regex='stand{}'.format(metrics[1])))


#stand calculation top journal and top citations for percentile by year according to a percetange threshold.
standthres = []
for i in range(3,5):
    for threshold in thresholds:
        d9 = p[i].filter(regex='_{}_'.format(threshold))
        standthres.append(d9.std(axis=1))

print('standthresper: ', standthres)

#stand calculation for percentile by year according to type of academic collaboration.
standAcadCollab = []
for j in range(2):
    p1 = p[1].filter(regex='{}_{}_'.format(metrics[2],Academiccollabtypes[j]))
    print("D9:", p1)
    standAcadCollab.append(p1.std(axis=1))

print("standACollabper: ", standAcadCollab)

#stand calculation for Cited publications percentile by year according to type of collaboration.
standCollab = []
for j in range(4):
    p2 = p[2].filter(regex='Collaboration_{}_'.format(Collabtypes[j]))
    standCollab.append(p2.std(axis=1))

print("standCollabper:", standCollab)

#Add the stand top journal and top citations percentile by year to the dataframe.
i = 0
for threshold in thresholds:
    data['stand{}_thres{}_percent'.format(metrics[9],threshold)] = standthres[i]
    data['stand{}_thres{}_percent'.format(metrics[10], threshold)] = standthres[i+4]
    i += 1

#Add the stand Academiccollabs percentile by year to the dataframe.
for j in range(2):
    data['stand{}_{}_percent'.format(metrics[2],Academiccollabtypes[j])] = standAcadCollab[j]

#Add the stand Collab percentile by year to the dataframe.
for j in range(4):
    data['stand{}_{}'.format(metrics[4],Collabtypes[j])] = standCollab[j]

#max calculation for data by year.
max = []
for i in range(11):
    if not(i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        max.append(d[i].max(axis=1))
    else:
        max.append(0)
print("max:", max)

#max calculation for data by year according to percetange threshold.
maxthres = []
for i in range(9,11):
    for threshold in thresholds:
        d9 = d[i].filter(regex='_{}_'.format(threshold))
        maxthres.append(d9.max(axis=1))

print('maxthres: ', maxthres)

#max calculation for data by year according to type of academic collaboration.
maxAcadCollab = []
for i in range(2,4):
    for j in range(2):
        d9 = d[i].filter(regex='{}_{}_'.format(metrics[i],Academiccollabtypes[j]))
        print("D9:", d9)
        maxAcadCollab.append(d9.max(axis=1))

print("maxACollab: ", maxAcadCollab)

#max calculation for data by year according to type of collaboration.
maxCollab = []
for j in range(4):
    d4 = d[4].filter(regex='Collaboration_{}_'.format(Collabtypes[j]))
    maxCollab.append(d4.max(axis=1))

for j in range(4):
    d7 = d[7].filter(regex='_{}_'.format(Collabtypes[j]))
    maxCollab.append(d7.max(axis=1))

print("maxCollab:", maxCollab)


#Add the max by year to the dataframe.
for i in range(11):
    if not(i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        data['max{}'.format(metrics[i])] = max[i]

#Add the max top journal and top citations percentages by year to the dataframe.
i = 0
for threshold in thresholds:
    data['max{}_thres{}'.format(metrics[9],threshold)] = maxthres[i]
    data['max{}_thres{}'.format(metrics[10], threshold)] = maxthres[i+4]
    i += 1

#Add the max Academiccollabs by year to the dataframe.
for j in range(2):
    data['max{}_{}'.format(metrics[2],Academiccollabtypes[j])] = maxAcadCollab[j]

for j in range(2):
    data['max{}_{}'.format(metrics[3],Academiccollabtypes[j])] = maxAcadCollab[j+2]

#Add the max Collab by year to the dataframe.
for j in range(4):
    data['max{}_{}'.format(metrics[4],Collabtypes[j])] = maxCollab[j]

for j in range(4):
    data['max{}_{}'.format(metrics[7],Collabtypes[j])] = maxCollab[j+4]

print('data: ', data.filter(regex = '^maxAcademicCorporateCollaborationImpact+'))
print('data: ', data.filter(regex = '^maxAcademicCorporateCollaboration_+'))


#Calculate and Add the maxpercentage by year.
data["max{}_percentage".format(metrics[1])] = p[0].max(axis=1)


print(data.filter(regex='max{}'.format(metrics[1])))


#max calculation top journal and top citations for percentile by year according to a percetange threshold.
maxthres = []
for i in range(3,5):
    for threshold in thresholds:
        d9 = p[i].filter(regex='_{}_'.format(threshold))
        maxthres.append(d9.max(axis=1))

print('maxthresper: ', maxthres)

#max calculation for percentile by year according to type of academic collaboration.
maxAcadCollab = []
for j in range(2):
    p1 = p[1].filter(regex='{}_{}_'.format(metrics[2],Academiccollabtypes[j]))
    print("D9:", p1)
    maxAcadCollab.append(p1.max(axis=1))

print("maxACollabper: ", maxAcadCollab)

#max calculation for Cited publications percentile by year according to type of collaboration.
maxCollab = []
for j in range(4):
    p2 = p[2].filter(regex='Collaboration_{}_'.format(Collabtypes[j]))
    maxCollab.append(p2.max(axis=1))

print("maxCollabper:", maxCollab)

#Add the max top journal and top citations percentile by year to the dataframe.
i = 0
for threshold in thresholds:
    data['max{}_thres{}_percent'.format(metrics[9],threshold)] = maxthres[i]
    data['max{}_thres{}_percent'.format(metrics[10], threshold)] = maxthres[i+4]
    i += 1

#Add the max Academiccollabs percentile by year to the dataframe.
for j in range(2):
    data['max{}_{}_percent'.format(metrics[2],Academiccollabtypes[j])] = maxAcadCollab[j]

#Add the max Collab percentile by year to the dataframe.
for j in range(4):
    data['max{}_{}'.format(metrics[4],Collabtypes[j])] = maxCollab[j]

#min calculation for data by year.
min = []
for i in range(11):
    if not(i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        min.append(d[i].min(axis=1))
    else:
        min.append(0)
print("min:", min)

#min calculation for data by year according to percetange threshold.
minthres = []
for i in range(9,11):
    for threshold in thresholds:
        d9 = d[i].filter(regex='_{}_'.format(threshold))
        minthres.append(d9.min(axis=1))

print('minthres: ', minthres)

#min calculation for data by year according to type of academic collaboration.
minAcadCollab = []
for i in range(2,4):
    for j in range(2):
        d9 = d[i].filter(regex='{}_{}_'.format(metrics[i],Academiccollabtypes[j]))
        print("D9:", d9)
        minAcadCollab.append(d9.min(axis=1))

print("minACollab: ", minAcadCollab)

#min calculation for data by year according to type of collaboration.
minCollab = []
for j in range(4):
    d4 = d[4].filter(regex='Collaboration_{}_'.format(Collabtypes[j]))
    minCollab.append(d4.min(axis=1))

for j in range(4):
    d7 = d[7].filter(regex='_{}_'.format(Collabtypes[j]))
    minCollab.append(d7.min(axis=1))

print("minCollab:", minCollab)


#Add the min by year to the dataframe.
for i in range(11):
    if not(i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        data['min{}'.format(metrics[i])] = min[i]

#Add the min top journal and top citations percentages by year to the dataframe.
i = 0
for threshold in thresholds:
    data['min{}_thres{}'.format(metrics[9],threshold)] = minthres[i]
    data['min{}_thres{}'.format(metrics[10], threshold)] = minthres[i+4]
    i += 1

#Add the min Academiccollabs by year to the dataframe.
for j in range(2):
    data['min{}_{}'.format(metrics[2],Academiccollabtypes[j])] = minAcadCollab[j]

for j in range(2):
    data['min{}_{}'.format(metrics[3],Academiccollabtypes[j])] = minAcadCollab[j+2]

#Add the min Collab by year to the dataframe.
for j in range(4):
    data['min{}_{}'.format(metrics[4],Collabtypes[j])] = minCollab[j]

for j in range(4):
    data['min{}_{}'.format(metrics[7],Collabtypes[j])] = minCollab[j+4]

print('data: ', data.filter(regex = '^minAcademicCorporateCollaborationImpact+'))
print('data: ', data.filter(regex = '^minAcademicCorporateCollaboration_+'))


#Calculate and Add the minpercentage by year.
data["min{}_percentage".format(metrics[1])] = p[0].min(axis=1)


print(data.filter(regex='min{}'.format(metrics[1])))


#min calculation top journal and top citations for percentile by year according to a percetange threshold.
minthres = []
for i in range(3,5):
    for threshold in thresholds:
        d9 = p[i].filter(regex='_{}_'.format(threshold))
        minthres.append(d9.min(axis=1))

print('minthresper: ', minthres)

#min calculation for percentile by year according to type of academic collaboration.
minAcadCollab = []
for j in range(2):
    p1 = p[1].filter(regex='{}_{}_'.format(metrics[2],Academiccollabtypes[j]))
    print("D9:", p1)
    minAcadCollab.append(p1.min(axis=1))

print("minACollabper: ", minAcadCollab)

#min calculation for Cited publications percentile by year according to type of collaboration.
minCollab = []
for j in range(4):
    p2 = p[2].filter(regex='Collaboration_{}_'.format(Collabtypes[j]))
    minCollab.append(p2.min(axis=1))

print("minCollabper:", minCollab)

#Add the min top journal and top citations percentile by year to the dataframe.
i = 0
for threshold in thresholds:
    data['min{}_thres{}_percent'.format(metrics[9],threshold)] = minthres[i]
    data['min{}_thres{}_percent'.format(metrics[10], threshold)] = minthres[i+4]
    i += 1

#Add the min Academiccollabs percentile by year to the dataframe.
for j in range(2):
    data['min{}_{}_percent'.format(metrics[2],Academiccollabtypes[j])] = minAcadCollab[j]

#Add the min Collab percentile by year to the dataframe.
for j in range(4):
    data['min{}_{}'.format(metrics[4],Collabtypes[j])] = minCollab[j]

data.to_csv('/Users/jesusllanogarcia/Desktop/Projecto/universities_data-overall-std-min-max.csv')
