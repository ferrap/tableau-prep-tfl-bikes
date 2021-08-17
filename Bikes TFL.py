import requests
from xml.etree import cElementTree as ET
import pandas as pd

def tfl_cycle_data(df):
    df = pd.DataFrame()
    
    response = requests.get("https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml")
    root= ET.fromstring(response.content)
    
    time_stamp = root.attrib['lastUpdate']
    time_stamp = int(time_stamp)
    time_stamp=[time_stamp]*len(root)
    
    id_list = [int(root[i][0].text) for i in range(0, len(root))]
    name_list = [root[i][1].text for i in range(0, len(root))]
    lat_list = [float(root[i][3].text) for i in range(0, len(root))]
    lon_list = [float(root[i][4].text) for i in range(0, len(root))]
    nbike_list=[int(root[i][10].text) for i in range(0, len(root))]
    nempty_list=[int(root[i][11].text) for i in range(0, len(root))]
    capacity_list = [int(root[i][12].text) for i in range(0, len(root))]

    
    all_locs = pd.DataFrame(list(zip(time_stamp, name_list, id_list, lat_list,lon_list, capacity_list,nbike_list,nempty_list)), columns = ["time_stamp","name","id","lat","lon","dock_capacity","bikes_availables","empty_space"])
    all_locs['time_stamp'] = pd.to_datetime(all_locs['time_stamp'],unit ='ms')
    all_locs['time_stamp'] = all_locs['time_stamp'].astype('str')
    df=all_locs
    
    return df
    


# this defines the columns and data types going back out to Prep
def get_output_schema():
    print('Getting output schema...\n')
    return pd.DataFrame({
        'time_stamp' : prep_string(),
        'id' : prep_int(),
        'lat' : prep_decimal(),
        'lon' : prep_decimal(),
        'dock_capacity' : prep_int(),
        'bikes_availables' : prep_int(),
        'empty_space' : prep_int(),
        'name' : prep_string()
        })

