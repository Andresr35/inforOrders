import pandas as pd
import csv
import json



class csvUtils:
    """creates an object from shopify csv 
    """

    
    def readCSV(csvInput):
        """Reads shpify csv to give back an object to allow for easier looping through orders and line items

        Args:
            csvInput (filePath): path to where csv file is

        Returns:
            dict: dictionary holding orders
        """

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
        
        
    def createCSV(finishedOrders:list,failedOrders:list):
        headings = ["Order","Status"]
        file = open('orders.csv','w',encoding='UTF8')
        writer = csv.writer(file)

        writer.writerow(headings)
        for order in failedOrders:
            writer.writerow([order,'Failed'])
        for order in finishedOrders:
            writer.writerow([order,'Finished'])

        file.close()
    # os.system('orders.csv')
class jsonUtils:

    def readJSON() -> dict:
        """reads the countries json and gives back a dict with the code

        Returns:
            dict: dict holding the code as the key and the name as the value
        """
        with open('names.json') as json_file:
            data = json.load(json_file)
            return data
