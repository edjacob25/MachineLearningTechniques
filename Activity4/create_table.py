import re
from typing import Dict, List, Tuple

import pandas as pd


def analyze_initial(df: pd.DataFrame, patterns, support: str, class_str, class_list: List[str] = None):
    r = {}
    supports = [float(x) for x in support.replace("[", "").replace("]", "").split(" ")]

    classes = df[class_str].unique().tolist()
    if class_list:
        classes = class_list
    for i, item in enumerate(classes):
        has_support = supports[i] > 0.0
        pattern = f"{class_str} == '{item}'"
        partition = df.query(pattern)
        subtree = analyze(partition, patterns, parent_ok=has_support)
        subtree["count"] = len(subtree)
        subtree["true_route"] = has_support
        r[pattern] = subtree
    return r


def analyze(df: pd.DataFrame, patterns: List[str], parent_ok=False) -> Dict:
    if len(patterns) < 1:
        if parent_ok:
            return {"count": 0, "true_route": True}
        return {"count": 0}
    r = {}
    pattern = patterns[0]
    df1 = df.query(pattern)
    df2 = df.query(f"not ({pattern})")
    r1 = analyze(df1, patterns[1:], parent_ok=parent_ok)
    r2 = analyze(df2, patterns[1:])
    if parent_ok:
        r["true_route"] = True
    r1["count"] = len(df1)
    r2["count"] = len(df2)
    r[pattern] = r1
    r[f"not({pattern})"] = r2
    return r


def convert_pattern(pattern: str) -> List[str]:
    regex = re.compile(r"\s=\s")
    pattern = regex.sub(" == ", pattern)
    pattern = pattern.replace("AND", "^")
    support_regex = re.compile(r"(\[.*\])")
    support = support_regex.search(pattern)
    if support:
        pattern = pattern.replace(support.group(1), "")
    patterns = pattern.split("^")

    back_regex = re.compile("([!=><]{1,2})")
    for i, pattern in enumerate(patterns):
        m = back_regex.search(pattern)
        column, value = pattern.split(m.group(1))
        if "-" in column:
            column = column.replace("-", " ")
            column = f"`{column.strip()}`"
            patterns[i] = f"{column} {m.group(1)} {value}"
    patterns = [x.replace("-", " ") for x in patterns]
    if support:
        patterns.append(support.group(1))

    return patterns


def get_all_keys(dic: Dict) -> List[str]:
    keys = [x for x in dic.keys() if x != "count" and x != "true_route"]
    other = []
    for key in keys:
        res = get_all_keys(dic[key])
        other.extend(res)
    keys.extend(other)
    keys = list(dict.fromkeys(keys))
    return keys


def get_sources_and_dest(dic: Dict, labels: List[str], past="") -> Tuple[List, List, List, List]:
    keys = [x for x in dic.keys() if x != "count" and x != "true_route"]
    sources = []
    destinations = []
    flows = []
    ways = []
    for key in keys:
        count = dic[key]["count"]
        if past != "" and count != 0:
            sources.append(labels.index(past))
            destinations.append(labels.index(key))
            flows.append(dic[key]["count"])
            ways.append("true_route" in dic[key])
        dsources, ddests, dflows, dways = get_sources_and_dest(dic[key], labels, key)
        sources.extend(dsources)
        destinations.extend(ddests)
        flows.extend(dflows)
        ways.extend(dways)

    return sources, destinations, flows, ways


def get_colors_nodes(labels: List[str], size=0) -> List:
    class_colors = ["#de639a", "#00a7e1", "#f7c59f", "#767b91", "#007ea7"]
    regex = re.compile(r"not\(.*\)")
    base_color = "#333333"
    pattern_color = "#7FC241"
    colors = [base_color for _ in range(len(labels))]
    for i, label in enumerate(labels):
        if not regex.match(label):
            colors[i] = pattern_color

    colors[0] = "#F27420"
    colors[1] = "#4994CE"
    if size > 0:
        for i in range(size):
            colors[i] = class_colors[i % 5]

    return colors


def get_colors_links(origins: List[str], dests: List[str], labels: List[str], ways: List[bool]) -> List:
    regex = re.compile(r"not\(.*\)")
    base_color = "#D3D3D3"
    out_color = "#333333"
    pattern_color = "rgba(101, 250, 20, 0.5)"
    colors = [base_color for _ in range(len(origins))]
    saved = []
    for i, tup in enumerate(zip(origins, dests)):
        label_o = labels[tup[0]]
        label_d = labels[tup[1]]
        if ways[i]:
            colors[i] = pattern_color
        elif not regex.match(label_o) and regex.match(label_d):
            colors[i] = out_color
        saved.append(tup)
    return colors
