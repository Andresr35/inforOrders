import pandas as pd

class csvUtils:

    
    def readCSV(csvInput):

        rawCSV =pd.read_csv(csvInput)
        newDict = {}
        for index,row in rawCSV.iterrows(): #gets all rows and just the names with their index

            if('order' not in locals()):
                newDict.update({
                    row['Name']:{
                    'shippingName':row["Shipping Name"],
                    'shippingStreet':row["Shipping Street"],
                    'shippingCity':row["Shipping City"],
                    'shippingZip':row["Shipping Zip"].replace("'",""),
                    'shippingState':row["Shipping Province"],
                    'shippingCountry':row["Shipping Country"],
                    'shippingAmount':row["Shipping"],
                    'discount':row["Discount Amount"],
                    'method':row["Payment Method"],
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
                    'shippingName':row["Shipping Name"],
                    'shippingStreet':row["Shipping Street"],
                    'shippingCity':row["Shipping City"],
                    'shippingZip':str(row["Shipping Zip"]).replace("'",""),
                    'shippingState':row["Shipping Province"],
                    'shippingCountry':row["Shipping Country"],
                    'shippingAmount':row["Shipping"],
                    'discount':row["Discount Amount"],
                    'method':row["Payment Method"],
                    'lineItems':[{
                        'sku':row["Lineitem sku"],
                        'price':row["Lineitem price"],
                        'quantity':row["Lineitem quantity"]
                    }]
                }})

            order = row

        return newDict
        
        

# print(rawCSV.columns)
# print(rawCSV[["Name","whatever"]][0:5]) or rawCSV.Name
# print(rawCSV.iloc[0:4]) gets specific rows
# print(rawCSV.iloc[2,1]) gets a value at a column in a row (R,C)

# print(rawCSV.loc[rawCSV['Name'] == "FB38486"]) looking for specific values in the data
# rawCSV["andresTest"] = "test worked" adding in new keys and values
# rawCSV = rawCSV.drop(columns=['Name '])