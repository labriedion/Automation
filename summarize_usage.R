#Summarizes the usage space for each OMERO user - a PPMS user account is also needed

library(doBy)

data=read.table("/home/omero/Documents/omerospace.log")
names(data) = c("Date", "User", "Amount")

#get the number of unique days logged, which gives the number of days in the month, this allows dividing all the usage by the total number of days.
numberDays <- length(unique(data$Date))

#converts to GBs
data$Amount <- data$Amount / 1048576

#Using the mean won't work because the user folder might not be present everyday of the month if its empty or not created yet.
summary = summaryBy(Amount ~ User, data=data, FUN = sum)
summary$Amount.sum <- summary$Amount.sum / numberDays
summary$Amount.sum <- round(summary$Amount, digits = 2)

write.table(summary, "/home/omero/Documents/summary.csv", sep=",", row.names=FALSE, col.names=FALSE, quote=FALSE)
