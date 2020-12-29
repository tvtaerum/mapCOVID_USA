
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely
import math
import sys, os

riverSegMiles = 5.0
qZip=True
qTextSave = False
qLimit = False
strFileCovidNew = '12-04-2020.csv'
strFileCovidNew = '12-25-2020.csv'
strFileCovidOld = '11-13-2020.csv'
strFileCovidOld = '12-04-2020.csv'
minIndicator = 0.0
maxIndicator = 0.0
# maxIndicator = 2.6332548132452

lstStts = ['WA','OR','MT','ID','WY']
lstStts = ['ND','SD','NE','IA','MN','WI','IL']
# lstStts = ['TX','OK','KS','MO','AR','LA']
# lstStts = ['AZ','CA','NM','UT','NV']
# lstStts = ['NY','CT','NJ']
lstStts = ['MS','LA','MO','TN']
qJoinStateCountyLabel = True
qLakes = True
qUSRivers = False
qStateRivers = True
qDiffCOVIDcounts = True
########### !!!!!!!!!!!!!!!!!  DO NOT DELETE  !!!!!!!!!!!!!!!!!!!!################
lstStates = ['Alabama','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Idaho','Illinois','Indiana']
lstStates.extend(['Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri'])
lstStates.extend(['Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota'])
lstStates.extend(['Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah'])
lstStates.extend(['Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming','District of Columbia'])
lstSTx = ['AL','AZ','AR','CA','CO','CT','DE','FL','GA','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO']
lstSTx.extend(['MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','DC'])
########### !!!!!!!!!!!!!!!!!  DO NOT DELETE  !!!!!!!!!!!!!!!!!!!!################



if qZip:

    def correctPopData(csvPop):
        temp_df = []
        for row in csvPop.itertuples(index=False):
            t_row=list(row)
            if row.STATE == 'Missouri' and row.CTYNAME=='St. Louis' and row.FIPS==29510:
                t_row[4]='St. Louis City'
                temp_df.append(t_row)
            elif row.STATE == 'New Mexico' and row.FIPS==35013:
                t_row[4]='Dona Ana'
                temp_df.append(t_row)
            else:
                temp_df.append(t_row)

        csvPop = pd.DataFrame(temp_df, columns=csvPop.columns)
        return csvPop
        

    def correctCovidData(csvCovid):
        temp_df = []
        for row in csvCovid.itertuples(index=False):
            t_row=list(row)
            # print("t_row: ", t_row)
            if row.STATE == 'Utah' and row.CTYNAME=='Bear River':
                t0_row=list(t_row); t0_row[0]=49003; t0_row[1]='Box Elder'  ; t0_row[4] = int(t0_row[4]*56046.0/186818.0)
                t1_row=list(t_row); t1_row[0]=49005; t1_row[1]='Cache'      ; t1_row[4] = int(t1_row[4]*128289.0/186818.0)
                t2_row=list(t_row); t2_row[0]=49033; t2_row[1]='Rich'       ; t2_row[4] = int(t2_row[4]*2483.0/186818.0)
                temp_df.extend([t0_row,t1_row,t2_row])
            elif row.STATE == 'Utah' and row.CTYNAME=='Southwest Utah':
                t0_row=list(t_row); t0_row[0]=49001; t0_row[1]='Beaver'    ; t0_row[4] = int(t0_row[4]*6710.0/252042.0)
                t1_row=list(t_row); t1_row[0]=49017; t1_row[1]='Garfield'  ; t1_row[4] = int(t1_row[4]*5051.0/252042.0)
                t2_row=list(t_row); t2_row[0]=49021; t2_row[1]='Iron'      ; t2_row[4] = int(t2_row[4]*54839.0/252042.0)
                t3_row=list(t_row); t3_row[0]=49025; t3_row[1]='Kane'      ; t3_row[4] = int(t3_row[4]*7886.0/252042.0)
                t4_row=list(t_row); t4_row[0]=49053; t4_row[1]='Washington'; t4_row[4] = int(t4_row[4]*177556.0/252042.0)
                temp_df.extend([t0_row,t1_row,t2_row,t3_row,t4_row])
            elif row.STATE == 'Utah' and row.CTYNAME=='Southeast Utah':
                t0_row=list(t_row); t0_row[0]=49007; t0_row[1]='Carbon' ; t0_row[4] = int(t0_row[4]*20463.0/40229.0)
                t1_row=list(t_row); t1_row[0]=49015; t1_row[1]='Emery'  ; t1_row[4] = int(t1_row[4]*10012.0/40229.0)
                t2_row=list(t_row); t2_row[0]=49019; t2_row[1]='Grand'  ; t2_row[4] = int(t2_row[4]*9754.0/40229.0)
                temp_df.extend([t0_row,t1_row,t2_row])
            elif row.STATE == 'Utah' and row.CTYNAME=='TriCounty':
                t0_row=list(t_row); t0_row[0]=49009; t0_row[1]='Daggett' ; t0_row[4] = int(t0_row[4]*950.0/56622.0)
                t1_row=list(t_row); t1_row[0]=49047; t1_row[1]='Uintah'  ; t1_row[4] = int(t1_row[4]*35734.0/56622.0)
                t2_row=list(t_row); t2_row[0]=49013; t2_row[1]='Duchesne'; t2_row[4] = int(t2_row[4]*19938.0/56622.0)
                temp_df.extend([t0_row,t1_row,t2_row])
            elif row.STATE == 'Utah' and row.CTYNAME=='Central Utah':
                t0_row=list(t_row); t0_row[0]=49023; t0_row[1]='Juab'    ; t0_row[4] = int(t0_row[4]*12017.0/81954.0)
                t1_row=list(t_row); t1_row[0]=49027; t1_row[1]='Millard' ; t1_row[4] = int(t1_row[4]*13188.0/81954.0)
                t2_row=list(t_row); t2_row[0]=49031; t2_row[1]='Piute'   ; t2_row[4] = int(t2_row[4]*1479.0/81954.0)
                t3_row=list(t_row); t3_row[0]=49055; t3_row[1]='Wayne'   ; t3_row[4] = int(t3_row[4]*2711.0/81954.0)
                t4_row=list(t_row); t4_row[0]=49039; t4_row[1]='Sanpete' ; t4_row[4] = int(t4_row[4]*30939.0/81954.0)
                t5_row=list(t_row); t5_row[0]=49041; t5_row[1]='Sevier'  ; t5_row[4] = int(t5_row[4]*21620.0/81954.0)
                temp_df.extend([t0_row,t1_row,t2_row,t3_row,t4_row,t5_row])
            elif row.STATE == 'Utah' and row.CTYNAME=='Weber-Morgan':
                t0_row=list(t_row); t0_row[0]=49057; t0_row[1]='Weber'  ; t0_row[4] = int(t0_row[4]*260213.0/272337.0)
                t1_row=list(t_row); t1_row[0]=49029; t1_row[1]='Morgan' ; t1_row[4] = int(t1_row[4]*12124.0/272337.0)
                temp_df.extend([t0_row,t1_row])
            elif row.STATE == 'Massachusetts' and row.CTYNAME=='Dukes and Nantucket':
                t0_row=list(t_row); t0_row[0]=25007; t0_row[1]='Dukes'
                t1_row=list(t_row); t1_row[0]=25019; t1_row[1]='Nantucket'
                temp_df.extend([t0_row,t1_row])
            else:
                temp_df.append(t_row)

        csvCovid = pd.DataFrame(temp_df, columns=csvCovid.columns)
        return csvCovid

  
    def strRGB(value):
        strRed="25"
        strGreen = "25"
        strBlue = "25"
        if value >= 0.0 and value < 50.0:
            strRed=str(int(70+(255-70)*(value/100.0)))
            strGreen = str(int(100+150*(100-value)/100.0))
            strVal = "rgba("+strRed+","+strGreen+","+strBlue+",1.0)"
        elif value >= 50.0 and value <=100.0:
            strRed = str(int(100+150*(value/100.0)))
            strGreen=str(int(70+(255-70)*(100.0-value)/100.0))
            strVal = "rgba("+strRed+","+strGreen+","+strBlue+",1.0)"
        else:
            strVal="rgba(140,140,140,1.0)"
        # print("value, strVal: ", value,strVal)                       
        return strVal
    
    def convertToColor(diseaseIndicator, minIndicator, maxIndicator):
        ### convert to something in log range
        # print("diseaseIndicator: ", list(diseaseIndicator))
        minDisease = diseaseIndicator.where(diseaseIndicator > -0.5).min()
        maxDisease = diseaseIndicator.max()
        rangeDisease = maxDisease - minDisease
        diseaseIndicator = np.where((diseaseIndicator!=-1),diseaseIndicator-minDisease/rangeDisease,diseaseIndicator)
        ### convert to color using log range
        colorIndicator = pd.Series(np.where((diseaseIndicator!=-1),np.log(1.0 + diseaseIndicator.astype(float)),diseaseIndicator))
        if minIndicator == 0.0: 
            minIndicator = colorIndicator.where(colorIndicator > -0.5).min()
        if maxIndicator == 0.0: 
            maxIndicator = colorIndicator.max()
        print("minIndicator, maxIndicator: ", minIndicator, maxIndicator)
        rangeIndicator = maxIndicator - minIndicator
        if np.isnan(rangeIndicator):
            rangeIndicator = minIndicator = maxIndicator = 1
        # print("colorIndicator: ", list(colorIndicator))
        # print("rangeIndicator: ", rangeIndicator)
        colorIndicator = np.where((colorIndicator!=-1),((100.0*(colorIndicator-minIndicator)/rangeIndicator)).astype(int),colorIndicator)
        #  print("colorIndicator: ", list(colorIndicator))
        return colorIndicator
    
    def convert(point,scale,x_min,y_max,factor):
        # print(">>> point: ", point)
        # print(">>> scale, x_min, y_max: ", scale,x_min,y_max)
        X = int(factor*(scale * (point[0] - x_min)))/factor
        Y = int(factor*(scale * (y_max - point[1])))/factor
        strXY = str(X) + ',' + str(Y) + ' '
        # print(">>> strXY: ", strXY)
        return strXY

    def to_geometry(geoType, geometry, scale, x_min, y_max, strID, label, value,strI):
        # print("\n\nENTERED to_geometry AT: ", strI)
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
        geometrys = []
        geometryTypes = []
        if type(geometry) is shapely.geometry.multipolygon.MultiPolygon:
            for iPoly, polygon in enumerate(geometry):
                if (iPoly==0 or polygon.area > 0.001):
                    geometrys.append(list(polygon.exterior.coords))
                    geometryTypes.append('polygon')
        elif type(geometry) is shapely.geometry.polygon.Polygon:
            geometrys.append(list(geometry.exterior.coords))
            geometryTypes.append('polygon')
        elif type(geometry) is shapely.geometry.multilinestring.MultiLineString:
            for iLine, line in enumerate(geometry):
                geometrys.append(list(line.coords))
                geometryTypes.append('linestring')
        elif type(geometry) is shapely.geometry.LineString:
            geometrys.append(list(geometry.coords))
            geometryTypes.append('linestring')
        else:
            raise ValueError("Geometry is not a polygon/multipolygon or linestring/multilinestring")
        # print("strI, strLimit, strCentroid: ", strI, strLimit,strCentroid)
        # strLimit = strCentroid
        htmlPoly = ""
        htmlRegion = ""
        # nPoints=0
        for iPoly, polygon in enumerate(geometrys):
            strPointsLabel = "points_"+strI+"_"+str(iPoly)
            geometryType = geometryTypes[iPoly]
            if geometryType == 'polygon':
                htmlPoly += " <polygon id='"+strPointsLabel+"' points= '"
            elif geometryType == 'linestring':
                htmlPoly += " <path fill='none' stroke-width='3' id='"+strPointsLabel+"' d= 'M "
            # nPoints += len(polygon)
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
                htmlRegion += "              adjustRect("+strI+",'text"+strI+"',mouseOverx,'OUT'); \n"
                htmlRegion += "       rects["+strI+"].style.fill='transparent';texts["+strI+"].style.fill='blue';\" >\n"
        htmlRegion += htmlPoly
        htmlRegion += "    <rect transform='translate("+strLimit+")' x='0' y='0' width='100' height='100' stroke='transparent' fill='transparent'></rect> \n"
        htmlRegion += "    <text id='text"+strI+"' x='0' y='50' transform='translate("+strLimit+")' font-family='Verdana' font-size='10' fill='blue'>"+"</text> \n"
        htmlRegion += "</g> \n"
        return htmlPoly,htmlRegion, strLimit,strArea

    def to_html(gdf, lstParams,lstStems,lstStemLabels,width=None):  
        # lstParams = ['geometry_simplified','REGION','CNTYNAME','COVID','percColorCOVID']
        # lstStems = ['REGION','CTYNAME','COVID','percColorCOVID','diseaseDensity','populationDensity']
        # lstStems = ['REGION','CTYNAME','COVID','percColorCOVID','diseaseDensity','populationDensity','zipArea']
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
        ## print("min_x,min_y,max_x,max_y: ", min_x,min_y,max_x,max_y)
        if not width:
            width = 1000
        scale = width / (max_x - min_x)
        height = math.ceil(scale * (max_y - min_y))
        num_regions = gdf.shape[0]
        geometries = list(gdf[geometry_col])
        values = list(gdf[value_col])
        colors = list(gdf[color_col])
        # print("colors: ", colors)
        popl = list(gdf.population)
        ids = list(gdf.REGION)
        disDens = list(gdf.diseaseDensity)
        # print("disDens: ", disDens)
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
                html += "#"+geoType+strID + ' {stroke-width:1; stroke:purple; fill:'+strRGB(colors[i])+';}'
            if geoType=='rivers':
                html += "#"+geoType+strID + ':hover {stroke-width:1; stroke:red; fill:rgba(0,255,255,1.0);}\n'
            else:
                html += "#"+geoType+strID + ':hover {stroke-width:1; stroke:purple; fill:rgba(0,255,255,1.0);}\n'
        html += '</style></head>\n'
        ## print(">>>>   height, width: ", height, width)
        strViewBox = "viewBox='0 0 1600 650'"
        htmlRegions = "<svg onload='init()' "+strViewBox+" width='auto' height='"+str(int(height+100))+"px'>\n\n"
        htmlMouseOvers = "<script>\n"
        htmlMouseOvers += "var mouseOvers = new Array() \n"
        # htmlMouseOverx = "var mouseOverx = new Array() \n"
        htmlMouseOverx = "mouseOverx = ''"
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
            htmlPoly,htmlRegion, strLimit,strArea = to_geometry(geoType, geometries[i],scale,min_x, max_y, strID, labels[i], values[i],strI)
            htmlRegions += htmlRegion
            mouseover = "\""+str(ids[i])
            for ii in range(1,len(lstStems)):
                strStem = lstStemLabels[ii]+str(valStems[ii][i])
                mouseover+= "<tspan x='7' dy='1.1em' font-size='10' fill='black'>"+strStem+"</tspan>"
            mouseover+= "\"\n"
            # htmlMouseOverx+= "  mouseOverx["+str(i)+"] = \""+str(ids[i])+"\"  \n"
            # htmlMouseOverx+= "  mouseOverx["+str(i)+"] = \""+"\"  \n"
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
		    topElement.innerHTML = mouseOverx
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


    def getUScovidData(lstStates,lstSTx,strFile):
#####  COVID BY COUNTY
        strFolder = 'E:/ZIP/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports/'
        print("getting data from:  ", strFolder, strFile)
        csvCovid = pd.read_csv(strFolder+strFile)
        csvCovid = csvCovid[csvCovid.Country_Region=='US']
        csvCovid = csvCovid[(csvCovid.Province_State.isin(lstStates))]
        csvState = csvCovid.Province_State
        csvState = csvState.replace(lstStates,lstSTx)
        csvCovid['STUSPS'] = csvState
        csvCovid = csvCovid[csvCovid.Admin2 != 'Unassigned']
        print("csvCovid.Columns:", csvCovid.columns)
        csvCovid = csvCovid.rename(columns={'Incident_Rate':'Incidence_Rate','Case_Fatality_Ratio':'Case-Fatality_Ratio'})
        csvCovid = csvCovid[['FIPS','Admin2','Province_State','Last_Update','Confirmed','Deaths','Active','Incidence_Rate','Case-Fatality_Ratio','STUSPS']]
        # print("csvCovid.Columns:", csvCovid.columns)
        csvCovid = csvCovid.rename(columns={'Admin2':'CTYNAME','Province_State':'STATE','Confirmed':'COVID'})
        csvCovid = correctCovidData(csvCovid)
        return csvCovid

    def getUSpopData(lstStates,lstSTx):
#####  COUNTY POPULATION ESTIMATES
        strFile = "./county2019/co-est2019-alldata.csv"
        csvPop = pd.read_csv(strFile, sep=',' , encoding='latin-1')[['REGION','STATE','COUNTY','STNAME','CTYNAME','POPESTIMATE2019']]
        csvPop['CTYNAME'] = csvPop.CTYNAME.str.replace(' County','')
        csvPop['CTYNAME'] = csvPop.CTYNAME.str.replace(' Parish','')
        csvPop['CTYNAME'] = csvPop.CTYNAME.str.replace('Fairfax city','Fairfax City')
        csvPop['CTYNAME'] = csvPop.CTYNAME.str.replace('Franklin city','Franklin City')
        csvPop['CTYNAME'] = csvPop.CTYNAME.str.replace('Richmond city','Richmond City')
        csvPop['CTYNAME'] = csvPop.CTYNAME.str.replace('Roanoke city','Roanoke City')
        csvPop['CTYNAME'] = csvPop.CTYNAME.str.replace(' city','')
        csvPop = csvPop[csvPop.COUNTY > 0]
        csvPop = csvPop[(csvPop.STNAME.isin(lstStates))]
        csvPop['FIPS'] = 1000*csvPop.STATE.astype(int) + csvPop.COUNTY.astype(int)
        csvPop = csvPop.rename(columns={'STATE':'STATE_NO','STNAME':'STATE','POPESTIMATE2019':'population'})
        csvPop = correctPopData(csvPop)
        return csvPop

    def getUSmapData(lstStates,lstSTx):
#####  COUNTY MAP
        strFile = './county2019/tl_2019_us_county.shp'
        county = gpd.read_file(strFile)
        county = county[county.STATEFP != '02']
        county = county[county.STATEFP != '15']
        county = county[county.STATEFP < '57']
        county = county.rename(columns={'NAME':'CNTYNAME','INTPTLAT':'LAT','INTPTLON':'LON','ALAND':'area_land','AWATER':'area_water'})
        county['FIPS'] = 1000*county.STATEFP.astype(int)+county.COUNTYFP.astype(int)
        county = county[['FIPS','STATEFP','COUNTYFP','GEOID','CNTYNAME','NAMELSAD','area_land','area_water','LAT','LON','geometry']]
        county['geometry_simplified']=county['geometry'].apply(lambda x:x.simplify(0.0005))
        county['GEO_TYPE'] = 'county'
        return county

    def getUScountyData(lstStates,lstSTx):
        csvCovid = getUScovidData(lstStates,lstSTx,strFileCovidNew)[['FIPS','CTYNAME','STATE','COVID']]
        csvCovidOld = getUScovidData(lstStates,lstSTx,strFileCovidOld)[['FIPS','COVID']]
        csvCovidOld = csvCovidOld.rename(columns={'COVID':'oldCOVID'})
        csvCovid = csvCovid.merge(csvCovidOld,how='inner',on=['FIPS'])
        if qDiffCOVIDcounts:
            diffCOVID = csvCovid.COVID - csvCovid.oldCOVID
            csvCovid.COVID = np.where((diffCOVID>=0.0),diffCOVID,0.0)
        csvPop = getUSpopData(lstStates,lstSTx)
        county = getUSmapData(lstStates,lstSTx)
#####  MERGING
        csvCovid = csvCovid.merge(csvPop,how='inner',on=['STATE','CTYNAME','FIPS'])
        csvCovid = county.merge(csvCovid,how='inner',on=['FIPS'])
        csvCovid = csvCovid.sort_values(['STATE','CTYNAME'])
        return csvCovid

    def getSummaryUSdata(UScovid):
        ## print(UScovid.columns)
        # print(csvCovid)
        #   Case-Fatality_Ratio = 100*Deaths/Confirmed
        #   Incidence_Rate = 100000*Confirmed/POPESTIMATE2019
        gp = UScovid.groupby(['STATE']).agg({'Incidence_Rate':['count','mean','median'],
            'Case-Fatality_Ratio':['mean','median'],'COVID':['sum'],'Deaths':['sum'],'Active':['sum'],'population':['sum']})
        gp.columns=['nCounties','inc_mean','inc_median','ratio_mean','ratio_median','confirm_sum','deaths_sum','active_sum','population']
        gp = gp.reset_index()
        gp['caseFatalityRatio'] = 100.* gp.deaths_sum/gp.confirm_sum
        gp['inc_Ratio'] = 100000.0*gp.confirm_sum/gp.population
        # print("\naggregates on incidence ratio: ")
        # print(gp)
        gp.to_csv('Covid_state_summary.csv')
        corr = gp.corr()
        print(corr)
        corr.to_csv('corr.csv')
        return gp

    def getUSstateData(lstStates,lstSTx):
        state = gpd.read_file('./state2019/tl_2019_us_state.shp')
        # print("state.columns: ", state.columns)
        state = state[(state.STUSPS.isin(lstSTx))][['GEOID','NAME','INTPTLAT','INTPTLON','ALAND','AWATER','geometry','STUSPS']]
        state = state.rename(columns={'GEOID':'REGION','NAME':'CNTYNAME','INTPTLAT':'LAT','INTPTLON':'LON','ALAND':'area_land','AWATER':'area_water'})
        # print("state.columns: ", state.columns)
        # print("list(state.REGION): ", list(state.REGION))
        # print("list(state.STUSPS): ", list(state.STUSPS))
        state['geometry_simplified']=state['geometry'].apply(lambda x:x.simplify(0.0005))
        state['GEO_TYPE'] = 'state'
        ## print("state.columns: ", state.columns)
        ## print("state.head(): \n", state.head())
        #####  STATE WIDE TESTING
        ##  Ignore values - old fillers which are updated later
        strFile = "./state2019/CovidTesting20200627.txt"
        header_list = ["STATE", "N_TESTS", "percent"]
        csvTesting = pd.read_csv(strFile, header=None, sep='\t', encoding='latin-1', names=header_list, thousands=',')
        csvState = csvTesting.STATE
        csvState = csvState.replace(lstStates,lstSTx)
        csvTesting['STUSPS'] = csvState
        ## print("csvTesting.shape: ", csvTesting.shape)
        ## print("csvTesting.columns: ", csvTesting.columns)
        # csvTesting.to_csv('csvTesting.csv')
        state = state.merge(csvTesting,how='inner',on=['STUSPS'])
        return state

    def getUSLakes():
        lakes = gpd.read_file('./waterbodies/USA_Large_Water_Bodies.shp')
        lakes['GEO_TYPE']='lakes'
        lakes = lakes.rename(columns={'OBJECTID':'REGION','NAME':'CTYNAME','SQMI':'area_water'})
        lakes['geometry_simplified']=lakes['geometry'].apply(lambda x:x.simplify(0.0005))
        lakes['COVID'] = -1
        lakes['population'] = 0
        return lakes

    def getUSRivers():
        rivers = gpd.read_file('./waterbodies/USA_Detailed_Water_Bodies.shp')
        rivers['GEO_TYPE']='rivers'
        # print("rivers.columns: ", rivers.columns)
        # print("rivers.FCODE_DESC.value_counts(): ", rivers.FCODE_DESC.value_counts())
        rivers = rivers[rivers.SQMI > 110.0]
        rivers = rivers[rivers.FCODE_DESC == 'Stream/River: Hydrographic Category = Perennial']
        rivers.NAME = "river_"+str(rivers.OBJECTID)
        # print("rivers.FCODE_DESC.value_counts(): ", rivers.FCODE_DESC.value_counts())
        rivers = rivers.rename(columns={'OBJECTID':'REGION','NAME':'CTYNAME','SQMI':'area_water'})
        rivers['geometry_simplified']=rivers['geometry'].apply(lambda x:x.simplify(0.0005))
        # print("US rivers.shape: ", rivers.shape)
        rivers['COVID'] = -1
        rivers['population'] = 0
        rivers['area'] = rivers.area_water
        return rivers

    def getStateRivers():
    # qTest = True
    # if qTest:
        rivers = gpd.read_file('./waterbodies/9ae73184-d43c-4ab8-940a-c8687f61952f2020328-1-r9gw71.0odx9.shp')
        rivers['GEO_TYPE']='rivers'
        # print("rivers.columns: ", rivers.columns)
        # print("rivers.Feature.value_counts(): ", rivers.Feature.value_counts())
        # rivers = rivers[rivers.Feature=='Stream']
        lstRivers = ["Alabama River","Allegheny River","Atchafalaya River","Big River",
                  "Brazos River","Canadian River","Chattahoochee River","Colorado River","Columbia River",
                  "Connecticut River","Cumberland River","Delaware River","Des Moines River","Gila River",
                  "Green River","Holston River","Hudson River","Illinois River","James River",
                  "Kansas River","Kootenay River","Kuskokwim River","Milk River","Mississippi River",
                  "Missouri River","Monongahela River","Niobrara River","North Canadian River","Ohio River",
                  "Ouachita River","Pecos River","Platte River","Potomac River","Red River",
                  "Rio Grande River","Sacramento River","Saint Lawrence River","Salmon river","San Joaquin River",
                  "Snake River","Susquehanna River","Tanana River","Tennessee River","Wabash River",
                  "Willamette River","Yellowstone River"]
        rivers = rivers[rivers.Miles > riverSegMiles]
        rivers = rivers[rivers.Name.isin(lstRivers)]
        #  take out ALASKA...  
        rivers = rivers[rivers.State != 'AK']
        #  set so border rivers are duplicated
        rivers = rivers[rivers.State.str.count('-') < 3]
        isDup11 = rivers[rivers.State.str.count('-')==1].copy()
        isDup12 = isDup11.copy()
        isDup11['STUSPS'] = isDup11['State'].str.extract('(.*)\-',expand=False)
        isDup12['STUSPS'] = isDup12['State'].str.extract('\-(.*)',expand=False)
        isDup21 = rivers[rivers.State.str.count('-')==2].copy()
        isDup22 = isDup21.copy()
        isDup23 = isDup21.copy()
        isDup21[['STUSPS','ST2','ST3']] = isDup21.State.str.split('-',expand=True,n=2)
        isDup22['STUSPS'] = isDup21.ST2
        isDup23['STUSPS'] = isDup21.ST3
        isDup21 = isDup21.drop(columns=['ST2','ST3'])
        rivers = rivers[rivers.State.str.count('-')==0].copy()
        rivers['STUSPS'] = rivers.State
        rivers = rivers.append(isDup11).append(isDup12)
        rivers = rivers.append(isDup21).append(isDup22).append(isDup23)
        rivers['geometry_simplified']=rivers['geometry'].apply(lambda x:x.simplify(0.0005))
        rivers = rivers.sort_values(['STUSPS','Name'])
        rivers['STUSPS_Name'] = rivers.STUSPS + rivers.Name
        rivers = rivers.dissolve(by='STUSPS_Name')
        # print("list(rivers.STUSPS): ", list(rivers.STUSPS))
        rivers = rivers.rename(columns={'OBJECTID':'REGION','Name':'CTYNAME','Miles':'area'})
        rivers.geometry_simplified = rivers.geometry
        # print("State rivers.shape: ", rivers.shape)
        rivers['COVID'] = -1
        rivers['population'] = 0
        rivers = rivers.reset_index()
        return rivers

    UScovid = getUScountyData(lstStates,lstSTx)
    state = getUSstateData(lstStates,lstSTx)
    state['REGION'] = state.REGION.astype(int)

    UScovid['REGION'] = UScovid.STATE_NO.astype(int)
    state_merge = state[['REGION','STUSPS']]
    UScovid = UScovid.merge(state_merge,how='inner',on=['REGION'])
    # state_merge = getUSstateData['
    zipCity = state.append(UScovid)
    # print("list(zipCity.FIPS): ", list(zipCity.FIPS))
    zipCity['REGION'] = np.where((zipCity.GEO_TYPE=='county'),zipCity.FIPS,zipCity.REGION)
    zipCity['REGION'] = zipCity.REGION.astype(int)
    # print("list(zipCity.REGION): ", list(zipCity.REGION))

    if qLakes:
        lakes = getUSLakes()[['REGION','CTYNAME','area_water','geometry','GEO_TYPE','geometry_simplified','COVID','population']]
        zipCity = zipCity.append(lakes)

    if qUSRivers:
        rivers = getUSRivers()[['REGION','CTYNAME','area_water','geometry','GEO_TYPE','geometry_simplified','COVID','population','area']]
        # print("US rivers: ", rivers)
        zipCity = zipCity.append(rivers)


    if qStateRivers:
        rivers = getStateRivers()[['REGION','CTYNAME','geometry','GEO_TYPE','geometry_simplified','STUSPS','COVID','population','area']]
        # rivers = getStateRivers()[['REGION','CTYNAME','area_water','geometry','GEO_TYPE','geometry_simplified']]
        # print("state rivers: ", rivers)
        zipCity = zipCity.append(rivers)

    zipCity = zipCity.reset_index(drop=True)
    if qLimit:
        zipCity = zipCity[zipCity.STUSPS.isin(lstStts)]
    zipCity = zipCity[~(zipCity.geometry.is_empty | zipCity.geometry.isna())]
    zipCity['population'] = np.where((zipCity.population.isna()),-1,zipCity.population)
    zipCity['COVID'] = np.where((zipCity.COVID.isna()),-1,zipCity.COVID)
    zipCity['diseaseDensity'] = np.where((zipCity.COVID!=-1.0), 
              (100.0*zipCity.COVID.astype(float)/zipCity.population.astype(float)).round(3),zipCity.COVID)
    zipCity['zipArea'] = (10000.0*zipCity.area.astype(float)).round(3)
    zipCity['populationDensity'] = (100.0*zipCity.population.astype(float)/zipCity.zipArea).round(3)
    zipCity['percColorCOVID'] = convertToColor(zipCity['diseaseDensity'], minIndicator, maxIndicator)

    ## print("************BEFORE TO_HTML********************")
    bounds = zipCity.geometry.bounds
    x_min = bounds.minx.min()
    x_max = bounds.maxx.max()
    y_min = bounds.miny.min()
    y_max = bounds.maxy.max()
    width = 300
    scale = width / (x_max - x_min)
    height = math.ceil(scale * (y_max - y_min))
    point = [x_max,y_min]
    ## print("width, scale, y_max, x_min: ", width, scale, y_max, x_min)
    width = width * 600.0/height
    #  y_max = y_max * 600.0/height
    scale = scale * 600.0/height
    strBounds = convert(point,scale,x_min,y_max,10000.0)
    ## print("width, scale, y_max, x_min: ", width, scale, y_max, x_min)
    ## print(">>>>>>>>>  strBounds: ", strBounds)
    if qJoinStateCountyLabel:
        zipCity.CTYNAME = zipCity.CTYNAME+", "+zipCity.STUSPS

    lstParams = ['geometry_simplified','REGION','CTYNAME','COVID','percColorCOVID']
    lstStems = ['REGION','CTYNAME','COVID','population','diseaseDensity','populationDensity','zipArea']
    lstStems = ['REGION','CTYNAME','COVID','percColorCOVID','diseaseDensity','populationDensity','zipArea']
    lstStemLabels = ['','','Cases: ','Popl: ','disDens: ','popDens: ','area: ']
    lstStemLabels = ['','','Cases: ','%color: ','disDens: ','popDens: ','area: ']
    if qTextSave:
        lstText = list(lstStems)
        lstText.extend(['area_land','area_water','LAT','LON'])
        zipCityText = zipCity[lstText]
        zipCityText.to_csv("./US_COVID_OUTPUT.csv", index=False)

    # print("zipCity.shape: ", zipCity.shape)
    html = to_html(zipCity,lstParams,lstStems,lstStemLabels,width=width)
    total_bounds = zipCity.total_bounds
    ## print("total_bounds: ", total_bounds)
    ## print("*****  COMPLETED ZIP")

    with open("output_US_EDGE.html", "w") as f: 
        f.write(html) 
    import webbrowser
    from urllib.request import pathname2url
    url = 'file:{}'.format(pathname2url(os.path.abspath('output_US_EDGE.html')))
    webbrowser.open(url)

