
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely
import math
import sys

qZip=True
qUseSaved=True
qShowMatPlot=False
qTextSave = True
qLimit = False

if qZip:
    def getZipLimits(zipCity,lstCities):
        zipCityHold=zipCity[(zipCity.label.isin(lstCities))]
        print("zipCityHold.label: ", zipCityHold.label)
        lstZips = list(zipCityHold.REGION)
        print("lstZips: ", lstZips)
        zipCityHold=zipCityHold[(zipCityHold.REGION.isin(lstZips))]
        minLat = zipCityHold.INTPTLAT10.min()
        maxLat = zipCityHold.INTPTLAT10.max()
        minLon = zipCityHold.INTPTLON10.min()
        maxLon = zipCityHold.INTPTLON10.max()
        coords = [minLat,maxLat,minLon,maxLon]
        print(">>>>>>>>>>>>>   coords: ", coords)
        return [lstZips,coords]
    
    def strRGB(value,minVal,maxVal):
        strRed="25"
        strGreen = "25"
        strBlue = "25"
        if value >= 0.0 and value < 50.0:
            strRed=str(int(70+(255-70)*(value/50.0)))
            strGreen=str(int(70+(255-70)*(50.0-value)/50.0))
            strVal = "rgba("+strRed+","+strGreen+","+strBlue+",1.0)"
        elif value >= 50.0 and value <=100.0:
            strRed=str(int(70+(255-70)*(value-50.0)/50.0))
            strGreen=str(int(70+(255-70)*(100.0-value)/50.0))
            strVal = "rgba("+strRed+","+strGreen+","+strBlue+",1.0)"
        else:
            strVal="rgba(140,140,140,1.0)"
        # print("value, strVal: ", value,strVal)                       
        return strVal
    
    def convertToColor(diseaseIndicator):
        ### convert to something in log range
        print("type(diseaseIndicator): ", type(diseaseIndicator))
        minDisease = diseaseIndicator.where(diseaseIndicator > -0.5).min()
        maxDisease = diseaseIndicator.max()
        rangeDisease = maxDisease - minDisease
        diseaseIndicator = np.where((diseaseIndicator!=-1),diseaseIndicator-minDisease/rangeDisease,diseaseIndicator)
        ### convert to color using log range
        colorIndicator = pd.Series(np.where((diseaseIndicator!=-1),np.log(1.0 + diseaseIndicator.astype(float)),diseaseIndicator))
        print("type(colorIndicator): ", type(colorIndicator))
        minIndicator = colorIndicator.where(colorIndicator > -0.5).min()
        maxIndicator = colorIndicator.max()
        rangeIndicator = maxIndicator - minIndicator
        print("rangeLogIndicator: ", rangeIndicator)
        colorIndicator = np.where((colorIndicator!=-1),((100.0*(colorIndicator-minIndicator)/rangeIndicator)).astype(int),colorIndicator)
        return colorIndicator
    
    def convert(point,scale,x_min,y_max,factor):
        # print(">>> point: ", point)
        # print(">>> scale, x_min, y_max: ", scale,x_min,y_max)
        X = int(factor*(scale * (point[0] - x_min)))/factor
        Y = int(factor*(scale * (y_max - point[1])))/factor
        strXY = str(X) + ',' + str(Y) + ' '
        # print(">>> strXY: ", strXY)
        return strXY

    def to_polygon(geoType, geometry, scale, x_min, y_max, strID, label, value,strI):
        # print("\n\nENTERED TO_POLYGON AT: ", strI)
        limit = geometry.bounds
        # print("limit: ", limit)
        strArea = str(int(geometry.area*10)/10.0)
        centroid = geometry.centroid.coords[0]
        strCentroid = convert(centroid,scale,x_min,y_max,10.0)
        # print("strI, strCentroid: ", strI, strCentroid)
        limit0=limit[0]+(centroid[0]-limit[0])/3.0
        limit3=limit[3]+(centroid[1]-limit[3])/3.0
        strLimit = convert([limit0,limit3],scale,x_min,y_max,10.0)
        # print("strI, strLimit: ", strI, strLimit)
        polygons = []
        if type(geometry) is shapely.geometry.multipolygon.MultiPolygon:
            for iPoly, polygon in enumerate(geometry):
                if (iPoly==0 or polygon.area > 0.001):
                    polygons.append(list(polygon.exterior.coords))
        elif type(geometry) is shapely.geometry.polygon.Polygon:
            polygons.append(list(geometry.exterior.coords))
        else:
            raise ValueError("Geometry is not a polygon or multipolygon")
        # print("strI, strLimit, strCentroid: ", strI, strLimit,strCentroid)
        # strLimit = strCentroid
        htmlPoly = ""
        htmlRegion = ""
        nPoints=0
        for iPoly, polygon in enumerate(polygons):
            strPointsLabel = "points_"+strI+"_"+str(iPoly)
            htmlPoly += " <polygon id='"+strPointsLabel+"' points= '"
            nPoints += len(polygon)
            for iPoint, point in enumerate(polygon):
                strPt = convert(point,scale,x_min,y_max,10000.0)
                htmlPoly += strPt
            htmlPoly += "' /> \n"
            if iPoly == 0:
                htmlRegion += " <g class=\"thing\" id='"+geoType+strID+"'\n" 
                htmlRegion += "   onmouseover=\"texts["+strI+"].setAttribute('transform','translate("+strLimit+")'); \n"
                htmlRegion += "       rects["+strI+"].setAttribute('transform','translate("+strLimit+")');\n"
                htmlRegion += "       adjustRect("+strI+",'text"+strI+"',mouseOvers["+strI+"],'OVER');\n"
                htmlRegion += "       rects["+strI+"].style.fill='rgba(240,180,240,1.0)';texts["+strI+"].style.fill='black';\"  \n"
                htmlRegion += "   onmouseout=\"texts["+strI+"].setAttribute('transform','translate("+strLimit+")');\n"
                htmlRegion += "       rects["+strI+"].setAttribute('transform','translate("+strLimit+")');\n"
                htmlRegion += "              adjustRect("+strI+",'text"+strI+"',mouseOverx["+strI+"],'OUT'); \n"
                htmlRegion += "       rects["+strI+"].style.fill='transparent';texts["+strI+"].style.fill='blue';\" >\n"
        htmlRegion += htmlPoly
        htmlRegion += "    <rect transform='translate("+strLimit+")' x='0' y='0' width='100' height='100' stroke='transparent' fill='transparent'></rect> \n"
        htmlRegion += "    <text id='text"+strI+"' x='0' y='50' transform='translate("+strLimit+")' font-family='Verdana' font-size='10' fill='blue'>"+"</text> \n"
        htmlRegion += "</g> \n"
        return htmlPoly,htmlRegion, strLimit,strArea

    def to_html(gdf, lstParams,lstStems,lstStemLabels,width=None):  
        # lstParams = ['geometry_simplified','REGION','label','COVID','percColorCOVID']
        # lstStems = ['REGION','label','COVID','percColorCOVID','diseaseDensity','populationDensity']
        # print("gdf.columns: ", gdf.columns)
        # print("gdf.shape: ", gdf.shape)
        geometry_col = lstParams[0]
        id_col = lstParams[1]
        label_col = lstParams[2]
        value_col = lstParams[3]
        color_col = lstParams[4]
        # print("color_col: ", color_col)
        # print("geometry_col: ", geometry_col)
        min_x = min([row.geometry_simplified.bounds[0] for i, row in gdf.iterrows()])
        min_y = min([row.geometry_simplified.bounds[1] for i, row in gdf.iterrows()])
        max_x = max([row.geometry_simplified.bounds[2] for i, row in gdf.iterrows()])
        max_y = max([row.geometry_simplified.bounds[3] for i, row in gdf.iterrows()])
        if not width:
            width = 1000
        scale = width / (max_x - min_x)
        height = math.ceil(scale * (max_y - min_y))
        num_regions = gdf.shape[0]
        geometries = list(gdf[geometry_col])
        values = list(gdf[value_col])
        colors = list(gdf[color_col])
        popl = list(gdf.population)
        ids = list(gdf.REGION)
        disDens = list(gdf.diseaseDensity)
        popDens = list(gdf.populationDensity)
        geoTypes = list(gdf.GEO_TYPE)
        valStems=[]
        for ii in range(len(lstStems)):
            valStems.append(list(gdf[lstStems[ii]]))
        if not id_col:
            ids = [f'region_id_{i}' for i in range(num_regions)]
        else:
            ids = list(gdf[id_col])
        if not label_col:
            labels = ['' for i in range(num_regions)]
        else:
            labels = list(gdf[label_col])
        html = '<html>'
        html += '<head><style>\n'
        for i in range(num_regions):
            strID = str(ids[i])
            geoType = str(geoTypes[i])
            if geoType=='state':
                html += "#"+geoType+strID + ' {stroke-width:1; stroke:purple; fill:rgba(195,195,195,1.0);}'
            else:
                html += "#"+geoType+strID + ' {stroke-width:1; stroke:purple; fill:'+strRGB(colors[i],0.0,100.0)+';}'
            html += "#"+geoType+strID + ':hover {stroke-width:1; stroke:purple; fill:rgba(0,255,255,1.0);}\n'
        html += '</style></head>\n'
        print(">>>>   height, width: ", height, width)
        htmlRegions = "<svg onload='init()' viewBox='0 0 750 750'  width='auto' height='"+str(int(height+100))+"px'>\n\n"
        htmlMouseOvers = "<script>\n"
        htmlMouseOvers += "var mouseOvers = new Array() \n"
        htmlMouseOverx = "var mouseOverx = new Array() \n"
        # print(">>>>>>>>>>>>> len(lstStems): ",len(lstStems))
        # print("num_regions: ", num_regions)
        for i in range(num_regions):
            geoType = str(geoTypes[i])
            strI = str(i)
            strCases = str(values[i])
            strID = str(ids[i])
            strPopl = str(popl[i])
            strDisDens = str(disDens[i])
            strPopDens = str(popDens[i])
            htmlPoly,htmlRegion, strLimit,strArea = to_polygon(geoType, geometries[i],scale,min_x, max_y, strID, labels[i], values[i],strI)
            htmlRegions += htmlRegion
            mouseover = "\""+str(ids[i])
            for ii in range(1,len(lstStems)):
                strStem = lstStemLabels[ii]+str(valStems[ii][i])
                mouseover+= "<tspan x='7' dy='1.1em' font-size='10' fill='black'>"+strStem+"</tspan>"
            mouseover+= "\"\n"
            # htmlMouseOverx+= "  mouseOverx["+str(i)+"] = \""+str(ids[i])+"\"  \n"
            htmlMouseOverx+= "  mouseOverx["+str(i)+"] = \""+"\"  \n"
            htmlMouseOvers += "  mouseOvers["+strI+"] = " + mouseover
        htmlMouseOverx += "</script>\n"
        html += htmlMouseOvers
        html += htmlMouseOverx
        htmlBody = """
<body>
    <script>
        var texts, rects
        var padding = 0
        function init() {
            list = document.getElementsByTagName("text")
	    texts = Array.from(list)
	    length = texts.length
            list = document.getElementsByTagName("rect")
	    rects = Array.from(list)
	    list = document.getElementsByTagName("polygon")
	    polygons = Array.from(list)
            for (var i = 0; i < length; i++) {
                adjustRect(i, texts[i],'none','INIT')
            }
        }
    </script>
    <script>
        var topIndex;
        var topElement;
        function adjustRect(i, strElement, mouseovertext,strPurpose) {
            if (strPurpose != 'INIT') {
		// console.log("topIndex: "+topIndex)
		if (topIndex != i & topIndex != null) {
		    topElement.innerHTML = mouseOverx[topIndex]
		    // console.log("topIndex: "+topIndex)
		    rectVal = rects[topIndex]
		    textVal = texts[topIndex]
		    bringToBottomofSVG(rectVal)
		    bringToTopofSVG(textVal)}
                var tt = document.getElementById(strElement);
                tt.innerHTML = mouseovertext
		topIndex=i
		topElement=tt
		rectVal = rects[i]
		textVal = texts[i]
		bringToTopofSVG(rectVal)
		bringToTopofSVG(textVal)
                }
            var bbox
            var textVal, rectVal
            textVal = texts[i]
            rectVal = rects[i]
            bbox = textVal.getBBox()
            rectVal.setAttribute("x", bbox.x - padding)
            rectVal.setAttribute("y", bbox.y - padding)
            rectVal.setAttribute("width", bbox.width + 2 * padding)
            rectVal.setAttribute("height", bbox.height + 2 * padding) }
    </script>
    <script>
        function bringToTopofSVG(targetElement){
              let parent = targetElement.ownerSVGElement;
              parent.appendChild(targetElement);
        }
        function bringToBottomofSVG(targetElement){ 
              let parent = targetElement.ownerSVGElement;
              parent.prepend(targetElement); 
        } 	
    </script>
"""
        html += htmlBody
        html += htmlRegions + "</svg>\n"  
        html += "</body></html>"
        return html

    def getAZData():
        strFile = './data/COVID19CONFIRMED_BYZIP_07212020.xls'
        excel = pd.read_excel(strFile,sheet_name=0,dtype={'POSTCODE':str,'ConfirmedCaseCount':str})
        excel = excel.replace({'ConfirmedCaseCount': {'1-5':'3','6-10':'8','Data Suppressed':'-1'}})
        excel = excel.rename(columns={'POSTCODE':'zip_codes','ConfirmedCaseCategory':'categ', 'ConfirmedCaseCount':'counts'})
        excel = excel[['zip_codes','counts']]
        excel['zip_codes'] = excel.zip_codes.str[:5].astype(int)
        excel = excel.drop_duplicates(subset=['zip_codes'],keep='last',inplace=False)
        print("excel.shape: ", excel.shape)
        strFile = './data/COVID19CONFIRMED_BYZIP_06302020.xls'
        excelx = pd.read_excel(strFile,sheet_name=0,dtype={'POSTCODE':str,'ConfirmedCaseCount':str})
        excelx = excelx.replace({'ConfirmedCaseCount': {'1-5':'3','6-10':'8','Data Suppressed':'-1'}})
        excelx = excelx.rename(columns={'POSTCODE':'zip_codes','ConfirmedCaseCategory':'categ', 'ConfirmedCaseCount':'oldCounts'})
        excelx = excelx[['zip_codes','oldCounts']]
        excelx['zip_codes'] = excelx.zip_codes.str[:5].astype(int)
        excelx = excelx.drop_duplicates(subset=['zip_codes'],keep='last',inplace=False)
        print("excelx.shape: ", excelx.shape)
        excel = excel.merge(excelx, how='outer', on='zip_codes')
        print("excel.shape: ", excel.shape)
        zipX = np.genfromtxt('./AZ_COVID19_ZIP.csv', dtype= None, encoding=None, skip_header=0, delimiter=",", names=True)
        # zipX.sort()
        zipX = pd.DataFrame(zipX)
        print("zipX.columns: ", zipX.columns)
        # zipX = zipX.rename(columns={'f0':'zip_codes','f1':'label','f2':'confirmed','f3':'population','f4':'transient'})
        zip_merged = zipX.merge(excel, how='outer', on='zip_codes')
        print("zip_merged.shape: ", zip_merged.shape)
        zip_sorted = zip_merged.sort_values('zip_codes')
        return zip_sorted

    if qUseSaved:
        ZCTA5_POLYGON = gpd.read_file('./zips2019/AZ_ZIP.shp')
    else: 
        ZCTA5_POLYGON = gpd.read_file('./zips2019/tl_2019_us_zcta510.shp')
        ZCTA5_POLYGON = ZCTA5_POLYGON[(ZCTA5_POLYGON.INTPTLAT10 >= '+31.3506') & (ZCTA5_POLYGON.INTPTLAT10 <= '+37.0175')]
        ZCTA5_POLYGON = ZCTA5_POLYGON[(ZCTA5_POLYGON.INTPTLON10 <= '-114.790') & (ZCTA5_POLYGON.INTPTLON10 >= '-109.032')]
        ZCTA5_POLYGON = ZCTA5_POLYGON.rename(columns={"ZCTA5CE10":"REGION"})
        ZCTA5_POLYGON.to_file('./zips2019/AZ_ZIP.shp')
    ZCTA5_POLYGON = ZCTA5_POLYGON.rename(columns={'INTPTLAT10':'LAT','INTPTLON10':'LON','ALAND10':'area_land','AWATER10':'area_water'})
    ZCTA5_POLYGON = ZCTA5_POLYGON[['REGION','LAT','LON','area_land','area_water','geometry']]
    ZCTA5_POLYGON['geometry_simplified']=ZCTA5_POLYGON['geometry'].apply(lambda x: x.simplify(0.0005))
    ZCTA5_POLYGON['GEO_TYPE'] = 'zip'

    state = gpd.read_file('./state2019/tl_2019_us_state.shp')
    state = state.rename(columns={'NAME':'label','INTPTLAT':'LAT','INTPTLON':'LON','ALAND':'area_land','AWATER':'area_water'})
    state = state[state.STUSPS == 'AZ'][['REGION','label','LAT','LON','area_land','area_water','geometry']]
    state['geometry_simplified']=state['geometry'].apply(lambda x:x.simplify(0.0005))
    state['GEO_TYPE'] = 'state'
    # state = state[state.STUSPS == 'AZ'][['REGION','LAT','LON','area_land','area_water','geometry']]
    print("ZCTA5_POLYGON.columns: ", ZCTA5_POLYGON.columns)
    print("state.columns: ", state.columns)
    # ZCTA5_POLYGON = state.append(ZCTA5_POLYGON)
    # sys.exit(0)

    # REGION_POLYGON = ZCTA5_POLYGON
    
    zipCity = ZCTA5_POLYGON
    
    zipCity['REGION'] = zipCity['REGION'].astype(int)
    print("zipCity.shape: ", zipCity.shape)
    print("zipCity.columns: ", zipCity.columns)
    zipCOVID = getAZData()[['zip_codes','label','counts','oldCounts','population','transient']]
    zipCOVID = zipCOVID.rename(columns={"zip_codes":"REGION","counts":"COVID","oldCounts":"oldCOVID"})
    
    zipCOVID['REGION'] = zipCOVID['REGION'].astype(int)
    zipCity = zipCity.merge(zipCOVID, on='REGION', how='inner')
    zipCity['COVID']=zipCity['COVID'].fillna('-1').astype(int)

    if qLimit:
        # zipCity=zipCity[(zipCity.REGION.isin([86040,86432,86445,86404,85348,85356,85533,85546]))]
        # lstCities=['Phoenix','Surprise','Scottsdale','Tempe','Cave Creek','New River','Goodyear']
        lstCities=['Surprise','Luke Airforce Base']
        # lstCities = ['Yuma','Gadsden','San Luis','Somerton','Wellton']
        [lstZips,coords] = getZipLimits(zipCity,lstCities)
        zipCity = zipCity[(zipCity.INTPTLAT10 >= coords[0]) & (zipCity.INTPTLAT10 <= coords[1])]
        zipCity = zipCity[(zipCity.INTPTLON10 <= coords[3]) & (zipCity.INTPTLON10 >= coords[2])]

    zipCity = zipCity[~(zipCity.geometry.is_empty | zipCity.geometry.isna())]
    zipCity['diseaseDensity'] = np.where((zipCity.COVID!=-1), 
              (1000*100.0*zipCity.COVID.astype(float)/zipCity.population.astype(float)).astype(int)/1000.0,zipCity.COVID)
    zipCity['area'] = zipCity.area
    zipCity['zipArea'] = (10000000.0*zipCity.area.astype(float)).astype(int)/1000.0

    zipCity['populationDensity'] = (1000*100.0*zipCity.population.astype(float)/zipCity.zipArea).astype(int)/1000.0
    print("zipCity.shape: ", zipCity.shape)
    print("zipCity.columns: ",zipCity.columns)
    zipCity['percColorCOVID'] = convertToColor(zipCity['diseaseDensity'])

    print("************BEFORE TO_HTML********************")
    bounds = zipCity.geometry.bounds
    x_min = bounds.minx.min()
    x_max = bounds.maxx.max()
    y_min = bounds.miny.min()
    y_max = bounds.maxy.max()
    width = 300
    scale = width / (x_max - x_min)
    height = math.ceil(scale * (y_max - y_min))
    point = [x_max,y_min]
    print("width, scale, y_max, x_min: ", width, scale, y_max, x_min)
    width = width * 600.0/height
    #  y_max = y_max * 600.0/height
    scale = scale * 600.0/height
    strBounds = convert(point,scale,x_min,y_max,10000.0)
    print("OVERALL, strBounds: ", "OVERALL", strBounds)

    print("width, scale, y_max, x_min: ", width, scale, y_max, x_min)
    print(">>>>>>>>>  strBounds: ", strBounds)

####  append AZ state
    zipCity = state.append(zipCity)
    zipCity = zipCity.reset_index(drop=True)
    if qTextSave:
        lstText = ['REGION','label','COVID','population','diseaseDensity','populationDensity','zipArea']
        lstText.extend(['transient','area_land','area_water','LAT','LON'])
        zipCityText = zipCity[lstText]
        zipCityText.to_csv("./AZ_COVID_OUTPUT.csv", index=False)

    lstParams = ['geometry_simplified','REGION','label','COVID','percColorCOVID']
    lstStems = ['REGION','label','COVID','population','diseaseDensity','populationDensity','zipArea']
    lstStemLabels = ['','','Cases: ','Popl: ','disDens: ','popDens: ','area: ']
    html = to_html(zipCity,lstParams,lstStems,lstStemLabels,width=width)
    total_bounds = zipCity.total_bounds
    print("total_bounds: ", total_bounds)
    print("*****  COMPLETED ZIP")

    if qShowMatPlot:
        zipNONE = zipCity[zipCity.COVID == '-1']
        zipCity = zipCity[zipCity.COVID != '-1']
        zipCity['COVID'] = np.log(1.0 + zipCity['COVID'].astype(float))
        strEPSG = "EPSG:2163"  ### shaped bad (equal area)
        # strEPSG = "EPSG:4326"  ### unshaped good LAT/LON
        fig, ax = plt.subplots(1,1)
        divider = make_axes_locatable(ax)
        ax.set_aspect('equal')
        ax.set_axis_off()
        cax = divider.append_axes("right", size="5%", pad=0.1)
        state.boundary.plot(ax = ax, zorder=8)
        plt.tight_layout()
        (plt.gcf()).set_size_inches(8,8)
        strTitle = "COVID "+'COVID'
        plt.gcf().canvas.set_window_title(strTitle)
        # zipCity = zipCity[zipCity['REGION']==85388]
        # print("zipCity.shape: ", zipCity.shape)
        _ = state.plot(ax=ax, zorder=1)
        _ = zipNONE.plot(ax=ax,zorder=3,color='grey')
        _ = zipCity.plot(ax=ax,cax=cax, figsize=(15,15),column='COVID',legend=True,zorder=5,
                    cmap='RdYlGn_r',edgecolor='k',lw=0.7, scheme=None)
        plt.show()
    
    with open("output_AZ_EDGE.html", "w") as f: 
        f.write(html) 
    import webbrowser
    import os
    from urllib.request import pathname2url
    url = 'file:{}'.format(pathname2url(os.path.abspath('output_AZ_EDGE.html')))
    webbrowser.open(url)

