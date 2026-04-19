import xml.etree.ElementTree as ET
# Import the built-in XML parsing module.
# Used for reading and navigating XML files.
#
# Common things you'll use most:
# ET.parse()        -> read XML file
# tree.getroot()    -> get the top/root tag
# .findall()        -> find all matching record elements
# .findtext()       -> safely get text from a child tag

import csv
# Import the built-in CSV module.
# Used for safely writing CSV output files.
# You only need this if your final output is CSV.

from pathlib import Path
# Import Path for safe file and folder handling.
# Better than manually typing long path strings.

HOME_DIR = Path(__file__).parent.resolve()
# Folder where the current Python script lives.

INPUT_PATH = HOME_DIR / "XMLs" / "input.xml"
# Input XML file path.

OUTPUT_DIR = HOME_DIR.parent / "OUTPUTFOLDER"
# Output folder path.
# .parent means "go one folder up"

OUTPUT_DIR.mkdir(exist_ok=True)
# Create OUTPUTFOLDER if it doesn't exist yet.
# exist_ok=True prevents an error if the folder already exists.

TXT_OUTPUT_PATH = OUTPUT_DIR / "output.txt"
# Output TXT file path.

CSV_OUTPUT_PATH = OUTPUT_DIR / "output.csv"
# Output CSV file path.

HEADER_OUTPUT_PATH = OUTPUT_DIR / "header.csv"
# Optional separate header-only CSV file path.


results = []
# A Python LIST used to store processed records.
# This is where cleaned/transformed XML data goes before writing.
#
# Most common structure:
# results = [
#   {"id": "101", "name": "John Smith", "department": "SALES"},
#   {"id": "102", "name": "Jane Doe", "department": "HR"}
# ]


# 1️⃣ PARSE XML
tree = ET.parse(INPUT_PATH)
# Reads the XML file and builds an ElementTree object.

root = tree.getroot()
# Gets the root/top XML element.
#
# Example XML:
# <data>
#     <employee>...</employee>
# </data>
#
# root would be:
# <data>


# 2️⃣ FIND RECORDS
for employee in root.findall(".//employee"):
    # Loop through each matching record element.
    #
    # ".//employee" means:
    # start from root
    # search all levels below
    # find every <employee> tag
    #
    # This is the XML version of:
    # for row in reader:
    #
    # "employee" is your repeating record element.


    # 3️⃣ EXTRACT VALUES
    emp_id = employee.findtext("id", "").strip()
    name = employee.findtext("name", "").strip()
    department = employee.findtext("department", "").strip()
    # .findtext("tag", "") safely gets the text inside a child tag.
    #
    # Example:
    # <name> John Smith </name>
    # becomes:
    # " John Smith "
    #
    # then .strip() removes spaces from the left and right:
    # "John Smith"
    #
    # Why use findtext() instead of find().text?
    # Because if the tag is missing:
    # employee.find("name") -> None
    # None.text -> crash
    #
    # But:
    # employee.findtext("name", "")
    # safely returns ""


    # 4️⃣ VALIDATE / SKIP BAD RECORDS
    if name == "" or department == "":
        continue
    # Skip record if required values are missing.
    #
    # continue means:
    # stop this loop iteration immediately
    # jump to the next <employee>
    #
    # Common validation examples:
    #
    # Skip if ID missing
    # if emp_id == "":
    #     continue
    #
    # Skip if ID not numeric
    # if not emp_id.isdigit():
    #     continue
    #
    # Skip if department invalid
    # valid_departments = ["SALES", "HR", "ENGINEERING"]
    # if department.upper() not in valid_departments:
    #     continue


    # 5️⃣ TRANSFORM / CLEAN DATA
    department = department.upper()
    # Standardize department casing.
    #
    # Example:
    # sales -> SALES
    # hr -> HR

    new_row = {
        "id": emp_id,
        "name": name,
        "department": department
    }
    # Create a NEW dictionary representing the cleaned XML record.
    #
    # This is the XML equivalent of building new_row from a CSV row.
    #
    # You can do more transformations here:
    #
    # "name": name.title()
    # "department": department.replace("&", "AND")
    # "employee_id": emp_id
    #
    # You can also rename fields:
    # "employee_id": employee.findtext("id", "").strip()


    # 6️⃣ STORE
    results.append(new_row)
    # Add the cleaned record to the results list.
    #
    # This allows you to:
    # inspect data before writing
    # count valid records
    # write TXT / CSV / JSON later
    # reuse the same processed data in multiple outputs


# 7️⃣ WRITE TO TXT
with TXT_OUTPUT_PATH.open("w") as f:
    # Open TXT output file for writing.
    #
    # "w" overwrites the file each run.
    # Other modes:
    # "a" append
    # "x" create only if it doesn't exist

    for row in results:
        line = "|".join([row["id"], row["name"], row["department"]])
        # Join the row values into one pipe-delimited line.
        #
        # Example:
        # ["101", "John Smith", "SALES"]
        # becomes:
        # 101|John Smith|SALES

        f.write(line + "\n")
        # Write line to the TXT file, then move to the next line.


# 8️⃣ WRITE TO CSV (single file with header)
with CSV_OUTPUT_PATH.open("w", newline="") as f:
    # newline="" lets csv module handle line endings correctly.
    # Prevents blank rows on some systems.

    writer = csv.DictWriter(f, fieldnames=["id", "name", "department"])
    # DictWriter expects dictionaries.
    #
    # fieldnames define:
    # - output column names
    # - output column order

    writer.writeheader()
    # Writes:
    # id,name,department

    writer.writerows(results)
    # Writes all dictionaries from results into the CSV.
    #
    # Equivalent to:
    # for row in results:
    #     writer.writerow(row)


# 9️⃣ OPTIONAL: WRITE SEPARATE HEADER FILE
with HEADER_OUTPUT_PATH.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "department"])
    # Writes only one header row into a separate file.
    #
    # Output:
    # id,name,department


# 🔟 PRINT FOR DEBUGGING
for r in results:
    print(f"{r['id']}|{r['name']}|{r['department']}")
# Print processed results to terminal for debugging.
# Good for checking your script before opening output files.