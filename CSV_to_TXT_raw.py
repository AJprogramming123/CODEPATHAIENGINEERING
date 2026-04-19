import csv
# CSV module is used ONLY for reading structured CSV files safely.

from pathlib import Path


############################
# PATH SETUP
############################

HOME_DIR = Path(__file__).parent.resolve()
# __file__ is the current script file path
# .parent gets the folder containing this script
# .resolve() converts it to an absolute path

INPUT_PATH = HOME_DIR / "CSVs" / "INPUT.csv"
# Path to the input CSV file

OUTPUT_DIR = HOME_DIR / "OUTPUTFOLDER"
# Folder where output will be written

OUTPUT_DIR.mkdir(exist_ok=True)
# Creates folder if it doesn't exist
# If it already exists, Python does nothing

OUTPUT_PATH = OUTPUT_DIR / "output.txt"
# Final TXT file path


############################
# STORAGE
############################

results = []
# Python LIST used to store processed rows.
#
# For TXT exports we usually store LISTS instead of dictionaries.
#
# Example:
# results = [
#   ["101","John Smith","SALES"],
#   ["102","Jane Doe","HR"]
# ]


############################
# 1️⃣ READ CSV
############################

with open(INPUT_PATH, newline="") as f:
# Opens the CSV file
# newline="" lets the csv module manage newline characters correctly

    reader = csv.DictReader(f)
    # Reads rows as dictionaries using the CSV header row
    #
    # Example row:
    # {'id':'101','name':'John Smith','department':'Sales'}

    for row in reader:
    # Loop through every row in the CSV file


        ############################
        # 2️⃣ PROCESS / CLEAN DATA
        ############################

        new_row = [
            row["id"],
            row["name"].strip(),
            row["department"].upper()
        ]

        # Build a LIST representing the new row.
        #
        # We choose LIST here because we will manually format
        # the output with join().
        #
        # Common transformations done here:
        #
        # Remove whitespace
        # row["name"].strip()
        #
        # Convert case
        # row["department"].upper()
        #
        # Replace characters
        # row["price"].replace("$","")
        #
        # Skip rows
        # if row["name"] == "":
        #     continue


        ############################
        # 3️⃣ STORE RESULT
        ############################

        results.append(new_row)
        # Adds cleaned row to results list


############################
# 4️⃣ WRITE TXT FILE
############################

with open(OUTPUT_PATH, "w") as f:
# Opens TXT file for writing
#
# "w" overwrites file each run

    for row in results:
    # Loop through stored rows


        line = "|".join(row.values())
        # join() converts a list into a string
        #
        # Example row:
        # ["101","John Smith","SALES"]
        #
        # "|".join(row) becomes:
        #
        # "101|John Smith|SALES"
        #
        # You can change the delimiter easily:
        #
        # ",".join(row)
        # ";".join(row)
        # "\t".join(row)
        # " - ".join(row)


        f.write(line + "\n")
        # Writes line to the TXT file
        #
        # "\n" creates a new line after each row


############################
# FINAL OUTPUT EXAMPLE
############################

# 101|John Smith|SALES
# 102|Jane Doe|HR
# 103|Mike Brown|ENGINEERING

#How to print it:
for r in results:
    print("|".join(r.values())) 