experiment1 <- read.csv('experiment1.csv', header=T, sep=",")

plot(experiment1$Full_search,experiment1$Skyline,main="Relationship of step numbers between full search and skyline algorithm", xlab="full search", ylab="skyline algorithm")

cor(experiment1$Full_search,experiment1$Skyline)

#[1] 0.1814083