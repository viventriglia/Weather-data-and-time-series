# Weather data and time series

*Example time-series analysis portfolio, using Python (NumPy, Matplotlib)*

## Introduction
We collect weather data from [NOAA](https://www.noaa.gov/) and use the integrated [GHCN-Daily](https://www.ncdc.noaa.gov/ghcn-daily-description) database of daily climate summaries from stations across the globe. This means looking at variables such as minimum and maximum temperatures, precipitations, snowfalls, and so on.
We download a list of stations and use it to locate temperature data for different cities. We manage missing values and smooth time series in order to enhance the information out of the noise. Finally, we create some visualisations of daily temperatures.

## The database
By plotting longitude against latitude, we can get a feel of the global coverage of the database.
<p align="center">
  <img alt="locations of weather stations" src="locations.png" width="100%">
  <br>
    <em>Global coverage of weather stations</em>
</p>

## Dealing with missing information
Next, we should face the problem of making sense of missing values in the database. This is a common aspect in data analysis and actually we could just ignore them. If we do need an uninterrupted series of numbers, we could set the missing entries, for istance, to the average of the respective column. A more sophisticated approach to restore missing values is given by [interpolation](https://numpy.org/doc/stable/reference/generated/numpy.interp.html), which selects the "good" data points and returns estimated values for the missing ones, that are interpolated linearly by fitting segments between existing data points. Here we follow this approach, which is actually rather conservative, hence intrinsically safe.

## Dealing with noise
A Time series is a sequence of values organised chronologically, usually with equal cadence.
Looking directly at the data from the series is informative, but one may see lots of noise in the form of rapid variations between one day and the next; this may result in covering up underlying trends. To limit the noise, one can smooth the data. The premise of data smoothing is that one is measuring a variable that is both slowly varying and also corrupted by random noise, so that smoothing (*i*) increases the signal-to-noise ratio and (*ii*) exposes the slow, long-term behaviour underneath the oscillations.
We follow a simple, direct approach to smoothing by replacing each value with the average of a set of its neighbours. Indeed, since nearby points measure very nearly the same underlying value, averaging can reduce the level of noise without (much) biasing the value obtained. Here we use a so-called "box filter": a smoothing mask with positive, normalised entries that add up to 1. To this end, it proves useful to use [cross-correlation](https://numpy.org/doc/stable/reference/generated/numpy.correlate.html).

## Daily temperatures
We try this out, for instance, over multiple years for Roma Ciampino, an international airport just outside Rome, to check if the climate is stable. Quite so.
<p align="center">
  <img alt="climate in Rome for different years" src="ROMA.png" width="100%">
  <br>
    <em>Climate in Rome for three different years</em>
</p>
Next, we wish to compare cities in different climates. To this end, we look over four US cities, namely New Orleans (Louisiana), New York City (New York), San Diego (California) and Minneapolis (Minnesota), focusing on the year 2019.
<p align="center">
  <img alt="climate in four different US cities" src="4_US_cities.png" width="100%">
  <br>
    <em>Climate in four US cities in 2019</em>
</p>
Note that the different shapes of the curves reflect the fact that [insolation](https://www.geog.ucsb.edu/ideas/Insolation.html) is not constant over the surface of the Earth: as the Earth orbits around the Sun, the insolation is concentrated in the northern hemisphere (summer in the northern hemisphere) and then in the southern hemisphere (winter in the northern hemisphere). On a yearly average, the equatorial region receives the most insolation, so we expect it to be the warmest – as it is.
