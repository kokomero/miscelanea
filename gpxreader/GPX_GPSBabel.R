
readGPSBabel <- function (i = "garmin", f = "usb:", type = "w", 
                          invisible = TRUE, ...){
  
  GB <- Sys.which("gpsbabel")
  
  if (nchar(GB) == 0 || !file.exists(GB))
    stop("gpsbabel not found")
    
  if (.Platform$OS.type == "windows")
    gpsdata <- system(paste(GB, " -i ", i, " -f ", f, " -", type,
                            " -o tabsep -F -", sep = ""), 
                      intern = TRUE, 
                      invisible = invisible)
    
  else gpsdata <- system(paste(GB, " -i ", i, " -f ", f, " -", type,
                               " -o tabsep -F -", sep = ""), 
                         intern = TRUE)
      
  if (any(grep("Can't init", gpsdata)))
    stop("Cannot read GPS: check connexion")
  
  gpsdf <- read.table(con <- textConnection(gpsdata), fill = TRUE, ...)
  close(con)
 
  gpsdf
}
