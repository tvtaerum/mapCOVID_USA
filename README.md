# Map COVID USA
### COVID distribution by counties in the USA or by zip code within Arizona

Let me first point out that there is no explicit or implicit criticism of any work which has been done in reporting the spread of SAR-CoV-2.  It is an enormously difficult task and few people realize how many challenges have to be overcome to do a reasonable job of reporting.  The best way to find out, of course, is to try to map the spread of the infections for your own enlightenment.  

There are four sets of information provided:    

1. We will discuss a little bit about where to get your shapefiles and data.  The data and sources of shapefiles changes month to month - a site which is reliable one month has major issues the next month.  

2. Two Python programs are provided with little documentation.  The programs reads in the data, creates the shape files, colors the shape files and labels them, and generates the HTML file to express the information read in.  Reading the Python programs tells you how it works.

3. Fragments of the HTML file are provided with some description and explanation.

4. Screen shots of the maps demonstrate that the Python programs works for the limited applications I am interested in.   

### Challenges and requirements

In order to do investigations on factors associated with and disease, you may wish to create maps, whether by county or by zip code.  Ideally you'd like it to be html files and it ought to allow you to hover over the county and get additional information.  While there are many attractive mapping programs available on the Internet and some are "free", you may be astonished at how frequently they are wrong or don't work.  

The primary challenge has to do with data disappearing and their formats changing day to day.  A site that was available a week ago is down for service.  Shape files have difficult to find errors in them (and some are very wrong).  The format for files containing COVID-19 data changes depending on the dates, where cases are found and the reporting preferences of each state.  Providers which promise to let you use their code for "free", constantly ask if you'd like to pay.  Code that is supposed to work when you are offline rarely works offline.  Much of the advice provided on the Internet for many packages is going out of date in a fast changing world.  

There are two requirements to consider here:  data sources and output.  The input files require multiple shapefiles (state/county/zip code/lakes/rivers), labels for the shapefiles, COVID-19 data, and demographic information such as population, income, race/ethnic distributions, and age distributions.  The output files require html code, scripts, and svg code.  

The required tasks are:  Create shape files for U.S. counties, decorate with detailed informations such as waterbodies, get the latest COVID-19 data, download census information, add additional information about counties, and transform the results to html files.  

We will describe:<ol type="1">
	<li>where you can get files and data</li>
	<ol type="a">
		<li>URL's to lots of geo info that's free:  https://freegisdata.rtwilson.com/</li>
		<li>Hopkins novel coronavirus data:  https://github.com/CSSEGISandData/COVID-19</li>
		<li>some arcgis map coordinates:  https://www2.census.gov/geo/tiger/TIGER2019/</li>
		<li>additional information about landmarks: https://hub.arcgis.com/datasets/esri::usa-detailed-water-bodies</li>
		<li>census information: https://data.census.gov/cedsci/all?q=county
		<li>zipcode information:  https://www.azcentral.com/in-depth/news/local/arizona-health/2020/03/20/arizona-coronavirus-map-county-county-look-covid-19-cases</li>
	</ol>
	<li>what the interactive html file you create must look like to work</li>
	<ol type="a">
		<li>define objects</li>
		<li>create mouseOver scripts</li>
		<li>define getElement scripts</li>
		<li>define svg positioning scripts</li>
		<li>define state classes for polygon shapes and interactions</li>
		<li>define county classes for polygon shapes and interactions</li>
		<li> define lake classes for polygon shapes and interactions</li>
		<li> define river classes for path shapes and interactions</li>
	</ol>

	
|Three weeks COVID ending December 14, 2020                        |Three weeks COVID ending December 28, 2020                        |
|:-----------------------------------------------------------------|:-----------------------------------------------------------------|
| <img src="/images/COVID_12142020.jpg" width="400" height="280"> | <img src="/images/COVID_12282020.jpg" width="400" height="280"> |


|Arizona COVID-19 ending July 12, 2020   |
|----------------------------------------|
|<img src="/images/AZ_zipcode_COVID.jpg" width="350" height="350">|

**1.** The first requirement is defining all the objects in the map.  Here we define States, Counties, Lakes and Rivers.  
When the stream is run and the html file is complete, there are 48 definitions of States, 3107 definitions of Counties, 8 definitions of major Lakes, and 149 definitions of major Rivers.  There are, in total, 3312 lines of definitions.  
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a text version of these fragments.*  
|Styles to create Objects and initial properties|
|----------------------------------------|
|<img src="/images/styleToDefineObjects.jpg" width="600" height="300">|

**2.** The second requirement is defining all the "mouse overs" for 48 States, 3107 Counties, 8 major Lakes, and 149 major Rivers.  The lines go beyond the end of the screen and are about 470 bytes long.  There are 3312 lines of instruction of what to do when there is a "mouse over".  
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a complete text version of these fragments.*  
|Script to handle Mouse hovering   |
|----------------------------------------|
|<img src="/images/scriptToDefineMouseOvers.jpg" width="600" height="300">|

**3.** The third requirement is a script which creates an array of html network locations for 48 States, 3107 Counties, 8 Lakes, and 149 Rivers.  These are used to identify which object is being pointed to and load the appropriate data for each State, County, Lake or River.  
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a text version of these fragments.*  
|Script to define arrays   |
|----------------------------------------|
|<img src="/images/scriptToDefineArrays.jpg" width="600" height="300">|

**4.** Next, we create a script with resizes labels for mouse hovers.  When a mouse hovers over an object, the program has to move the object to the front in order to be observed.  Other objects are hidden.  Given the data to be displayed, the program has to fit boundaries around the data.  
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a text version of these fragments.*  
|Script to adjust size to fit label and data|
|----------------------------------------|
|<img src="/images/adjustRectsToFitText.jpg" width="350" height="325">|

**5.** When the mouse hovers over an object, the browser has to be instructed on which objects move up so they can be seen and which objects get pushed to the bottom so they are hidden.  .  
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a text version of these fragments.*  
|Script to raise or lower Objects so they can be seen or hidden   |
|----------------------------------------|
|<img src="/images/scriptToRaiseOrLowerPolygon.jpg" width="350" height="100">|

**6.** This small svg simply directs the action of the browser when the HTML file is first brought up.  
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a text version of these fragments.*  
|svg initialization function   |
|----------------------------------------|
|<img src="/images/svgInitializeArraysOnLoad.jpg" width="300" height="20">|

**7.** The classes for the simple mainland states are defined here.  Some states require a single polygons to define their edges.  The definition of edges for a state can be 57,000 bytes long.  Typically 12 lines of data are required to define a State Class.
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a text version of these fragments.*  
|Sample of Class to create simple State polygon   |
|----------------------------------------|
|<img src="/images/classToCreateSimplePolygon.jpg" width="450" height="200">|

**8.** The classes for the complex states are defined here.  Some states require multiple polygons to define their edges.  The same strategy is used when defining counties made up of multiple polygons.  The definition of edges for a state can be 57,000 bytes long.  More than 12 lines of data are required to define a complex State Class.
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a complete text version of a fragment.*  
|Sample of Class to create State made up of many polygons  |
|----------------------------------------|
|<img src="/images/classToCreateMultiPolygon.jpg" width="450" height="200">|

**9.** The classes for the 3107 counties are defined here.  The definition of edges for a county can be 57,000 bytes long.  Typically 12 lines of data are required to define a County Class.  
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a text version of a fragment.*  
|Sample of Class to create one of many Counties   |
|----------------------------------------|
|<img src="/images/classToCreateCounty1001.jpg" width="450" height="200">|

**10.** The 8 major lakes play an important role in defining the edges of counties and states.  The edges of the lakes are defined here.  Typically 12 lines of data are required to define a Lake Class.  
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a text version of a fragment.*  
|Sample of Class to create one of many Lakes   |
|----------------------------------------|
|<img src="/images/classToCreateLake30179.jpg" width="450" height="200">|

**11.** Last of all, we create the classes for the 149 major rivers in the U.S..  Rivers are paths or segments which are jointed to one another. Multiple lines of data are required to define a River Class.   
*Refer to the file mapCOVID_USA/files/FRAGMENTS_output_US_edge.html for a text version of a fragment.*  
|Sample of Class to create one of many rivers   |
|----------------------------------------|
|<img src="/images/classToCreateRiver26838.jpg" width="450" height="250">|



### Motivation for creating maps using State, County, Lake and River polygons and paths.  
As previously indicated, you may wish to develop your own maps for many different reasons including tracking COVID-19.  One advantage of HTML files is you can ZIP the files and then email them to other people and they can examine the results without having to use the Internet.  You can test the veracity of statements made by public officials and draw your own conclusions.  It's important to validate your results against official publications.  

### Citations:
<dl>
<dt> Hopkins data - used for validation and verification </dt><dd> Available from https://coronavirus.jhu.edu/us-map, last accessed January 1st, 2021. </dd>
<dt> John Hopkins data download </dt> <dd> Download from https://github.com/CSSEGISandData/COVID-19, last accessed January 1st, 2021. </dd>
<dt> Lancet Article for any use of data in publication </dt> <dd> https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30120-1/fulltext  </dd>
<dt> Arizona ZIPcode data </dt><dd>https://www.azcentral.com/in-depth/news/local/arizona-health/2020/03/20/arizona-coronavirus-map-county-county-look-covid-19-cases</dd>
</dl>

### Deliverables:
  1.  two Python programs to create maps for mainland USA based on counties and Arizona based on zip code polygons
  2.  html fragments illustrating the contents of an html file
  3.  descriptions of the contents of an html file

### Limitations and caveates:

  1.  stream:  refers to the overall process of streaming/moving data through input, algorithms, and output of data and its evaluation.
  2.  limited applicability:  the methods described work for a limited set of data.
  3.  lack of completeness:  the code works for my requirements and no promise is made about its application, usefulness, or accuracy to other applications  
  
### Software and hardware requirements:
    - Python version 3.7.3
        - Numpy version 1.17.3
        - Matplotlib version 3.0.3
	- Pandas version 
	- geoPandas version
	- shapely version 
    - Operating system used for development and testing:  Windows 10

#### LICENSE  <a href="/LICENSE">MIT license</a>
