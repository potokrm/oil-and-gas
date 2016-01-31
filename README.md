# oil-and-gas
Oil and gas repo

## The Repo
This repo contains several project spurs, as the idea evolved.  Scott Nguyen, PhD (experienced oil and gas technologist and VP of Technology at Genie Energy) and I collaborated on the project, and received advice from various people in the oil and gas industry.  I started this work in 2013 and continued it on nights and weekends until about 2014.  

Since we've decided not to pursue many of these ideas, I have made several parts of the repo public, which is contained here.

Structure of repo is

1.  production_data_exploration : Notebooks and code for exploring the data
2.  las_reader:  most complicated part, reading generic las files (well logs)
3.  database_create : creating a postges / postgis database
4.  scrape_ndic : code to scrape websites for the data used here

## Idea
In 2012, during the height of the shale oil boom in the US, I spoke with friends in the oil and gas industry about problems they were facing.  One problem of particular interest was increasing the 'probability of success' of drilling a well that would hit oil.  I was told (turned out to be accurate) that approximately 1/3 of wells hit nothing, 1/3 of wells hit small (pay only for themselves), and 1/3 hit big.  Well cost was about \$5-10M each. 

The general process to drill a well is: drill a small hole in the ground and take measurements while boring.  These measurements are called well logs.  If the well log shows promise, then drill a well.  The determine the depth to drill and the techniques (like fracking, number of perforations in the well, etc) to use to extract the maximum amount of oil.  Sometimes they also take rock samples (rock cores) at various depths for laboratory measurements.

From my experience in agriculture, I knew that both federal and state governments in the US often takes (or requires private companies to share) data, then will publish it in the public domain somewhere.  Given my particular expertise in geospatial and statistical analysis, this seemed like an subject 1)  with readily available data, and 2)  aligned with my expertise.  

## Cost
1.  Single EC2 server and S3 for the data storage, about \$30/month if it was on the whole month.  
2.  Premium subscription to the North Dakota Oil and Gas website ~\$120/year 
3.  Private github repo at \$7/mo
4.  Spare time on nights and weekends

## Original High Level Concept (from lowest to highest value, also happens to be from easiest to hardest)
1.  Rock Core-Well Log correlations
    * Inputs: Well Logs
    * Outputs: Core measured properties
    * Goal: Generate more accurate synthetic property logs
    * Value Prop:  Minimize coring needs, more accurate charaterization of future wells.
2.  Well Forecasting
    * Inputs:  Well logs, well design, completion design
    * Outputs:  Oil production curve or cummulative production
    * Goal:  Forecast production of well based on well logs
    * Value proposition:  Identify wells that will be top producers, and identify best completion parameters for a given well
3.  Sweet spotting
    *  Inputs:  Well logs, well design, completion design, 3D seismic, other well productivity
    *  Outputs:  Cummulative production or 'good well/bad well' location
    *  Goal:  Forecast production of an undrilled well location
    *  Value Proposition: Identify high and low performance acreage and/or well location


## Where to get data from?
The oil and gas logs are reported on a state-by-state basis, so starting with the right state is critical.  Different states have different reporting guidelines and infrastructure for storing the data.  There are companies that collect this data already, the leaders are IHS and DrillingInfo, however they are very expensive.  I also found their platforms built 'lookup' well by well, rather than provide analysis in aggregate. 

First, I narrowed down the states to look at based on amount of oil they produced.  I was also interested in recent activity - so states that have increased productivity recently were particularly worth exploring.  With http://www.eia.gov/dnav/pet/pet_crd_crpdn_adc_mbbl_a.htm

<img src="https://s3.amazonaws.com/git-public/oil/intro/petroProductionbyYear.png" width="480">

## Dig Deep in North Dakota 
During the fracking boom, many states started producing oil more quickly.  There were two states that clearly were most impacted:  Texas and North Dakota.  After researching how much data each had, it was clear North Dakota had better data availability.

After purchasing access to the North Dakota web search engine for oil and gas exploration and production:  https://www.dmr.nd.gov/oilgas/, I wrote a webcrawler to scrape the data.  (It would have been expensive to 'purchase' the database from North Dakota.) 

## Well Productivity:  Even worse than expected, about 1/5 of wells are very productive
Monthly and yearly productivity of each well are kept.  Even further, if a well is drilled but no oil is found, the records of the drilling are still in here.  Below I show the distribution of productivity of wells drilled in 2013:

<img src="https://s3.amazonaws.com/git-public/oil/intro/barrels_of_oil_2013_by_well.png" width="480">

What you can clearly see is in 2013, most well produced no oil.  To quantify this further, below is yearly cummulative production (right axis, black curve).  You can see clearly the amount of oil increased rapidly after 2007.  On the left axis, I show the number of wells needed to produce 1/2 of the total output.  Not surprisingly, a small amount of wells produce 1/2 the oil.  In fact, less than 1/5 of the wells active in a year (including dry wells drilled that year) produce 1/2 of the total oil.  

<img src="https://s3.amazonaws.com/git-public/oil/intro/fraction_of_output.png" width="480">

Simultaneously, activity (both number of companies and number of wells were increasing, see plot below.  From a business prospective, this means more potential customers (and there is currently no clear 'leader').  From a technology prospective, if we could collect and analyze everyones data together, we could perhaps provide valuable insights. 

<img src="https://s3.amazonaws.com/git-public/oil/intro/operators_by_year.png" width="480">

## Opportunity:  Learn from others best practices
Unfortunately, the easiest first project:  correlating rock cores to well logs, was not successful due to lack of data.  Basically, the rock core samples were very, very sparse.

The second and third project looked very promising though.  The data from North Dakota was contained in basically 2 states: a standardized web form (a general information page and a production history page) and basically text logs (call LAS files) that contained the well measurements.  

So, once the data was scraped, we had 15,000 drilled wells worth of:

1.  Well productivity
2.  Well location (spatial information)
3.  Well design details like  depth and completion design (perforations, fracking, etc) 
4.  Well logs (LAS files) --- typically contain several measurements, detailed below
    *  Porosity:  How much space in the rock is there for oil, and how easy will it be to extract
    *  Resistivity:  Proxy for oil to water ratio
    *  Nuclear activity:  Oil is slightly radioactive

##Connecting the dots:
Ideally, we would like to use supervised learning techniques and build a training dataset where the well properties are the features and the well productivity is the answer to fit the data to.  One row would be a single well, well design details would be other features.  The well logs would need to be converted into features.  Likely, we would want to look at the well log measurements relative to the place they pumped from (the perforations) -- a sort of 'depth normalization'.  Normalizing the depth to the 'location drilled' (not the 'depth of the well') is likely the right due to 
1.  The production comes from that location - calling it '0' makes sense
2.  Say if the ground were flat in ancient times, all the oil would be at the same 'height from the center of the earth'.  However, if there is topography on the surface (thousands of years of sediment, glaciers and rock formations) that is uneven, we would get different depth wells to hit that 'oil' surface.  Now, likely the 'oil surface' is not flat, so you should look for features in well logs that are 'similar' to big oil producing wells.

An example feature we could extract from the well logs -- something like average value and slope 500 ft above perforations, same below, then move away from the well in both directions.  We could also look at the change in value between the perforated and unperforated areas (likely in sections as well away from the perforations).  There are many ways to look at the data.  But step 2 is to just graph it.

##The Data
I was expecting to find complete well logs (from 0ft to thousands of feet) to be submitted to North Dakota.  I was also expecting many measurements to be taken (radioactivity, resistivity, and porosity, at least).  Unfortunately, only about 10% of wells contained those measurements.  One example is below:

<img src="https://s3.amazonaws.com/git-public/oil/intro/16843-AIG-BCS-CND1_fig.png" width="480">

The dashed lines show the min and max depth of the perforations of the well.  So, importantly, the well log contains data where the oil was pumped from.  Unfortunately, the data only starts at 10000ft, rather than the surface (0 ft), but at least it could work.

The vast majority of well logs, though, explicitly excluded the measurements from the oil producing zone.  Once I saw this, I realized the idea was not possible.  You can see an example below, there is no data between the dashed lines.  In fact, often that data seems to be intentionally removed.

<img src="https://s3.amazonaws.com/git-public/oil/intro/17518-AIG-CND_fig.png" width="480">


##Outlook for future
Lack of data, low oil prices, and changing our own personal interests led us to abandon this project.  I still think there is opportunity to increase both the probability of hitting oil and the productivity of the wells with a technique like this.  For now, it was a fun exploration!




