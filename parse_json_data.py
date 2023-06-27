import unicodedata
import re
from pathlib import Path
from tqdm import tqdm
import json


def parse_convos(file_path: Path) -> None:
    with open(file_path, "r", encoding="utf-8-sig") as data_file:
        data = data_file.read()

    data_json = json.loads(data)
    data_json_dumped = json.dumps(data_json, indent=2)
    ##print(data_json_dumped)

    training_data_file = open("Data\\training_data.txt", "a")

    for item in data_json:
        if item.get("event") is None:
            if item.get("text") is not None:
                output_str: str = (
                    unicodedata.normalize("NFKD", item.get("text")).encode(
                        "ascii", "ignore"
                    )
                ).decode()
                output_str: str = re.sub(r"http\S+", "", output_str)
                output_str: str = re.sub(r"\\n", "", output_str)
                output_str: str = re.sub(r"\\\'", "'", output_str)
                output_str: str = re.sub(r"\\\\", str(r"\\"), output_str)

                output_str = output_str.strip()
                output_str: str = output_str + "\n"

                if len(output_str) > 1:
                    training_data_file.write(f"{output_str}")

    training_data_file.close()

    return


FILE_PATHS: list = [
    "Data\\4-27-23 Data\\2021 Opening Week group 27\\message.json",
    "Data\\4-27-23 Data\\Beta Sig Comp Sci Comp E's\\message.json",
    "Data\\4-27-23 Data\\Constitution Committee\\message.json",
    "Data\\4-27-23 Data\\Eta Chapter History Committee\\message.json",
    "Data\\4-27-23 Data\\File Committee\\message.json",
    "Data\\4-27-23 Data\\Jack Daniel's Family\\message.json",
    "Data\\4-27-23 Data\\Membership\\message.json",
    "Data\\4-27-23 Data\\PC 21 Kum Gaurd\\message.json",
    "Data\\4-27-23 Data\\PC 21 The Union\\message.json",
    "Data\\4-27-23 Data\\PC 21 v3\\message.json",
    "Data\\4-27-23 Data\\PC_21_GC\\message.json",
    "Data\\4-27-23 Data\\PC21 Gains\\message.json",
    "Data\\4-27-23 Data\\PC22 Big Brothers\\message.json",
    "Data\\4-27-23 Data\\Rajun Cajun\\message.json",
    "Data\\4-27-23 Data\\Spring '22 E-Board\\message.json",
    "Data\\4-27-23 Data\\THEOG_CHAT\\message.json",
    "Data\\4-27-23 Data\\Those Eta Bois XVI\\message.json",
    "Data\\4-27-23 Data\\Weekend Group 5\\message.json",
    "Data\\4-27-23 Data\\Yard Committee Fall 2021\\message.json",
]

for file_path in tqdm(FILE_PATHS, desc="Parsing json's"):
    parse_convos(file_path)


"""old paths
    'Data\Eta_Chapter_History_Committee\message.json',
    'Data\File_Committee\message.json',
    'Data\Jack_Daniels_Family\message.json',
    'Data\PC_21_GC\message.json',
    'Data\PC_21_Kum_Guard\message.json',
    'Data\PC_21_v3\message.json',
    'Data\PC21_Gains\message.json',
    'Data\PC22_Big_Brothers\message.json',
    'Data\Rajun_Cajun\message.json',
    'Data\Spring_22_E-Board\message.json',
    'Data\THEOG_CHAR\message.json',
    'Data\Those_Eta_Bois_XVI\message.json',
    'Data\Weekend_Group_5\message.json',
    'Data\Yard_Committee_Fall_2021\message.json',
"""
