library(Rbbg) #Bloomberg Connection

#Connect to Bloomberg API
conn <- blpConnect()

indexes <- c("RTY Index", "SX5E Index", "IBEX Index", "SPX Index", "NKY Index", "UKX Index")

#Get members for index and their RICS
memb_codes <- bds(conn, indexes[6], c("INDX_MEMBERS") )
rics <- paste(memb_codes[ ,1], "Equity", sep= " ")

#Get spots for each member and their first digit
spots <- bdp(conn, rics, c("PX_LAST") )
firstDigit <- as.numeric( substring( spots[ , 1], 1, 1 ) )

#Get histogram for first Digit
histogram <- hist( firstDigit, breaks = 0:9 )

#Benford Law Theoretical Probability
benfordTheoretical <- log10( 1 + 1/(1:9) )

#Result dataframe
results_UKX <- data.frame(FirstDigit = 1:9, Probability = histogram$density, Theoretical = benfordTheoretical)


#For those not having a bloomberg connection
load("BenfordLaw.RData")

#Plot results
plot(results_UKX$Probability, main='Benford Law for stock prices in FTSE100 Index', 
     xlab="First Digit", ylab="Probability", col="green", pch=1, xaxt="n")
axis(1, at=seq(1,9))
lines(results_UKX$Theoretical, col="red", pch=0)
legend("topright", c("Results", "Theoretical"), lty=c(0,1), pch=c(1,0), col=c("green", "red"))