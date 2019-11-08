import re
from typing import Dict, List, Tuple

import pandas as pd


def analyze(df: pd.DataFrame, patterns) -> Dict:
    if len(patterns) < 1:
        return {"count": 0}
    r = {}
    pattern = patterns[0]
    df1 = df.query(pattern)
    df2 = df.query(f"not ({pattern})")
    r1 = analyze(df1, patterns[1:])
    r2 = analyze(df2, patterns[1:])
    r1["count"] = len(df1)
    r2["count"] = len(df2)
    r[pattern] = r1
    r[f"not({pattern})"] = r2
    return r


def convert_pattern(pattern: str) -> List[str]:
    regex = re.compile(r"\s=\s")
    pattern = regex.sub(" == ", pattern)
    pattern = pattern.replace("AND", "^")
    return pattern.split("^")


def get_all_keys(dic: Dict) -> List[str]:
    keys = [x for x in dic.keys() if x != "count"]
    other = []
    for key in keys:
        res = get_all_keys(dic[key])
        other.extend(res)
    keys.extend(other)
    keys = list(dict.fromkeys(keys))
    return keys


def get_sources_and_dest(dic: Dict, labels: List[str], past="") -> Tuple[List, List, List]:
    keys = [x for x in dic.keys() if x != "count"]
    sources = []
    destinations = []
    flows = []

    for key in keys:
        count = dic[key]["count"]
        if past != "" and count != 0:
            sources.append(labels.index(past))
            destinations.append(labels.index(key))
            flows.append(dic[key]["count"])
        dsources, ddests, dflows = get_sources_and_dest(dic[key], labels, key)
        sources.extend(dsources)
        destinations.extend(ddests)
        flows.extend(dflows)

    return sources, destinations, flows


def get_colors_nodes(labels: List[str]) -> List:
    regex = re.compile(r"not\(.*\)")
    base_color = "#333333"
    pattern_color = "#7FC241"
    colors = [base_color for _ in range(len(labels))]
    for i, label in enumerate(labels):
        if not regex.match(label):
            colors[i] = pattern_color
    colors[0] = "#F27420"
    colors[1] = "#4994CE"
    return colors


def get_colors_links(origins: List[str], dests: List[str], labels: List[str]) -> List:
    regex = re.compile(r"not\(.*\)")
    base_color = "#D3D3D3"
    out_color = "#333333"
    pattern_color = "rgba(101, 250, 20, 0.5)"
    colors = [base_color for _ in range(len(origins))]
    saved = []
    for i, tup in enumerate(zip(origins, dests)):
        label_o = labels[tup[0]]
        label_d = labels[tup[1]]
        if not regex.match(label_o) and not regex.match(label_d) and tup not in saved:
            colors[i] = pattern_color
        elif not regex.match(label_o) and regex.match(label_d):
            colors[i] = out_color
        saved.append(tup)
    return colors
