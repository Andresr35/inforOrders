import pandas as pd

class csvUtils:
    def readCSV(csvInput):
        rawCSV =pd.read_csv(csvInput)
        # print(rawCSV.columns)
        # print(rawCSV[["Name","whatever"]][0:5]) or rawCSV.Name
        # print(rawCSV.iloc[0:4]) gets specific rows
        # print(rawCSV.iloc[2,1]) gets a value at a column in a row (R,C)
        # for index, row in rawCSV.iterrows(): gets all rows and just the names with their index
        #     print(index,row["Name"])
        # print(rawCSV.loc[rawCSV['Name'] == "FB38486"]) looking for specific values in the data
        # rawCSV["andresTest"] = "test worked" adding in new keys and values
        # rawCSV = rawCSV.drop(columns=['Name '])
        finalCSV = rawCSV[["Name","Lineitem quantity","Lineitem price","Lineitem sku","Shipping Name","Shipping Street","Shipping City","Shipping Zip","Shipping Province","Shipping Country"]]
        return finalCSV
    