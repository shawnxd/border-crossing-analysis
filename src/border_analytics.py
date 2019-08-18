# coding: utf-8
# import for packages
import pandas as pd
import decimal

# load dataset from input
file_path = '../input/Border_Crossing_Entry_Data.csv'

# select columns we need for analysis
dataset = pd.read_csv(file_path, header=0, usecols=['Border', 'Date', 'Measure', 'Value'], index_col=False)

# group by ['Date', 'Measure', 'Border'] and calculate the sum of values, update the values for 'Value' column
dataset = dataset.groupby(['Date', 'Measure', 'Border'])['Value'].sum()
dataset = dataset.reset_index(level=['Date', 'Measure', 'Border'])

# sort by ['Measure', 'Border', 'Date'] in ascending order
dataset.sort_values(by=['Measure', 'Border', 'Date'], ascending=[True, True, True], inplace=True)

# function to add column 'Average' to calculate <monthly average values> of different borders & measure
average_lst = []
decimal.getcontext().rounding = "ROUND_HALF_UP"
for i in dataset.groupby(['Measure', 'Border']):
    # get list of Value for different boarder & meature combination
    current_filter = list((i[1]['Value']))
    length = len(current_filter)
    total, count = 0, 0
    for j in range(length):
        if j == 0:
            average_lst.append(0)
        else:
            count += 1
            ans = decimal.Decimal(str(total / count)).quantize(decimal.Decimal("0"))
            average_lst.append(int(ans))
        total += current_filter[j]
dataset['Average'] = average_lst

# sort by ['Date', 'Value', 'Measure', 'Border'] in descending order as required
dataset.sort_values(by=['Date', 'Value', 'Measure', 'Border'], ascending=[False, False, False, False], inplace=True)

# change column order as required
dataset = dataset[['Border', 'Date', 'Measure', 'Value', 'Average']]

# export dataset to csv file in output folder
dataset.to_csv("../output/report.csv", index=False)
