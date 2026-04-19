import csv
# Import the built-in CSV module.
# Used for safely reading and writing CSV formatted files.
# Alternatives you might see: pandas, json, database connectors.
from pathlib import Path
HOME_DIR = Path(__file__).parent.resolve()      #THis goes to the PARENT FOLDER of the file or python script we are running right now
INPUT_PATH = HOME_DIR / "CSVs" / "INPUT.csv"
OUTPUT_DIR = HOME_DIR.parent / "OUTPUTFOLDER"       #<- OR you can just do it like this: OUTPUT_DIR = HOME_DIR / ".." / "OUTPUTFOLDER"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "output.txt"     #The output


results = []
# A Python LIST used to store processed rows.
# This is where cleaned/transformed data goes before writing.
# You could also store:
#   dictionaries (most common with DictWriter)
#   lists (common with csv.writer)
#   filtered rows only
#   transformed rows


# 1️⃣ READ
with open(INPUT_PATH, newline="") as f:
# Opens the CSV file.
# newline="" allows the CSV module to control newline handling.
# If omitted, Windows CSV files can produce blank rows.


    reader = csv.DictReader(f)
    # Creates a CSV reader that converts rows into dictionaries.
    # Example row returned:
    # {'column1':'value1','column2':'value2'}
    #
    # Optional things you can configure:
    # delimiter="|"        (pipe-delimited files)
    # delimiter="\t"       (tab files)
    # quotechar='"'
    #
    # Example:
    # reader = csv.DictReader(f, delimiter="|")


    # 2️⃣ PROCESS
    for row in reader:
    # Loop through each row of the CSV.
    # Each iteration gives a dictionary.
    #
    # Example:
    # row = {'column1':'John','column2':'Sales'}


        # clean / transform values
        new_row = {
            "column1": row["column1"],
            "column2": row["column2"]
        }
        # This creates a NEW dictionary representing the cleaned row.
        # You can transform data here.
        #
        # Examples:
        #
        # Remove whitespace
        # "column1": row["column1"].strip()
        #
        # Standardize casing
        # "column2": row["column2"].upper()
        #
        # Replace characters
        # row["price"].replace("$","")
        #
        # Skip rows
        # if row["column1"] == "":
        #     continue
        #
        # Rename columns
        # "employee_id": row["emp_id"]


        # 3️⃣ STORE
        results.append(new_row)
        # Adds the cleaned row to the results list.
        #
        # This allows you to:
        # filter rows
        # count rows
        # inspect rows before writing
        #
        # Example stored data:
        #
        # results = [
        #   {'column1':'John','column2':'Sales'},
        #   {'column1':'Jane','column2':'HR'}
        # ]


# 4️⃣ WRITE
with open(OUTPUT_PATH, "w", newline="") as f:
# Opens a new file for writing.
# "w" overwrites the file each run.
#
# Other modes:
# "a" append to file
# "x" create file only if it doesn't exist


    writer = csv.DictWriter(f, fieldnames=["column1","column2"])
    # Creates a CSV writer that expects dictionaries.
    #
    # fieldnames define:
    # - column order
    # - column names written to the header
    #
    # You can also change delimiters:
    #
    # writer = csv.DictWriter(
    #     f,
    #     fieldnames=["column1","column2"],
    #     delimiter="|"
    # )


    writer.writeheader()
    # Writes the column names as the first row of the CSV.
    #
    # Output example:
    #
    # column1,column2


    writer.writerows(results)
    # Writes ALL rows stored in the results list.
    #
    # Equivalent to:
    #
    # for row in results:
    #     writer.writerow(row)
for r in results:
    print(f"{r['id']}|{r['name']}|{r['department']}")