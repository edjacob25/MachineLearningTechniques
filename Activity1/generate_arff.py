import json
import numpy as np
import os
import re
import pandas as pd
from common import camel_case_to_snake_case
from typing import List


def convert_initial_to_row(data: dict, rank: int) -> List:
    row = [rank, data["name"], data["country"]]
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


def get_headers(data: dict) -> List[str]:
    headers = ["rank", "name", "country"]
    for metric in data["metrics"]:
        metric_name = camel_case_to_snake_case(metric["metricType"])
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
                    parts = metric_name.rsplit('_', 2)
                    composed_name = f"{parts[0]}_{threshold}percent_{parts[1]}"
                headers.extend(get_header_by_year(composed_name, value))
            # headers.extend(get_header_by_year(composed_name, value, percentage=True))

    return headers


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
        file.write("\n@Data\n")

        for _, row in dataset.iterrows():
            items = [str(x) for x in row]
            file.write(f"{', '.join(items)}\n")


def main():
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

    dataset = pd.DataFrame(data=rows, columns=headers)

    pattern = re.compile(".*_(2009|2010|2011|2012|2013)")
    columns_to_drop = [x for x in dataset.columns if pattern.match(x)]
    # print(columns_to_drop)
    dataset = dataset.drop(columns=columns_to_drop)

    write_arff_file(dataset)


if __name__ == '__main__':
    main()
