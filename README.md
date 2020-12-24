# Map COVID USA
### COVID distribution by counties in the USA


At a certain point you may wish to post maps of the county by county distribution of SARS-CoV-2.  It may have seemed like an easy task.  Create shape files for U.S. counties from https://www.arcgis.com/home/ and https://www2.census.gov/geo/tiger/TIGER2019/COUNTY/, decorate with detailed informations such as waterbodies from https://hub.arcgis.com/datasets/esri::usa-detailed-water-bodies, get the latest COVID-19 data from https://github.com/CSSEGISandData/COVID-19, download census information from https://www2.census.gov/geo/tiger/TIGER2019/ in order to adjust data for information such as populations density, add additional information about landmarks from https://hub.arcgis.com/datasets/esri::usa-detailed-water-bodies, and transform the results to html files.  What could be easier?  

In point of fact, there are few things more difficult.  Files for census information appear and disappear like ghosts in the night.  Shape files have difficult to find errors in them.  The format for files containing COVID-19 data changes depending on where cases are found and the preferences of each state.  Providers which promise to let you use their code for "free", constantly pester you to pay.  Code that is supposed to work when you are offline is tempermental and rarely works as promised.  Much of the advice provided is out of date and for older versions of software and data sources.  

We will describe:<ol type="1">
	<li>where you can get files and data</li>
	<ol type="a">
		<li>Everything that's free:  https://freegisdata.rtwilson.com/</li>
		<li>Hopkins novel coronavirus data:  https://github.com/CSSEGISandData/COVID-19</li>
		<li>arcgis map coordinates</li>
		<li>add additional information about landmarks</li>
		<li>census information
		<li>creation of html files</li>
	</ol>
	<li>measures you can create on your own</li>
</ol>

There are three examples of outcomes from the use of SOM below.  It's worth examining these results and discussing them to see the utility of these kinds of segmentation.  

The first illustrates the results for the classis Iris data.  The data is classic for two reasons.  First, it is used to demonstrate how good an algorithm is at grouping or segmenting objects in comparison to other algorithms.  Second, the Iris genus has about 300 species, of which versicolor is an allopolyploidy of setosa and virginica - multiple genomes from different species operating within one plant.  The result is that any segmentation may reflect ploids found within Iris versicolor.  

For this matrix, I provide background colors and textual displays within each cells as standard output for this Python stream - the stars and summaries on the left are additional decorations.  The matrix consists of 3 dimensions measuring 3 by 3 by 4 cells.  At the bottom of the matrix is the order of the four most important measures:  petal width, petal length, sepal length, and sepal width.  The RGB colors reflect combination of the three most important measures.  The colors are grayish reflecting the fact that the top three measures are highly correlated with one another - after all, physical sizes are generally correlated with one another.  

In doing segmentation, I generally prefer SOM over G-means.  In my experience, G-means has a tendency to produce few groups which have a very uneven distribution of objects.  As an example, there might be 2% in one group 5% in a second, and 93% in a third group.  While 3 groups might be reasonable for the classic Iris data, the display of SOM provides an interpretable basis for deciding if any particular number of groups is really the best.  Beyond this, using multi-dimensional SOM allows for interpretation of dimensions.  

<p align="center">
<img src="/images/COVID_12042020.jpg" width="500" height="350">
</p>


<p align="center">
<img src="/images/COVID_12182020.jpg" width="500" height="350">
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
