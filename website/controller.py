from .models import Owner
import website.dataaccess as da
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_vehicles():
    vehicles = []
    vehicles = da.get_vehicles_from_db()
    '''
    for i in range(0,10):
        v =Vehicle( plate=f'{i}-xx', brand='BRAND')
        vehicles.append(v)
    '''
    return vehicles

def get_owners():
    owners =[]
    owners = da.get_owners_from_db()
    return owners

def get_owner_by_document(document_number):
    _, owner = da.get_owner_by_document_db(document_number=document_number)
    return owner

def update_owner (owner:Owner):
    print(f'Calling update_owner from controller ')
    succes,reason = da.update_owner_db(owner)
    if not succes: print (reason)
    return succes,reason

def get_owner_of_vehicle(plate):
    _,owner = da.get_owner_of_vehicle_db(plate)
    return owner


def update_vehicle_owner (plate, document_number):
    result = da.check_vehicle_unpaid_infractions(plate)
    if not result[0]:
        # the vehicle doesn't have any pending unpaid infractions
        da.update_vehicle_owner_db(plate, document_number)
        return True
    else:
        return False
    
def get_all_infractions():
    result = da.get_all_infractions_db()
    return result

def get_payment_status ():
    pays = da.get_payment_status_db()
    df=pd.DataFrame.from_records([s.to_dict() for s in pays])
    with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
        #print(df)
        chart=df.sum().to_dict()
        colors=["green","yellow"]
        mylabels = chart.keys()
        values = chart.values()
        
        fig, ax = plt.subplots()
        ax.pie(values, labels=mylabels, autopct='%.0f%%',
            textprops={'size': 'smaller'}, radius=0.5, colors=colors)

        #plt.pie(values, labels=mylabels, colors=colors)
        ax.legend(title="Payment Distribution")
        plt.savefig('website\\static\\rprt.png', format="png", bbox_inches="tight")
        ##plt.show()
