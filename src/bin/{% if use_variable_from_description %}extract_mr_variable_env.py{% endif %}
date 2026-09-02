#!/usr/bin/env python3
import json
import os

# pylint: disable=print-used


description = os.getenv("CI_MERGE_REQUEST_DESCRIPTION")
with open("mr_variable.sh", "w") as f:
    if description and "# Variable" in description:
        data = description.split("#Variable")[-1].split("```")[1]
        try:
            data = json.loads(data)
        except Exception as e:
            raise Exception(f"Fail to read the json data are \n {data} \n error: {e}")
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # pass complex variable as a string in json
                value = json.dumps(value)
            f.writelines(f"export {key.upper()}='{value}'\n")
    else:
        print("Extract MR variable: No variable found or invalid description")
