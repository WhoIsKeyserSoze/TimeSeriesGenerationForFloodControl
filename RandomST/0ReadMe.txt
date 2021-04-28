All files here contains a list of river height measures stored under csv format.

```
date,height
```

Measures were took each hour during 3 days and are stored from the most recent to the oldest.
The name of file gives :
- the date when the series of measure started
- the id of the sensor that took them
- a letter representing the classification

for this data classification was done by hand
L stands for Linear
R stands for reccurent pattern
F stands for flood (meaning that there probably is a flood in the data)
N stands for no apparent patterns

Here is a little python code to iterate throught all the file : 

```py
# data_path is a string storing the path to the rep where all data is
for file in os.listdir(data_path):
    if file.endswith(".csv"):

        # store the data in a dataframe
        df = pandas.read_csv(unclassified_data_path + '\\' + file)
```