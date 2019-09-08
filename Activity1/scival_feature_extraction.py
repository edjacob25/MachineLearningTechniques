import pandas as pd

metrics = {0: 'ScholarlyOutput', 1: 'CitedPublications', 2: 'AcademicCorporateCollaboration',
           3: 'AcademicCorporateCollaborationImpact', 4: 'Collaboration', 5: 'CitationCount',
           6: 'CitationsPerPublication', 7: 'CollaborationImpact', 8: 'FieldWeightedCitationImpact',
           9: 'PublicationsInTopJournalPercentiles', 10: 'OutputsInTopCitationPercentiles'}

academic_collabtypes = {0: 'Academic-corporatecollaboration', 1: 'Noacademic-corporatecollaboration'}

collabtypes = {0: 'Institutionalcollaboration', 1: 'Internationalcollaboration', 2: 'Nationalcollaboration',
               3: 'Singleauthorship', }

thresholds = [1, 5, 10, 25]

data = pd.read_csv('/Users/jesusllanogarcia/Desktop/Projecto/universities_data-uri2.csv').iloc[:, 1:]

# Split data into data with values per year and data with percentages by year.
d = []
for i in range(11):
    d1 = data.filter(regex=f'^{metrics[i]}')
    d.append(d1.filter(regex='valueByYear'))

p = []
for i in range(11):
    d1 = data.filter(regex=f'^{metrics[i]}')
    d1 = d1.filter(regex='percentageByYear')
    print(d1.empty)
    if not d1.empty:
        p.append(d1.filter(regex='percentageByYear'))

print(d)

for i in range(len(p)):
    print(f"p: {p[i].columns}")

# Overall calculation for data by year.
overall = []
for i in range(11):
    if not (i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        overall.append(d[i].mean(axis=1))
    else:
        overall.append(0)
print(f"overall: {overall}")

# Overall calculation for data by year according to percetange threshold.
overall_thres = []
for i in range(9, 11):
    for threshold in thresholds:
        d9 = d[i].filter(regex=f'_{threshold}_')
        overall_thres.append(d9.mean(axis=1))

print(f'overallthres: {overall_thres}')

# Overall calculation for data by year according to type of academic collaboration.
overall_acad_collab = []
for i in range(2, 4):
    for j in range(2):
        d9 = d[i].filter(regex=f'{metrics[i]}_{academic_collabtypes[j]}_')
        print("D9:", d9)
        overall_acad_collab.append(d9.mean(axis=1))

print(f"overallACollab: {overall_acad_collab}")

# Overall calculation for data by year according to type of collaboration.
overall_collab = []
for j in range(4):
    d4 = d[4].filter(regex=f'Collaboration_{collabtypes[j]}_')
    overall_collab.append(d4.mean(axis=1))

for j in range(4):
    d7 = d[7].filter(regex=f'_{collabtypes[j]}_')
    overall_collab.append(d7.mean(axis=1))

print(f"overallCollab: {overall_collab}")

# Add the Overall by year to the dataframe.
for i in range(11):
    if not (i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        data[f'overall{metrics[i]}'] = overall[i]

# Add the Overall top journal and top citations percentages by year to the dataframe.
for i, threshold in enumerate(thresholds):
    data[f'overall{metrics[9]}_thres{threshold}'] = overall_thres[i]
    data[f'overall{metrics[10]}_thres{threshold}'] = overall_thres[i + 4]

# Add the Overall Academiccollabs by year to the dataframe.
for j in range(2):
    data[f'overall{metrics[2]}_{academic_collabtypes[j]}'] = overall_acad_collab[j]

for j in range(2):
    data[f'overall{metrics[3]}_{academic_collabtypes[j]}'] = overall_acad_collab[j + 2]

# Add the Overall Collab by year to the dataframe.
for j in range(4):
    data[f'overall{metrics[4]}_{collabtypes[j]}'] = overall_collab[j]

for j in range(4):
    data[f'overall{metrics[7]}_{collabtypes[j]}'] = overall_collab[j + 4]

print('data: ', data.filter(regex='^overallAcademicCorporateCollaborationImpact+'))
print('data: ', data.filter(regex='^overallAcademicCorporateCollaboration_+'))

# Calculate and Add the Overallpercentage by year.
data[f"overall{metrics[1]}_percentage"] = p[0].mean(axis=1)

print(data.filter(regex=f'overall{metrics[1]}'))

# Overall calculation top journal and top citations for percentile by year according to a percetange threshold.
overall_thres = []
for i in range(3, 5):
    for threshold in thresholds:
        d9 = p[i].filter(regex=f'_{threshold}_')
        overall_thres.append(d9.mean(axis=1))

print(f'overallthresper: {overall_thres}')

# Overall calculation for percentile by year according to type of academic collaboration.
overall_acad_collab = []
for j in range(2):
    p1 = p[1].filter(regex=f'{metrics[2]}_{academic_collabtypes[j]}_')
    print(f"D9: {p1}")
    overall_acad_collab.append(p1.mean(axis=1))

print(f"overallACollabper: {overall_acad_collab}")

# Overall calculation for Cited publications percentile by year according to type of collaboration.
overall_collab = []
for j in range(4):
    p2 = p[2].filter(regex=f'Collaboration_{collabtypes[j]}_')
    overall_collab.append(p2.mean(axis=1))

print(f"overallCollabper: {overall_collab}")

# Add the Overall top journal and top citations percentile by year to the dataframe.
for i, threshold in enumerate(thresholds):
    data[f'overall{metrics[9]}_thres{threshold}_percent'] = overall_thres[i]
    data[f'overall{metrics[10]}_thres{threshold}_percent'] = overall_thres[i + 4]

# Add the Overall Academiccollabs percentile by year to the dataframe.
for j in range(2):
    data[f'overall{metrics[2]}_{academic_collabtypes[j]}_percent'] = overall_acad_collab[j]

# Add the Overall Collab percentile by year to the dataframe.
for j in range(4):
    data[f'overall{metrics[4]}_{collabtypes[j]}'] = overall_collab[j]

# stand calculation for data by year.
stand = []
for i in range(11):
    if not (i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        stand.append(d[i].std(axis=1))
    else:
        stand.append(0)
print(f"stand: {stand}")

# stand calculation for data by year according to percetange threshold.
stand_thres = []
for i in range(9, 11):
    for threshold in thresholds:
        d9 = d[i].filter(regex=f"_{threshold}_")
        stand_thres.append(d9.std(axis=1))

print(f'standthres: {stand_thres}')

# stand calculation for data by year according to type of academic collaboration.
standAcadCollab = []
for i in range(2, 4):
    for j in range(2):
        d9 = d[i].filter(regex=f'{metrics[i]}_{academic_collabtypes[j]}_')
        print(f"D9: {d9}")
        standAcadCollab.append(d9.std(axis=1))

print(f"standACollab: {standAcadCollab}")

# stand calculation for data by year according to type of collaboration.
standCollab = []
for j in range(4):
    d4 = d[4].filter(regex=f'Collaboration_{collabtypes[j]}_')
    standCollab.append(d4.std(axis=1))

for j in range(4):
    d7 = d[7].filter(regex=f'_{collabtypes[j]}_')
    standCollab.append(d7.std(axis=1))

print("standCollab:", standCollab)

# Add the stand by year to the dataframe.
for i in range(11):
    if not (i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        data[f'stand{metrics[i]}'] = stand[i]

# Add the stand top journal and top citations percentages by year to the dataframe.
for i, threshold in enumerate(thresholds):
    data[f'stand{metrics[9]}_thres{threshold}'] = stand_thres[i]
    data[f'stand{metrics[10]}_thres{threshold}'] = stand_thres[i + 4]

# Add the stand Academiccollabs by year to the dataframe.
for j in range(2):
    data[f'stand{metrics[2]}_{academic_collabtypes[j]}'] = standAcadCollab[j]

for j in range(2):
    data[f'stand{metrics[3]}_{academic_collabtypes[j]}'] = standAcadCollab[j + 2]

# Add the stand Collab by year to the dataframe.
for j in range(4):
    data[f'stand{metrics[4]}_{collabtypes[j]}'] = standCollab[j]

for j in range(4):
    data[f'stand{metrics[7]}_{collabtypes[j]}'] = standCollab[j + 4]

print('data: ', data.filter(regex='^standAcademicCorporateCollaborationImpact+'))
print('data: ', data.filter(regex='^standAcademicCorporateCollaboration_+'))

# Calculate and Add the standpercentage by year.
data[f"stand{metrics[1]}_percentage"] = p[0].std(axis=1)

print(data.filter(regex=f'stand{metrics[1]}'))

# stand calculation top journal and top citations for percentile by year according to a percetange threshold.
stand_thres = []
for i in range(3, 5):
    for threshold in thresholds:
        d9 = p[i].filter(regex=f'_{threshold}_')
        stand_thres.append(d9.std(axis=1))

print('standthresper: ', stand_thres)

# stand calculation for percentile by year according to type of academic collaboration.
standAcadCollab = []
for j in range(2):
    p1 = p[1].filter(regex=f'{metrics[2]}_{academic_collabtypes[j]}_')
    print("D9:", p1)
    standAcadCollab.append(p1.std(axis=1))

print("standACollabper: ", standAcadCollab)

# stand calculation for Cited publications percentile by year according to type of collaboration.
standCollab = []
for j in range(4):
    p2 = p[2].filter(regex=f'Collaboration_{collabtypes[j]}_')
    standCollab.append(p2.std(axis=1))

print("standCollabper:", standCollab)

# Add the stand top journal and top citations percentile by year to the dataframe.
for i, threshold in enumerate(thresholds):
    data[f'stand{metrics[9]}_thres{threshold}_percent'] = stand_thres[i]
    data[f'stand{metrics[10]}_thres{threshold}_percent'] = stand_thres[i + 4]

# Add the stand Academiccollabs percentile by year to the dataframe.
for j in range(2):
    data[f'stand{metrics[2]}_{academic_collabtypes[j]}_percent'] = standAcadCollab[j]

# Add the stand Collab percentile by year to the dataframe.
for j in range(4):
    data[f'stand{metrics[4]}_{collabtypes[j]}'] = standCollab[j]

# max calculation for data by year.
max = []
for i in range(11):
    if not (i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        max.append(d[i].max(axis=1))
    else:
        max.append(0)
print("max:", max)

# max calculation for data by year according to percetange threshold.
maxthres = []
for i in range(9, 11):
    for threshold in thresholds:
        d9 = d[i].filter(regex=f'_{threshold}_')
        maxthres.append(d9.max(axis=1))

print('maxthres: ', maxthres)

# max calculation for data by year according to type of academic collaboration.
max_acad_collab = []
for i in range(2, 4):
    for j in range(2):
        d9 = d[i].filter(regex=f'{metrics[i]}_{academic_collabtypes[j]}_')
        print("D9:", d9)
        max_acad_collab.append(d9.max(axis=1))

print("maxACollab: ", max_acad_collab)

# max calculation for data by year according to type of collaboration.
maxCollab = []
for j in range(4):
    d4 = d[4].filter(regex=f'Collaboration_{collabtypes[j]}_')
    maxCollab.append(d4.max(axis=1))

for j in range(4):
    d7 = d[7].filter(regex=f'_{collabtypes[j]}_')
    maxCollab.append(d7.max(axis=1))

print("maxCollab:", maxCollab)

# Add the max by year to the dataframe.
for i in range(11):
    if not (i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        data[f'max{metrics[i]}'] = max[i]

# Add the max top journal and top citations percentages by year to the dataframe.

for i, threshold in enumerate(thresholds):
    data[f'max{metrics[9]}_thres{threshold}'] = maxthres[i]
    data[f'max{metrics[10]}_thres{threshold}'] = maxthres[i + 4]

# Add the max Academiccollabs by year to the dataframe.
for j in range(2):
    data[f'max{metrics[2]}_{academic_collabtypes[j]}'] = max_acad_collab[j]

for j in range(2):
    data[f'max{metrics[3]}_{academic_collabtypes[j]}'] = max_acad_collab[j + 2]

# Add the max Collab by year to the dataframe.
for j in range(4):
    data[f'max{metrics[4]}_{collabtypes[j]}'] = maxCollab[j]

for j in range(4):
    data[f'max{metrics[7]}_{collabtypes[j]}'] = maxCollab[j + 4]

print('data: ', data.filter(regex='^maxAcademicCorporateCollaborationImpact+'))
print('data: ', data.filter(regex='^maxAcademicCorporateCollaboration_+'))

# Calculate and Add the maxpercentage by year.
data[f"max{metrics[1]}_percentage"] = p[0].max(axis=1)

print(data.filter(regex=f'max{metrics[1]}'))

# max calculation top journal and top citations for percentile by year according to a percetange threshold.
maxthres = []
for i in range(3, 5):
    for threshold in thresholds:
        d9 = p[i].filter(regex=f'_{threshold}_')
        maxthres.append(d9.max(axis=1))

print('maxthresper: ', maxthres)

# max calculation for percentile by year according to type of academic collaboration.
max_acad_collab = []
for j in range(2):
    p1 = p[1].filter(regex=f'{metrics[2]}_{academic_collabtypes[j]}_')
    print("D9:", p1)
    max_acad_collab.append(p1.max(axis=1))

print("maxACollabper: ", max_acad_collab)

# max calculation for Cited publications percentile by year according to type of collaboration.
maxCollab = []
for j in range(4):
    p2 = p[2].filter(regex=f'Collaboration_{collabtypes[j]}_')
    maxCollab.append(p2.max(axis=1))

print("maxCollabper:", maxCollab)

# Add the max top journal and top citations percentile by year to the dataframe.
for i, threshold in enumerate(thresholds):
    data[f'max{metrics[9]}_thres{threshold}_percent'] = maxthres[i]
    data[f'max{metrics[10]}_thres{threshold}_percent'] = maxthres[i + 4]

# Add the max Academiccollabs percentile by year to the dataframe.
for j in range(2):
    data[f'max{metrics[2]}_{academic_collabtypes[j]}_percent'] = max_acad_collab[j]

# Add the max Collab percentile by year to the dataframe.
for j in range(4):
    data[f'max{metrics[4]}_{collabtypes[j]}'] = maxCollab[j]

# min calculation for data by year.
min = []
for i in range(11):
    if not (i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        min.append(d[i].min(axis=1))
    else:
        min.append(0)
print("min:", min)

# min calculation for data by year according to percetange threshold.
minthres = []
for i in range(9, 11):
    for threshold in thresholds:
        d9 = d[i].filter(regex=f'_{threshold}_')
        minthres.append(d9.min(axis=1))

print('minthres: ', minthres)

# min calculation for data by year according to type of academic collaboration.
minAcadCollab = []
for i in range(2, 4):
    for j in range(2):
        d9 = d[i].filter(regex=f'{metrics[i]}_{academic_collabtypes[j]}_')
        print("D9:", d9)
        minAcadCollab.append(d9.min(axis=1))

print("minACollab: ", minAcadCollab)

# min calculation for data by year according to type of collaboration.
minCollab = []
for j in range(4):
    d4 = d[4].filter(regex=f'Collaboration_{collabtypes[j]}_')
    minCollab.append(d4.min(axis=1))

for j in range(4):
    d7 = d[7].filter(regex=f'_{collabtypes[j]}_')
    minCollab.append(d7.min(axis=1))

print("minCollab:", minCollab)

# Add the min by year to the dataframe.
for i in range(11):
    if not (i == 2 or i == 3 or i == 4 or i == 9 or i == 10 or i == 7):
        print(i)
        data[f'min{metrics[i]}'] = min[i]

# Add the min top journal and top citations percentages by year to the dataframe.
for i, threshold in enumerate(thresholds):
    data[f'min{metrics[9]}_thres{threshold}'] = minthres[i]
    data[f'min{metrics[10]}_thres{threshold}'] = minthres[i + 4]

# Add the min Academiccollabs by year to the dataframe.
for j in range(2):
    data[f'min{metrics[2]}_{academic_collabtypes[j]}'] = minAcadCollab[j]

for j in range(2):
    data[f'min{metrics[3]}_{academic_collabtypes[j]}'] = minAcadCollab[j + 2]

# Add the min Collab by year to the dataframe.
for j in range(4):
    data[f'min{metrics[4]}_{collabtypes[j]}'] = minCollab[j]

for j in range(4):
    data[f'min{metrics[7]}_{collabtypes[j]}'] = minCollab[j + 4]

print('data: ', data.filter(regex='^minAcademicCorporateCollaborationImpact+'))
print('data: ', data.filter(regex='^minAcademicCorporateCollaboration_+'))

# Calculate and Add the minpercentage by year.
data[f"min{metrics[1]}_percentage"] = p[0].min(axis=1)

print(data.filter(regex=f'min{metrics[1]}'))

# min calculation top journal and top citations for percentile by year according to a percetange threshold.
minthres = []
for i in range(3, 5):
    for threshold in thresholds:
        d9 = p[i].filter(regex=f'_{threshold}_')
        minthres.append(d9.min(axis=1))

print('minthresper: ', minthres)

# min calculation for percentile by year according to type of academic collaboration.
minAcadCollab = []
for j in range(2):
    p1 = p[1].filter(regex=f'{metrics[2]}_{academic_collabtypes[j]}_')
    print("D9:", p1)
    minAcadCollab.append(p1.min(axis=1))

print("minACollabper: ", minAcadCollab)

# min calculation for Cited publications percentile by year according to type of collaboration.
minCollab = []
for j in range(4):
    p2 = p[2].filter(regex=f'Collaboration_{collabtypes[j]}_')
    minCollab.append(p2.min(axis=1))

print("minCollabper:", minCollab)

# Add the min top journal and top citations percentile by year to the dataframe.
for i, threshold in enumerate(thresholds):
    data[f'min{metrics[9]}_thres{threshold}_percent'] = minthres[i]
    data[f'min{metrics[10]}_thres{threshold}_percent'] = minthres[i + 4]

# Add the min Academiccollabs percentile by year to the dataframe.
for j in range(2):
    data[f'min{metrics[2]}_{academic_collabtypes[j]}_percent'] = minAcadCollab[j]

# Add the min Collab percentile by year to the dataframe.
for j in range(4):
    data[f'min{metrics[4]}_{collabtypes[j]}'] = minCollab[j]

data.to_csv('/Users/jesusllanogarcia/Desktop/Projecto/universities_data-overall-std-min-max.csv')
