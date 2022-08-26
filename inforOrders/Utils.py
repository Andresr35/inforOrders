''' 
This file is meant to hold parser functions that read/write csv and json files. 

Here the parser for the input csv will be changed to a dict,
    orders.csv will be created here,
    and reading the names.json file into a dict.
'''


import csv
import json

import pandas as pd


class csvUtils:
    """ Parser functions for reading input csv and export csv with finished orders
    """

    def readCSV(csvInput):
        """Reads shpify csv to give back an object to allow for easier looping through orders and line items

        Args:
            csvInput (filePath): path to where csv file is

        Returns:
            dict: dictionary holding orders
        """

        # Using pandas library to help parse csv
        rawCSV = pd.read_csv(csvInput)
        newDict = {}

        # Going through each row in csv and making a key
        for index, row in rawCSV.iterrows():
            # If statement here deals with the way infor exports csv's
            # orders can span multiple rows, need a way to parse that into a dict
            if('order' not in locals()):
                newDict.update({
                    row['Name']: {
                        'shippingName': row["Shipping Name"],
                        'shippingStreet': row["Shipping Street"],
                        'shippingCity': row["Shipping City"],
                        'shippingZip': row["Shipping Zip"].replace("'", ""),
                        'shippingState': row["Shipping Province"],
                        'shippingCountry': row["Shipping Country"],
                        'shippingAmount': row["Shipping"],
                        'discount': row["Discount Amount"],
                        'method': row["Payment Method"],
                        'lineItems': [{
                            'sku': row["Lineitem sku"],
                            'price':row["Lineitem price"],
                            'quantity':row["Lineitem quantity"]
                        }]
                    }})
            elif(row["Name"] == order["Name"]):
                x: dict = newDict.get(row["Name"])
                y: list = x.get('lineItems')
                y.append(
                    {
                        'sku': row["Lineitem sku"],
                        'price': row["Lineitem price"],
                        'quantity': row["Lineitem quantity"]
                    })
            else:
                newDict.update({row["Name"]: {
                    'shippingName': row["Shipping Name"],
                    'shippingStreet': row["Shipping Street"],
                    'shippingCity': row["Shipping City"],
                    'shippingZip': str(row["Shipping Zip"]).replace("'", ""),
                    'shippingState': row["Shipping Province"],
                    'shippingCountry': row["Shipping Country"],
                    'shippingAmount': row["Shipping"],
                    'discount': row["Discount Amount"],
                    'method': row["Payment Method"],
                    'lineItems': [{
                        'sku': row["Lineitem sku"],
                        'price':row["Lineitem price"],
                        'quantity':row["Lineitem quantity"]
                    }]
                }})
            order = row

        return newDict

    def createCSV(finishedOrders: list, failedOrders: list):
        """Creating a csv to export failed and finished orders

        Args:
            finishedOrders (list): strings of orders that finished sucessfully
            failedOrders (list): str of orders that failed and need revision
        """
        # Setting up csv writer
        headings = ["Order", "Status"]
        file = open('../orders.csv', 'w', encoding='UTF8')
        writer = csv.writer(file)

        # Writing the rows to csv
        writer.writerow(headings)
        for order in failedOrders:
            writer.writerow([order, 'Failed'])
        for order in finishedOrders:
            writer.writerow([order, 'Finished'])

        # Finish the csv
        file.close()


class jsonUtils:
    """ Converts json to dict
    """

    def readJSON() -> dict:
        """reads the countries json and gives back a dict with the code

        Returns:
            dict: dict holding the code as the key and the name as the value
        """
        with open('./assets/names.json') as json_file:
            data = json.load(json_file)
            return data
