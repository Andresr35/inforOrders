import pandas as pd
import json

class csvUtils:
    def readCSV(csvInput):
        rawCSV =pd.read_csv(csvInput)
        # print(rawCSV.columns)
        # print(rawCSV[["Name","whatever"]][0:5]) or rawCSV.Name
        # print(rawCSV.iloc[0:4]) gets specific rows
        # print(rawCSV.iloc[2,1]) gets a value at a column in a row (R,C)

        # print(rawCSV.loc[rawCSV['Name'] == "FB38486"]) looking for specific values in the data
        # rawCSV["andresTest"] = "test worked" adding in new keys and values
        # rawCSV = rawCSV.drop(columns=['Name '])
        newDict = {}

        for index, row in rawCSV.iterrows(): #gets all rows and just the names with their index

            if('order' not in locals()):
                print("first index")
                newDict.update({
                    row["Name"]:{
                    'shippingname':row["Shipping Name"],
                    'shippingStreet':row["Shipping Street"],
                    'shippingCity':row["Shipping City"],
                    'shippingZip':row["Shipping Zip"],
                    'shippingState':row["Shipping Province"],
                    'shippingCountry':row["Shipping Country"],
                    'shippingAmount':row["Shipping"],
                    'discount':row["Discount Amount"],
                    'lineItems':[{
                        'sku':row["Lineitem sku"],
                        'price':row["Lineitem price"],
                        'quantity':row["Lineitem quantity"]
                    }]
                }})
            elif(row["Name"] == order["Name"]):
                x:dict = newDict.get(row["Name"])
                y:list=x.get('lineItems')
                y.append(
                    {
                        'sku':row["Lineitem sku"],
                        'price':row["Lineitem price"],
                        'quantity':row["Lineitem quantity"]
                    })






            else:
                 newDict.update({row["Name"]:{
                    'shippingname':row["Shipping Name"],
                    'shippingStreet':row["Shipping Street"],
                    'shippingCity':row["Shipping City"],
                    'shippingZip':row["Shipping Zip"],
                    'shippingState':row["Shipping Province"],
                    'shippingCountry':row["Shipping Country"],
                    'shippingAmount':row["Shipping"],
                    'discount':row["Discount Amount"],
                    'lineItems':[{
                        'sku':row["Lineitem sku"],
                        'price':row["Lineitem price"],
                        'quantity':row["Lineitem quantity"]
                    }]
                }})
            # print(index,row["Name"])
            # rawCSV.iloc[index,1]
            order = row
        print(json.dumps(newDict,indent=4,sort_keys=True))
        finalCSV = rawCSV[["Name","Lineitem quantity","Lineitem price","Lineitem sku","Shipping Name","Shipping Street","Shipping City","Shipping Zip","Shipping Province","Shipping Country","Shipping","Discount Amount"]]
        return finalCSV
    