# Map COVID USA
### COVID distribution by counties in the USA or by zip code within Arizona

There are four sets of information provided:  1. sites where information has been obtained or can be obtained, 2. Python programs which read, process, and deliver html files for the United States or the state of Arizona, 3. fragments of the html file which is generated by the Python program, and 4. screen shots of maps created by the Python programs.  

### Challenges and requirements

In order to do investigations on factors associated with COVID-19, you may wish to create maps, whether by county or by zip code.  Ideally you'd like it to be html files and it ought to allow you to hover your mouse over the county and get additional information.  This may seem like an easy task.  After all, there are many attractive mapping programs available on the Internet, some are "free", there are a few examples for each of the features you might wish to make use of, maybe you're thinking, "I should have something up by next week".  

In point of fact, there are few projects more difficult.  Data for counties and zipcodes appear and disappear like ghosts in the night.  A site that was available a week ago is down for service.  Shape files have difficult to find errors in them (you'll be amazed how many are wrong).  The format for files containing COVID-19 data changes depending on the dates, where cases are found and the reporting preferences of each state.  Providers which promise to let you use their code for "free", constantly ask if you'd like to pay.  Code that is supposed to work when you are offline rarely works offline.  Much of the advice provided is out of date.  

There are two requirements to consider here:  data sources and output.  The input files require multiple shapefiles (state/county/zip code/lakes/rivers), labels for the shapefiles, COVID-19 data, and demographic information such as population, income, race/ethnic distributions, and age distributions.  The output files require html code, scripts, and svg code.  

So what might the required tasks be?  Create shape files for U.S. counties, decorate with detailed informations such as waterbodies, get the latest COVID-19 data, download census information, add additional information about counties, and transform the results to html files.  

We will describe:<ol type="1">
	<li>where you can get files and data</li>
	<ol type="a">
		<li>Everything that's free:  https://freegisdata.rtwilson.com/</li>
		<li>Hopkins novel coronavirus data:  https://github.com/CSSEGISandData/COVID-19</li>
		<li>arcgis map coordinates:  https://www2.census.gov/geo/tiger/TIGER2019/</li>
		<li>add additional information about landmarks: https://hub.arcgis.com/datasets/esri::usa-detailed-water-bodies</li>
		<li>census information: https://data.census.gov/cedsci/all?q=county
	</ol>
	<li>how to create your own interactive html file</li>
	<ol type="a">
		<li>define objects</li>
		<li>create mouseOver scripts</li>
		<li>define getElement scripts</li>
		<li>define svg positioning scripts</li>
		<li>define state object polygon shapes and interactions</li>
		<li>define county object polygon shapes and interactions</li>
		<li> define lake object polygon shapes and interactions</li>
		<li> define river path shapes and interactions</li>
	</ol>

<script>
.column {  float: left;  width: 50.00%;  padding: 5px;}
.row::after {  content: "";  clear: both;  display: table;}
</script>

<div class="row">
  <div class="column">
<img src="/images/COVID_12042020.jpg" width="400" height="300">
  </div>
  <div class="column">
<img src="/images/COVID_12182020.jpg" width="400" height="300">
  </div>
</div>

<p align="center">
<img src="/images/COVID_12042020.jpg" width="400" height="300">
<img src="/images/COVID_12182020.jpg" width="400" height="300">
</p>

<p align="center">
<img src="/images/AZ_zipcode_COVID.jpg" width="350" height="350">
</p>

While we quickly recognize if a face is typical f


### Motivation for identifying differences between xrays of healthy lungs and those with pneumonia:
Considerable effort has been applied to building neural nets to discriminate between patients who are healthy and those patients with pneumonia based on x-rays.  An avenue which 
### Citations:
<dl>
<dt> Jason Brownlee, How to Develop a Conditional GAN (cGAN) From Scratch,</dt><dd> Available from https://machinelearningmastery.com/how-to-develop-a-conditional-generative-adversarial-network-from-scratch, accessed January 4th, 2020. </dd>
<dt>Jason Brownlee, How to Explore the GAN Latent Space When Generating Faces, </dt><dd>Available from https://machinelearningmastery.com/how-to-interpolate-and-perform-vector-arithmetic-with-faces-using-a-generative-adversarial-network, accessed January 13th, 2020. </dd>
<dt>Iván de Paz Centeno, MTCNN face detection implementation for TensorFlow, as a PIP package,</dt><dd> Available from https://github.com/ipazc/mtcnn, accessed February, 2020. </dd>
<dt>Jeff Heaton, Jeff Heaton's Deep Learning Course,</dt><dd> Available from https://www.heatonresearch.com/course/, accessed February, 2020. </dd>
<dt>Wojciech Łabuński, X-ray - classification and visualisation</dt>  <dd> Available from 
https://www.kaggle.com/wojciech1103/x-ray-classification-and-visualisation, accessed March, 2020</dd>
<dt>Tory Walker, Histogram equalizer, </dt> <dd>Available from 
https://github.com/torywalker/histogram-equalizer, accessed March, 2020</dd>
</dl>

### Deliverables:
  1.  description of issues identified and resolved within specified limitations
  2.  code fragments illustrating the core of how an issue was resolved
  3.  two Python programs which vectorize face and x-ray images and compare these images producing contrasts

### Limitations and caveates:

  1.  stream:  refers to the overall process of streaming/moving data through input, algorithms, and output of data and its evaluation.
  2.  convergence:  since there are no unique solutions in GAN, convergence is sufficient when there are no apparent improvements in a subjective evaluation of clarity of images being generated.   
  3.  limited applicability:  the methods described work for a limited set of data and cGan problems.
  4.  bounds of model loss:  there is an apparent relationship between mode collapse and model loss - when model loss is extreme (too high or too low) then there is mode collapse.  
  
### Software and hardware requirements:
    - Python version 3.7.3
        - Numpy version 1.17.3
        - Tensorflow with Keras version 2.0.0
        - Matplotlib version 3.0.3
    - Operating system used for development and testing:  Windows 10

#### The process:

 Creating a cGAN as illustration, I provide limited working solutions to the following problems:

<ol type="1">
  <li>can we generate images of female and male faces based solely on embedding labels</li>
  <li>can we create images which point out the differences between typical female and male faces</li>
  <li>can we generate images of x-rays differentiating between healthy lungs and those with bacterial and viral pneumonia</li>
  <li>can we create images which point out the differneces betweeen healthy lungs and those with bacterial and viral pneumonia</li>
  <li>cGan streams and data sources</li>
</ol>


### 1.  can we generate images of female and male faces by alternating only embeddings:

As we saw in https://github.com/tvtaerum/cGANs_housekeeping, it is possible to both create and vertorize images where male versus female faces can be created simply by selecting a corresponding label/embedding.  

### 2. can we create images which point out the differences between typical female and male faces:
In making comparisons between female and male faces, there is considerable advantage to the fact the same weights can be used to create a male face and a female face and the only difference is the label/embedding.  

### 3.  can we generate images of x-rays differentiating between healthy lungs and those with bacterial and viral pneumonia based solely on alternating embeddings?
As we saw in https://github.com/tvtaerum/xray_housekeeping, it is possible to both create and vertorize images where healthy lungs versus viral pneumonia lungs versus bacterial pneumonia lungs can be created simply by selecting a corresponding label/embedding.  

### 4.  can we create images which point out the differences betweeen healthy lungs and those with bacterial and viral pneumonia?
In making comparisons between healthy lungs and lungs with viral or bacterial pneumonia, there is considerable advantage to the fact that the same weights can be used to create the different images and the only difference is the label/embedding.  

###  5.  cGan streams and data sources:
The following is an outline of the programming steps and Python code used to create the results observed in this repository.  There are two Python programs which are unique to this repository and five modelling (.h5) files.   

The recommended folder structure looks as follows:
<ul>
    <li>embedding_derived_heatmaps-master (or any folder name)</li>
	<ul>
	<li> files (also contains two Python programs - program run from here)</li>
	<ul>
		<li> <b>celeb</b></li>
		<ul>
			<li> <b>label_results</b> (contains five .h5 generator model files)</li>
		</ul>
		<li> <b>xray</b></li>
		<ul>
			<li> <b>label_results</b> (contains five .h5 generator model files)</li>
		</ul>
		<li> <b>cgan</b> (contains images from summary analysis of models)</li>
	</ul>
	<li> images (contains images for README file)</li>
	</ul>
</ul>
Those folders which are in <b>BOLD</b> need to be created. 
All Python programs must be run from within the "file" directory. 

#### LICENSE  <a href="/LICENSE">MIT license</a>
