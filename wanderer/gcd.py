def gcd(ptlon1,ptlat1,ptlon2,ptlat2):
    import math
    
    ptlon1_radians = math.radians(ptlon1)
    ptlat1_radians = math.radians(ptlat1)
    ptlon2_radians = math.radians(ptlon2)
    ptlat2_radians = math.radians(ptlat2)

    distance_radians=2*math.asin(math.sqrt(math.pow((math.sin((ptlat1_radians-ptlat2_radians)/2)),2) + math.cos(ptlat1_radians)*math.cos(ptlat2_radians)*math.pow((math.sin((ptlon1_radians-ptlon2_radians)/2)),2)))
    # 6371.009 represents the mean radius of the earth
    # shortest path distance
    distance_km = 6371.009 * distance_radians
    return distance_km

