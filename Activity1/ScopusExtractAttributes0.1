from os import listdir
import pandas as pd
import re

lists = listdir('/Users/jesusllanogarcia/Downloads/Scopus')
count = [[] for uni in lists]

#Names for the Table Attributes.
top_countries = ['Documents_by_country_top_1', 'Documents_by_country_top_2', 'Documents_by_country_top_3',
                 'Documents_by_country_top_4', 'Documents_by_country_top_5', 'Docnumber_by_country_top_1',
                 'Docnumbers_by_country_top_2', 'Docnumber_by_country_top_3', 'Docnumber_by_country_top_4',
                 'Docnumber_by_country_top_5']

top_Aff = ['Documents_by_affiliation_top_1', 'Documents_by_affiliation_top_2', 'Documents_by_affiliation_top_3',
                 'Documents_by_affiliation_top_4', 'Documents_by_affiliation_top_5', 'Docnumber_by_affiliation_top_1',
                 'Docnumber_by_affiliation_top_2', 'Docnumber_by_affiliation_top_3', 'Docnumber_by_affiliation_top_4',
                 'Docnumber_by_affiliation_top_5']

top_Author = ['Documents_by_Author_top_1', 'Documents_by_Author_top_2', 'Documents_by_Author_top_3',
                 'Documents_by_Author_top_4', 'Documents_by_Author_top_5']

Granted_Awards = ['Institution_Grants_top_1', 'Institution_Grants_top_2', 'Institution_Grants_top_3',
                 'Institution_Grants_top_4', 'Institution_Grants_top_5','Awarded_Grants_top_1', 'Awarded_Grants_top_2', 'Awarded_Grants_top_3',
                 'Awarded_Grants_top_4', 'Awarded_Grants_top_5']

Publications_Type = ['Article', 'Conference Paper', 'Book Chapter', 'Review', 'Editorial']

#Final DataFrame with the data.
FinalData = pd.DataFrame()
for i in range(len(lists)):
    data = {'Name': [lists[i]]}
    emptydf = pd.DataFrame(data)
    print(emptydf)
    if not re.search(r'.DS_Store\b', lists[i]):
        #Obtain the names for the universities.
        print('names:', lists[i])
        lists2 = listdir('/Users/jesusllanogarcia/Downloads/Scopus/{}'.format(lists[i]))
        for j in range(len(lists2)):
            #Conditions for the code to search the documents according to the type of information they have. 
            #Refine_Values contains most of the information
            if re.search(r'-Analyze-Country\b', lists2[j]):
                #This part obtaines the name of the top 5 countries where the institution has collaborated and the amount of publications out of those collabs.
                country = pd.read_csv('/Users/jesusllanogarcia/Downloads/Scopus/{}/{}'.format(lists[i], lists2[j]),error_bad_lines=False,
                                      skiprows=7)
                # country_top = country[:, :5]
                country = country.transpose()
                country_top = country.iloc[0, 0:5]
                country_top_value = country.iloc[1, 0:5]
                features = pd.concat([country_top, country_top_value])
                features = pd.DataFrame(features)
                features = features.transpose()
                features.columns = top_countries
                # print(country_top)
                emptydf = emptydf.join(features, lsuffix='_left', rsuffix='_right')

            if re.search(r'Scopus_exported_refine_values\b', lists2[j]):
                df1 = pd.read_csv('/Users/jesusllanogarcia/Downloads/Scopus/{}/{}'.format(lists[i], lists2[j]), delimiter=',',error_bad_lines=False,
                                     skiprows=7)
                 #df_new obtains the totals by year of the refine, the number of articles by access type per year, the number of publicationsby author
                 #the number of publications by type, 
                df_new = []
                features = pd.DataFrame()
                for k in range(0, 10, 2):
                    print("k: ", k)
                    df_new.append(df1.iloc[:, 0+k:2+k])

                df_new.pop(3)
                for k in range(len(df_new)):
                    df_new[k] = df_new[k].iloc[0:5, :]
                    print("df_new: ", df_new[k])

                df_new[2]['AUTHOR NAME'] = top_Author

                for k in range(len(df_new)):
                    print(df_new[k])
                    print(lists[i])
                    df_new[k] = df_new[k].dropna(how='all')
                    df_new[k].columns = [0,1]


                for k in range(len(df_new)):
                    features = pd.concat([features, df_new[k]], ignore_index=True)

                features = features.transpose()
                features.columns = features.iloc[0]
                features = features.drop(index=0)
                features = features.reset_index()
                emptydf = emptydf.join(features,lsuffix='_left', rsuffix='_right')

            if re.search(r'-Analyze-Affiliation\b', lists2[j]):
                Aff = pd.read_csv('/Users/jesusllanogarcia/Downloads/Scopus/{}/{}'.format(lists[i], lists2[j]),error_bad_lines=False,
                                      skiprows=7)
                                      
                #This part obtains the number of publications by the top five affiliations of the university.
                print('Aff:', Aff)
                Aff.columns = [0, 1]
                Aff = Aff.iloc[0:5, :]
                print(Aff)
                Aff = Aff.transpose()
                print(Aff)
                Aff_name = Aff.iloc[0, 0:5]
                Aff_values = Aff.iloc[1, 0:5]
                print(Aff_name)
                print(Aff_values)
                features = pd.concat([Aff_name, Aff_values])
                features = pd.DataFrame(features)
                features = features.transpose()
                features.columns = top_Aff
                print("AFFeatures: ",features)
                print(Aff)
                emptydf = emptydf.join(features,lsuffix='_left', rsuffix='_right')

            if re.search(r'-Analyze-FundingSponsor\b', lists2[j]):
                Funding = pd.read_csv('/Users/jesusllanogarcia/Downloads/Scopus/{}/{}'.format(lists[i], lists2[j]),error_bad_lines=False,
                                      skiprows=7)
                #This part obtains the top five funding sponsors of the university and the amount of awards granted to the university.
                Funding.columns = [0, 1]
                Funding = Funding.iloc[0:5, :]
                Funding = Funding.transpose()
                Funding_name = Funding.iloc[0, 0:5]
                Funding_values = Funding.iloc[1, 0:5]
                features = pd.concat([Funding_name, Funding_values])
                features = pd.DataFrame(features)
                features = features.transpose()
                features.columns = Granted_Awards
                emptydf = emptydf.join(features,lsuffix='_left', rsuffix='_right')
    for k in range(len(df_new)):
        df_new[k].to_csv('/Users/jesusllanogarcia/Downloads/Scopus processed/processed_df_new{}.csv'.format(k))
    FinalData = pd.concat([FinalData,emptydf], ignore_index=True, sort=True)
    print("Final:",FinalData)
    FinalData.to_csv('/Users/jesusllanogarcia/Downloads/Scopus processed/processed_FINAL2.csv')
    emptydf.to_csv('/Users/jesusllanogarcia/Downloads/Scopus processed/processed_{}.csv'.format(lists[i]))
    print(emptydf['Name'])
