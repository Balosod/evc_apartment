from beanie.operators import RegEx,And,Or,In,GTE,LTE, GT,LT
from server.models.property import Property



async def filters(location,capacity):
    
    data = {"count":"","data":""}
    location_pattern = f'^{location}$' if location != None else rf'[a-zA-Z0-9_]'
    if location != None and capacity != None:
        result = await Property.find(And((RegEx(Property.nearest_area, location_pattern,"i")),(Property.capacity == capacity),(Property.approval_status == True)),fetch_links=True).to_list()
        data["count"] = len(result)
        data["data"] = result
        return data
    if location != None:
        result = await Property.find(And((RegEx(Property.nearest_area, location_pattern,"i")),(Property.approval_status == True)),fetch_links=True).to_list()
        data["count"] = len(result)
        data["data"] = result
        return data
    if capacity != None:
        result = await Property.find(And((Property.capacity == capacity),(Property.approval_status == True)),fetch_links=True).to_list()
        data["count"] = len(result)
        data["data"] = result
        return data
    if location  ==  None and capacity == None:
        result = await Property.find(Property.approval_status == True,fetch_links=True).to_list()
        data["count"] = len(result)
        data["data"] = result
        return data
    
