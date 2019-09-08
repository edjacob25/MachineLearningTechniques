import json
import os
import re
from typing import List

import numpy as np
import pandas as pd

from common import camel_case_to_snake_case


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
                    # print(metric_name)
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
                # print(headers)
                # print(len(headers))
            row = convert_initial_to_row(data, rank)
            # print(row)
            # print(len(row))

        rows.append(row)

    return pd.DataFrame(data=rows, columns=headers)


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

        for _, row in dataset.iterrows():
            items = [str(x) for x in row]
            file.write(f"{', '.join(items)}\n")


def main():
    dataset = create_main_dataset()
    print(dataset)

    new_dataset = create_data_specific()
    print(new_dataset)

    total = pd.concat([dataset, new_dataset], axis=1)
    print(total)

    pattern = re.compile(".*_(2009|2010|2011|2012|2013)")
    columns_to_drop = [x for x in total.columns if pattern.match(x)]
    # print(columns_to_drop)
    total = total.drop(columns=columns_to_drop)
    print(total)
    write_arff_file(total)


if __name__ == '__main__':
    main()
