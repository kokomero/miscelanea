#' GPXTools: A package for reading GPX files and calculate basic statistic of our GPS tracks.
#'
#' The GPXTools package provides a simple interface to read GPX files and calculate basics statistics
#' of our outdoors tracks. The package can calculate speeds, elevation gains, elevation speed,
#' headings and many other data which can be useful for planning mountain activities, training
#' 
#' @section GPXTools functions:
#' readGPX: Reads the GPX file returning a data.frame with space coordenates, elevation and timestamps
#' trackDistance: Calculate distances (deltas and cumulative), detect points where we are moving or still
#' and calculate cumulative moving time.
#' trackSpeed: Calculate instantaneous and average speed and average moving speed
#' trackBearing: Calculate the bearing or heading of the track, indicating the cardinal point where we are

library(XML) #XML parsing
library(RgoogleMaps)
library(SDMTools) #For gradient legends

#' Read a GPX file containing a track recorded by a GPS device.
#' 
#' @param fileName Path to the .gpx file
#' @return A data.frame containing longitude and latitude coordenates, elevations and timestamps
#' @examples
#' track <- readGPX("2013-08-10-Curavacas.gpx")
#' 
readGPX <- function(fileName){
  
  #Read XML Files
  xmlFile <- htmlTreeParse(fileName, error = function (...) {}, useInternalNodes = T)
  
  #Verify we only have one track per file
  if( xpathSApply(xmlFile, path = "count(//trk)", xmlValue) != 1){
    stop("Only one track per .gpx is supported")   
  }
  
  #Perform XPath queries to extract fields
  #Read elevation, timestamps and coordenates
  elev <- as.numeric(xpathSApply(xmlFile, path = "//trk[1]/trkseg/trkpt/ele", xmlValue) )
  times <- as.POSIXct(xpathSApply(xmlFile, path = "//trk[1]/trkseg/trkpt/time", xmlValue), format="%Y-%m-%dT%H:%M:%SZ")
  coords <- xpathSApply(xmlFile, path = "//trkpt", xmlAttrs)
  
  # Extract latitude and longitude from the coordinates
  lats <- as.numeric(coords["lat",])
  lons <- as.numeric(coords["lon",])
  
  # Put everything in a dataframe
  data.frame(Lon = lons, Lat = lats, Ele = elev, DateTime = times)  
}
