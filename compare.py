import pandas as pd
import datacompy
import argparse

# Function that takes two dataframes in parameters, compares them, and returns the differences
def compare_datasets(doc1: pd.DataFrame, doc2: pd.DataFrame, keys: list):
    # Comparing the two given datasets with the datacompy library
    if keys: comparison = datacompy.Compare(doc1, doc2, join_columns = keys, df1_name = "File #1", df2_name = "File #2")
    else: comparison = datacompy.Compare(doc1, doc2, on_index = True, df1_name = "File #1", df2_name = "File #2")

    # Getting the list of columns with unequal values
    unequal_columns = [column for column in comparison.column_stats if column["unequal_cnt"] > 0]

    # Creating the dataframe that will contains the differences
    diff = pd.DataFrame(columns = ["file1", "file2", "column", "line"])

    # For each column with unequal values
    for column in unequal_columns:
        # Getting a list of all the differences in this column
        samples = comparison.sample_mismatch(column["column"], for_display = True, sample_count = 9999999)

        # Formating the differences found
        for i in range(len(keys)): samples = samples.drop(samples.columns[0], axis = 1)
        samples['column'] = samples.columns[0].split(" (")[0]
        samples['line'] = samples.index
        samples.columns = ["file1", "file2", "column", "line"]

        # Adding the differences found to the created dataframe that will be returned
        diff = pd.concat([samples, diff], ignore_index = True)
    
    return diff[["line", "column", "file1", "file2"]], comparison

print("\nStart of the script")
print("Parsing the arguments")

# Initializing the arguments parser
parser = argparse.ArgumentParser()

# Listing all the possible arguments
parser.add_argument("--file1", "-1", help = "Path of the first file you want to compare (.csv file)")
parser.add_argument("--file2", "-2", help = "Path of the second file you want to compare (.csv file)")
parser.add_argument("--delimiter", "-d", help = "Character used to delimit columns in both documents")
parser.add_argument("--keys", "-k", help = "Name of the column(s) used as a key for the comparison")
parser.add_argument("--output", "-o", help = "Path where you want to output the comparison result (.csv file)")
parser.add_argument("--exclude", "-e", help = "Columns to exclude before comparison in both documents (separated by a comma)")
parser.add_argument("--chunk", "-c", help = "Number of lines loaded per chunk")

# Read arguments from the command line
args = parser.parse_args()

# Checking the required arguments
if not args.file1: print("ERROR: Please, enter the first file you want to compare (--file1 or -1)")
if not args.file2: print("ERROR: Please, enter the second file you want to compare (--file2 or -2)")

print("\nFile #1: {}".format(args.file1))
print("File #2: {}".format(args.file2))

# Checking the non required arguments
if args.keys: keys = args.keys.split(",")
else: keys = []

if args.output: output = args.output
else: output = "output.csv"

print("Output: {}".format(output))

if args.delimiter: delimiter = args.delimiter
else: delimiter = ","

print("Delimiter: {}".format(delimiter))

if args.exclude: exclude = args.exclude.split(",")
else: exclude = []

print("Excluded columns: {}".format(exclude))

if args.chunk: chunk = args.chunk
else: chunk = "N/A"

print("Number of lines per chunk: {}".format(chunk))

# If a chunk argument was given
if args.chunk:
    # Reading the documents
    file1 = pd.read_csv(args.file1, sep = delimiter, chunksize = int(chunk))
    file2 = pd.read_csv(args.file2, sep = delimiter, chunksize = int(chunk))
    differences = None
    index = 1

    # For each chunk
    for d1, d2 in zip(file1, file2):
        print("\nProcessing chunk #{} - {} lines".format(index, len(d1)))

        # Exluding the given columns
        for e in exclude:
            print("Excluding the column {}".format(e))
            d1 = d1.drop(e, axis = 1)
            d2 = d2.drop(e, axis = 1)

        # Comparing the two documents
        print("\nComparing the two chunks\n")
        result, comparison = compare_datasets(d1, d2, keys)

        # Adding the result of the chunk comparison to the global result
        if differences is not None: differences = pd.concat([differences, result], ignore_index = True)
        else: differences = result

        index += 1
        print(comparison.report())
# If no chunk argument was given
else:
    # Reading the documents
    print("\nReading the first file")
    file1 = pd.read_csv(args.file1, sep = delimiter)

    print("Reading the second file")
    file2 = pd.read_csv(args.file2, sep = delimiter)

    # Exluding the given columns
    for e in exclude:
        print("Excluding the column {}".format(e))
        file1 = file1.drop(e, axis = 1)
        file2 = file2.drop(e, axis = 1)

    # Comparing the two documents
    print("\nComparing the two documents\n")
    differences, comparison = compare_datasets(file1, file2, keys)

    print(comparison.report())

# Exporting the differences in a .csv file
print("Exporting the differences")
differences.to_csv(output, index = False)

print("End of the script")