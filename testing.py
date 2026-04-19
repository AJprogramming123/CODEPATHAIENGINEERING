'''
What is 'self'
"This specific object:"
It lets Python know which created object you are talking about
'processor = CSVProcessor(input_file, output_file)'

Next, the constructor:
'It runs automatically when you create an object'
def __init__(self, input_path: Path, output_path: Path) -> None:
    self.input_path = input_path
    self.output_path = output_path

so its (self=processor, input_path, output_path)
what does processor mean?
When you create a object in the class the self parameter receives the object that called it
so for example
'def process(self): ' 

so in the def main() somebody would call
my_dog = CSVProcessor(input_path, output_path)
my_dog.process()

Next the read_csv:
'def read_csv(self) -> tuple[list[dict[str, str]], list[str]]:'
This method uses 'self' and returns two things
1.) a list of row dictionaries
2.) a list of field names

The -> part (Return Type Hint)
This part isnt how the code runs its just a promise of what the function returns
tuple[...] - The function returns multiple values grouped together
    A tuple = a fixed group of values

the first Item: 'list[dict[str, str]]
    A list[multiple items] or from what we know a list is this -> [...] one giant list that has multiple items
    
    dict[str, str]
    - Each item in the list is a dictionary where:
        - Keys are strings
        - Values are strings
    
*Basically to summarize its a list, and inside that list are dictionaries*

Why not just a dictionary?
dict[str, str]
row = {
    "id": "101",
    "name": "John"
}

That is 1 row only, but csv files have many rows

rows = [
    {"id": "101", "name": "John"},
    {"id": "102", "name": "Jane"},
    {"id": "103", "name": "Mike"}
]

The basics of a dictionary - A way to store data using labels(keys) instead of positions

Ok but the csvs are just commas separate values, each line is a row
What Python turns it into:
    - What you use something like 'csv.DictReader', Python interprets that text and converts it into something easier to work with:

If we use .read() instead
A CSV file is just plain text where each line is a row and commas separate values,
but Python can turn that raw text into structured data. If you use .read(), you only get one big
string and have to manually split it into lines and columns yourself. Using csv.reader() improves this by giving you rows as lists
(like ["101", "John"] ), but you still have to remember what each position means. The most useful option is csv.DictReader() , which converts each row into a dictionary like {"id", "101", "name": "John"}, where keys are column names and values are the data.

So when you do:
'rows, fieldnames = self.read_csv()

So how does it know to use the input_path and not the output_path:
look at 'self' in the __init__:
    self = {
        "input_path": Path("input.csv"),
        "output_path": Path("output.csv")
    }

now self contains both constantly..so every object will have it
def read_csv(self):
    with self.input_pth.open(...) as f:

Awesome now the rest of the code:

'''

import csv
from pathlib import Path


class CSVProcessor:
    def __init__(self, input_path: Path, output_path: Path) -> None:
        self.input_path = input_path
        self.output_path = output_path

###############################################################################

    def read_csv(self) -> tuple[list[dict[str, str]], list[str]]:
        with self.input_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f) #Creates the CSV reader "Take this file and read it as a CSV with column names"
            #What reader actually gives you
            # for row in reader:
            #   print(row)
            #{"id": "101", "name": "John"}
            #{"id": "102", "name": "Jane"}
            #
            rows = list(reader) #This is equivalent to appending and looping through all the rows collecting them into a list
            # It becomes:
            #    [
            #        {"id": "101", "name": "John"},
            #        {"id": "102", "name": "Jane"}
            #    ]
'''
what does list(reader) do it stores everything into 1 LIST including keys and values every single row

'''

            fieldnames = reader.fieldnames[:] if reader.fieldnames else []
            #List splicing [:] "Give me everything in the list"
            #- reader.filenames = original list (like a master document)
            #- [:] = "Make me a photocopy"
'''
Heres proof of function:
lets say we had
a = ["id", "name"]
b = a
*a and b point to the same list*

if we do:
    b.append("age")
    print(a)

It will turn to:
["id", "name", "age"]
a changed because a and b are the same objeect in memory

So we use : "slicing"   -> give me a portion of this sequence (list, string, etc.)

remember: 'somthing[start:end]'

Next, where does fieldnames come from, its a real attribute (built-in variable) that belongs to csv.DictReader objects only.


'''     
        return rows, fieldnames

    def build_full_label(self, row: dict[str, str]) -> str:
        return f"{row['id']} - {row['name']}"

    def transform_row(self, row: dict[str, str]) -> dict[str, str]:
        row["full_label"] = self.build_full_label(row)
        return row

    def ensure_column(self, fieldnames: list[str], column_name: str) -> list[str]:
        if column_name not in fieldnames:
            fieldnames.append(column_name)
        return fieldnames

    def write_csv(self, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
        with self.output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

###############################################################################

    def process(self) -> None:
        rows, fieldnames = self.read_csv() #These two variables are NOT the same as in DictReader
        fieldnames = self.ensure_column(fieldnames, "full_label")

        transformed_rows = []
        for row in rows:
            new_row = self.transform_row(row)
            transformed_rows.append(new_row)

        self.write_csv(transformed_rows, fieldnames)





'''
Scenario Questions Fixes:
reader = csv.DictReader(f) -> "Prepares to read rows one at a time"
next(reader) -> "grabs the FIRST row only
next() means: "give me the next item from something you can loop through
    - Each time you call next(it), you get the next value

nums = [10, 20, 30]

it = iter(nums)

print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30

just like a actual list you can loop through, Anything you can use in a 'for' loop -> you can use next() on.
Very common use case in reader()
reader = csv.reader(f)

header = next(reader)  # skip header row

for row in reader:
    print(row)

    
'''
