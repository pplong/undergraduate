experiment3 <- read.csv('experiment3_kai.csv', header=T, sep=",")
experiment3 <- experiment3[,c(1:3)]

fixed <- mean(experiment3$fixed_count)
flexible <- mean(experiment3$version3_count)
bure <- mean(experiment3$version4_count)

print(flexible/fixed)
print(bure/flexible)
print(bure/fixed)

#[1] 6.365288
#[1] 0.4482957
#[1] 2.853531

#plot(experiment3$fixed_count,experiment3$version3_count, experiment3$version4_count,main="Relationship of step numbers between full search and skyline algorithm", xlab="full search", ylab="skyline algorithm")
#plot(experiment3$fixed_count,experiment3$version3_count,xlab="Fixed functional requiments", ylab="Flexible functions",main="Relationship of step numbers between fixed functional requiments and flexible functions")
#plot(experiment3$version3_count,experiment3$version4_count,xlab="Flexible functions", ylab="Bure algorithm",main="Relationship of step numbers between Fixed functional requiments and Bure algorithm")
#plot(experiment3$fixed_count,experiment3$version4_count,xlab="Fixed functional requiments", ylab="Bure algorithm",main="Relationship of step numbers between fixed functional requiments and Bure algorithm")
