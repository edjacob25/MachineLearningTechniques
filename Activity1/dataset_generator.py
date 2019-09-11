import json
import os
import re
from typing import List

import numpy as np
import pandas as pd

from common import camel_case_to_snake_case, load_institutions, isnumber


def convert_initial_to_row(data: dict, rank: int, document_specific=False) -> List:
    row = [rank, data["name"], data["country"]]
    if document_specific:
        row = []
    for metric in data["metrics"]:
        if "valueByYear" in metric:
            for year in metric["valueByYear"]:
                row.append(metric["valueByYear"][year])
        if "values" in metric:
            for value in metric["values"]:
                for year in value["valueByYear"]:
                    row.append(value["valueByYear"][year])
    return row


def get_header_by_year(metric_name: str, metric: dict, percentage=False) -> List[str]:
    if percentage:
        return [f"{metric_name}_percentage_{year}" for year in metric['percentageByYear']]
    else:
        return [f"{metric_name}_{year}" for year in metric["valueByYear"]]


def get_headers(data: dict, document_type: str = None) -> List[str]:
    headers = ["rank", "name", "country"]
    if document_type is not None:
        headers = []
    for metric in data["metrics"]:
        metric_name = camel_case_to_snake_case(metric["metricType"])
        if document_type is not None:
            metric_name = f"{metric_name}_{document_type}"

        if "valueByYear" in metric:
            headers.extend(get_header_by_year(metric_name, metric))
        # if "percentageByYear" in metric:
        #     headers.extend(get_header_by_year(metric_name, metric, percentage=True))
        if "values" in metric:
            for value in metric["values"]:
                if "collabType" in value:
                    if "corporate" in metric_name:
                        if "No" in value["collabType"]:
                            composed_name = f"no_{metric_name}"
                        else:
                            composed_name = f"{metric_name}"
                    else:
                        collab_type = value["collabType"].split(" ")[0].lower()
                        composed_name = f"{metric_name}_{collab_type}"
                else:
                    threshold = value['threshold']
                    if document_type is None:
                        parts = metric_name.rsplit('_', 2)
                        composed_name = f"{parts[0]}_{threshold}percent_{parts[1]}"
                    else:
                        parts = metric_name.rsplit('_', 3)
                        composed_name = f"{parts[0]}_{threshold}percent_{parts[1]}_{parts[3]}"
                headers.extend(get_header_by_year(composed_name, value))
            # headers.extend(get_header_by_year(composed_name, value, percentage=True))
    headers = [camel_case_to_snake_case(x).replace("__", "_") for x in headers]
    return headers


def get_author_info() -> pd.DataFrame:
    headers = ["top_500_authors_output_avg", "top_500_authors_output_annual_avg", "top_500_authors_hindex_avg",
               "top_500_authors_citacions_avg", "top_500_authors_citacions_annual_avg",
               "top_500_authors_citacions_per_publication_avg", "top_500_authors_citacions_per_publication_annual_avg"]
    pattern = re.compile(r"\d{1,3}_.*")
    result = pd.DataFrame(columns=headers)
    dirs = [x for x in os.listdir("Data/Scopus") if pattern.match(x)]
    for directory in dirs:
        file_path = os.path.join("Data/Scopus", directory, "List_of_authors.csv")
        a = pd.read_csv(file_path, header=9)
        a = a.iloc[:-1, [1, 3, 4, 5, 6]]
        a = a.mean()
        serie = pd.Series(index=headers)
        serie.name = int(directory.split("_")[0])
        serie["top_500_authors_output_avg"] = a[0]
        serie["top_500_authors_output_annual_avg"] = a[0] / 5
        serie["top_500_authors_hindex_avg"] = a[4]
        serie["top_500_authors_citacions_avg"] = a[1]
        serie["top_500_authors_citacions_annual_avg"] = a[1] / 5
        serie["top_500_authors_citacions_per_publication_avg"] = a[2]
        serie["top_500_authors_citacions_per_publication_annual_avg"] = a[0] / 5
        result = result.append(serie)
    left = [x for x in range(0, 200) if x not in result.index]
    for i in left:
        result = result.append(pd.Series(index=headers, name=i))
    return result.sort_index()


def get_funding_info() -> pd.DataFrame:
    headers = ["grants_value", "grants_value_per_year", "grants_value_growth", "number_of_grants",
               "number_of_grants_per_year", "number_of_grants_growth", "number_of_sponsors"]
    pattern = re.compile(r"\d{1,3}_.*")
    result = pd.DataFrame(columns=headers)
    dirs = [x for x in os.listdir("Data/Scopus") if pattern.match(x)]
    for directory in dirs:
        index = int(directory.split("_")[0])
        serie = pd.Series(index=headers)
        serie.name = index
        try:

            file_path = os.path.join("Data/Scopus", directory, "Awarded_Grants_by_Funding_Body.csv")
            a = pd.read_csv(file_path, header=6)
            a = a.iloc[:-1, [2, 4, 5, 6]]
            a = a[a.applymap(isnumber)]
            a.iloc[:, 1] = pd.to_numeric(a.iloc[:, 1])
            a.iloc[:, 3] = pd.to_numeric(a.iloc[:, 3])
            summation = a.sum()
            avg = a.mean()

            serie["grants_value"] = summation[0]
            serie["grants_value_per_year"] = summation[0] / 5
            serie["grants_value_growth"] = avg[1]
            serie["number_of_grants"] = summation[2]
            serie["number_of_grants_per_year"] = summation[2] / 5
            serie["number_of_grants_growth"] = avg[3]
            serie["number_of_sponsors"] = a.shape[0]
        except FileNotFoundError:
            pass
        finally:
            result = result.append(serie)

    left = [x for x in range(0, 200) if x not in result.index]
    for i in left:
        result = result.append(pd.Series(index=headers, name=i))
    return result.sort_index()


def normalize_country_name(name: str) -> str:
    name = name.replace(' ', '_')
    name = name.replace("'", '')
    name = camel_case_to_snake_case(name)
    return name.replace("__", "_")


def get_country_headers(dirs: List[str]) -> List[str]:
    all_countries = {}
    for directory in dirs:
        file_path = os.path.join("Data/Scopus", directory, "countries.csv")
        try:
            a = pd.read_csv(file_path, header=3)
            for country in a.iloc[:, 0]:
                all_countries[country] = {}
        except FileNotFoundError:
            pass

    return [f"collaboration_{normalize_country_name(x)}" for x in all_countries]


def get_country_info() -> pd.DataFrame:
    pattern = re.compile(r"\d{1,3}_.*")
    dirs = [x for x in os.listdir("Data/Scopus") if pattern.match(x)]
    headers = get_country_headers(dirs) + ["biggest_country_collaborator"]

    result = pd.DataFrame(columns=headers)
    for directory in dirs:
        serie = pd.Series(index=headers, name=int(directory.split("_")[0]))
        try:
            file_path = os.path.join("Data/Scopus", directory, "countries.csv")
            a = pd.read_csv(file_path, header=3)
            for country, quantity in zip(a.iloc[:, 0], a.iloc[:, 1]):
                serie[f"collaboration_{normalize_country_name(country)}"] = quantity
            biggest_collaborator = a.iloc[a.iloc[:, 1].idxmax(), 0]
            serie["biggest_country_collaborator"] = biggest_collaborator
        except FileNotFoundError:
            pass
        result = result.append(serie)
    left = [x for x in range(0, 200) if x not in result.index]
    for i in left:
        result = result.append(pd.Series(index=headers, name=i))
    return result.sort_index()


def fix_csv_folder_names():
    institutions = load_institutions()
    taken = []
    names = [x.name for x in institutions]
    dirs = os.listdir("Data/Scopus")
    for directory in dirs:
        pattern = re.compile(r"\d{1,3}_.*")
        if pattern.match(directory):
            print(f"{directory} already fixed")
            taken.append([x for x in institutions if x.name in directory][0])
            continue
        if directory in names:
            inst = [x for x in institutions if x.name == directory][0]
            print(f"{inst.name} found with rank {inst.rank}")
        else:
            decision = "n"
            skip = False
            inst = None
            while decision != "y":
                print(f"{directory} not found")
                left = [x for x in institutions if x not in taken]
                print(left)
                chosen = input("Choose the institution: ")
                if chosen == "s":
                    skip = True
                    decision = "y"

                else:
                    inst = [x for x in institutions if x.rank == int(chosen)][0]
                    print(f"Chosen {inst.name} with rank {inst.rank} for folder {directory}")
                    decision = input("Sure? y/n ")
            if skip:
                continue
        directory = os.path.join("Data/Scopus", directory)
        os.rename(directory, f"Data/Scopus/{inst.rank}_{inst.name}")
        taken.append(inst)


def fix_csv_names():
    dirs = os.listdir("Data/Scopus")
    for directory in dirs:
        directory = os.path.join("Data/Scopus", directory)
        for file in os.listdir(directory):
            try:
                if "List_of_authors" in file:
                    os.rename(os.path.join(directory, file), os.path.join(directory, "List_of_authors.csv"))
                elif "Awarded_Grants_by_Funding_Body" in file:
                    os.rename(os.path.join(directory, file), os.path.join(directory,
                                                                          "Awarded_Grants_by_Funding_Body.csv"))
                elif "Analyze-Country" in file:
                    os.rename(os.path.join(directory, file), os.path.join(directory, "countries.csv"))
            except FileExistsError:
                pass


def create_main_dataset() -> pd.DataFrame:
    headers = None
    rows = []
    files = os.listdir("Data/Scival")
    files.sort(key=lambda x: int(x.split("_", 1)[0]))
    for filename in files:
        file_path = os.path.join("Data/Scival", filename)
        with open(file_path, "r") as file:
            data = json.load(file)
            rank = int(filename.split("_")[0]) + 1
            if headers is None:
                headers = get_headers(data)
            row = convert_initial_to_row(data, rank)

        rows.append(row)
    return pd.DataFrame(data=rows, columns=headers)


def expand_data(data: pd.DataFrame) -> pd.DataFrame:
    headers = data.columns
    pattern = re.compile(".*_[0-9]{4}")
    headers = [x for x in headers if pattern.match(x)]
    items = {x.rsplit("_", 1)[0]: {} for x in headers}

    for item in items:
        selected = [x for x in headers if item in x]
        insertion_index = list(data.columns).index(selected[-1]) + 1
        selected_df = data.loc[:, selected]
        avg = selected_df.mean(axis=1)
        avg.name = f"{item}_avg"
        change = selected_df.diff(axis=1).mean(axis=1)
        change.name = f"{item}_growth"
        acc = selected_df.diff(axis=1).diff(axis=1).mean(axis=1)
        acc.name = f"{item}_growth_acc"
        data.insert(insertion_index, avg.name, avg)
        data.insert(insertion_index + 1, change.name, change)
        data.insert(insertion_index + 2, acc.name, acc)
    return data


def create_data_specific() -> pd.DataFrame:
    headers = []
    rows = []
    row = []
    files = os.listdir("Data/ScivalArticles")
    files.sort(key=lambda x: int(x.split("_", 1)[0]))
    last_inst: int = -1
    for filename in files:
        file_path = os.path.join("Data/ScivalArticles", filename)
        rank = int(filename.split("_")[0]) + 1
        document_type = filename.split("_")[-1].split(".")[0]

        if rank != last_inst:
            last_inst = rank
            if row:
                rows.append(row)
            row = []
        with open(file_path, "r") as file:
            data = json.load(file)
            if last_inst == 1:
                headers.extend(get_headers(data, document_type))
            row.extend(convert_initial_to_row(data, rank, document_specific=True))
    rows.append(row)
    return pd.DataFrame(rows, columns=headers)


def convert_topic_name(topic: dict) -> str:
    return topic["name"].replace("; ", "_").replace(" ", "")


def create_topic_headers() -> List[str]:
    headers = []
    # atts = ["prominencePercentile", "scholarlyOutput", "topicCount", "overallScholarlyOutput"]
    atts = ["scholarlyOutput"]
    files = os.listdir("Data/ScivalTopics")
    files.sort(key=lambda x: int(x.split("_", 1)[0]))
    for filename in files:
        file_path = os.path.join("Data/ScivalTopics", filename)
        with open(file_path, "r") as file:
            data = json.load(file)
            for topic in data["topics"]:
                name = convert_topic_name(topic)
                for att in atts:
                    header_name = f"{name}_{att}"
                    if header_name not in headers:
                        headers.append(header_name)
    return headers


def create_topic_info() -> pd.DataFrame:
    headers = create_topic_headers()
    # atts = ["prominencePercentile", "scholarlyOutput", "topicCount", "overallScholarlyOutput"]
    atts = ["scholarlyOutput"]
    files = os.listdir("Data/ScivalTopics")
    files.sort(key=lambda x: int(x.split("_", 1)[0]))
    df = pd.DataFrame(columns=headers)
    for filename in files:
        file_path = os.path.join("Data/ScivalTopics", filename)
        with open(file_path, "r") as file:
            data = json.load(file)
            serie = pd.Series(index=headers)
            for topic in data["topics"]:
                name = convert_topic_name(topic)
                for att in atts:
                    header_name = f"{name}_{att}"
                    serie[header_name] = topic[att]
            df = df.append(serie, ignore_index=True)
    return df


def write_arff_file(dataset: pd.DataFrame, filename="dataset.arff", name="Universities"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"@RELATION {name}\n\n")
        max_len = len(max(dataset.columns, key=len))
        for header in dataset.columns:
            if dataset[header].dtype == np.float64 or dataset[header].dtype == np.int64:
                column_type = "NUMERIC"
            else:
                column_type = "STRING"

            file.write(f"@ATTRIBUTE {header.ljust(max_len)} {column_type}\n")
        file.write("\n@DATA\n")

        for _, column in dataset.iteritems():
            if column.dtype == np.object:
                pattern = re.compile(r"^(.*)$")
                dataset[column.name] = column.str.replace(pattern, r'"\1"')

        for _, row in dataset.iterrows():
            items = [str(x) for x in row]
            items = [x if x != "nan" else "?" for x in items]
            file.write(f"{', '.join(items)}\n")


def drop_columns_from_before(data: pd.DataFrame) -> pd.DataFrame:
    pattern = re.compile(".*_(2009|2010|2011|2012|2013)")
    columns_to_drop = [x for x in data.columns if pattern.match(x)]
    return data.drop(columns=columns_to_drop)


def main():
    dataset = create_main_dataset()
    dataset = drop_columns_from_before(dataset)
    dataset = expand_data(dataset)

    authors = get_author_info()
    funding = get_funding_info()
    collab_countries = get_country_info()

    document_specific_df = create_data_specific()
    document_specific_df = drop_columns_from_before(document_specific_df)
    document_specific_df = expand_data(document_specific_df)

    topics_dataset = create_topic_info()

    total = pd.concat([dataset, authors, funding, collab_countries, document_specific_df, topics_dataset], axis=1)
    write_arff_file(total, filename="Data/dataset.arff")


if __name__ == '__main__':
    main()
    # fix_csv_names()
