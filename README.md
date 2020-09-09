# python-csv-comparator

A Python script for comparing two .csv files and returning the differences found.

## Installation

Make sure that [Python](https://www.python.org/downloads/) is installed on your machine.

To install the required Python libraries, use this command in the project folder:

```bash
pip install -r requirements.txt
```

## Usage
### Script arguments

#### Required
* **--file1 or -1**: Path of the first file you want to compare
* **--file2 or -2**: Path of the second file you want to compare

#### Not required
* **--delimiter or -d**: Character used to delimit columns in both files *(default = ",")*
* **--keys or -k**: Columns delimited by commas you want to  use as keys for the comparison. If empty, the script will compare the two files line by line. In this case, the two files must be properly sorted *(default = "")*
* **--output or -o**: Path of the output file where the differences will be exported *(default = "output.csv")*
* **--exclude or -e**: Columns delimited by commas you want to exclude of the comparison *(default = "")*
* **--chunk or -c**: Number of lines processed at a time *(default = None)*

### Basic usage

This following script execution will compare the two .csv files (```path/to/first/file.csv``` and ```path/to/second/file.csv```) line by line and export the differences found in the output file (```path/to/output/output.csv```). The two .csv files are using the ```;``` delimiter.

```python
python compare.py -1 "path/to/first/file.csv" -2 "path/to/second/file.csv" -o "path/to/output/file.csv" -d ";"
```

### Advanced usage

#### Specifying comparison keys
By default, the script compares the two files line by line. Because of that, **the two .csv files must be ordered properly before comparison**. With the ```-k``` argument, you can give column names (delimited by commas), and the script will use these columns as keys for the comparison. That way, you don't have to order your files before using the script.

Example with a column ```id``` used as a key:

```python
python compare.py -1 "path/to/first/file.csv" -2 "path/to/second/file.csv" -o "path/to/output/file.csv" -d ";" -k "id"
```

Example with two columns ```id``` and ```num``` used as keys:

```python
python compare.py -1 "path/to/first/file.csv" -2 "path/to/second/file.csv" -o "path/to/output/file.csv" -d ";" -k "id,num"
```

#### Exclude columns from the comparison
If you want to exclude specific columns from the comparison, you can use the ```-e``` argument. Just give the name of the columns (delimited by commas) you want to exclude.

Example with the columns ```name``` and ```product``` excluded from the comparison:

```python
python compare.py -1 "path/to/first/file.csv" -2 "path/to/second/file.csv" -o "path/to/output/file.csv" -d ";" -e "name,product"
```

#### Specifying the max number of lines to compare at a time
The script loads the two files to compare in your computer RAM. If you don't have a powerful computer or if the two files are too big to be loaded at once, you can specify the ```-c``` argument. Just give the maximum number of lines you can load at once and the script will chunk the two files using this value.

In this example, the script will compare the two files 10000 lines at a time:

```python
python compare.py -1 "path/to/first/file.csv" -2 "path/to/second/file.csv" -o "path/to/output/file.csv" -d ";" -c 10000
```

## Author

[**Antoine DE WILDE**](https://github.com/AntoineDW) - adewilde@treez-data.fr