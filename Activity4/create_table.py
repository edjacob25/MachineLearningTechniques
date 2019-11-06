import pandas as pd
from pathlib import Path
from typing import Dict

def analyze(df: pd.DataFrame, patterns) -> Dict: 
    if len(patterns) < 1: 
        return {"children": []}
    r = {}
    pattern = patterns[0] 
    df1 = df.query(pattern) 
    df2 = df.query(f"not ({pattern})") 
    r1 = analyze(df1, patterns[1:])
    r2 = analyze(df2, patterns[1:])
    r1["count"] =  len(df1)
    r2["count"] =  len(df2)
    #r["children"] = [r1, r2]
    #r["name"] = pattern
    r[pattern] = r1
    r[f"not({pattern})"] = r2
    return r


