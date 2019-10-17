from typing import List, Tuple
from pathlib import Path
from sortedcontainers import SortedDict
from argparse import ArgumentParser

def obtain_patterns(path: Path) -> List[Tuple]:
    patterns = []
    with open(path, "r", encoding="UTF8") as file:
        reading_patterns = False
        for line in file.readlines():
            if not reading_patterns:
                if "=== Class" in line:
                    reading_patterns = True
            else:
                if line.strip().endswith("]"):
                    pattern, nums = line.strip().split("[")
                    a, b = nums.replace("]", "").split(" ", 1)
                    patterns.append((pattern, float(a), float(b), float(a) - float(b)))
    return patterns

def main():
    parser = ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()
    directory = Path(args.directory)
    buckets = SortedDict()
    for file in directory.iterdir():
        _, _, bucket = file.stem.split(" ", 2)
        print(f"Getting patterns for file {file}")
        patterns = obtain_patterns(file)
        if bucket in buckets:
            buckets[bucket].extend(patterns)
        else:
            buckets[bucket] = patterns

    with open("Results", "w") as file:
        for bucket in buckets:
            patterns = buckets[bucket]
            patterns = list(dict.fromkeys(patterns))
            patterns.sort(key=lambda x: x[3], reverse=True)
            print(f"The 4 best patterns for bucket {bucket} are:")
            file.write(f"{bucket}\n")
            for i in range(4):
                p = [str(x) for x in patterns[i]]
                file.write(f"{','.join(p)}\n")
                print(patterns[i])
            file.write("\n")

if __name__ == "__main__":
    main()