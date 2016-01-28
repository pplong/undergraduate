experiment3 <- read.csv('experiment3_kai-last-1.csv', header=T, sep=",")
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




 #fixed_count     version3_1      version3_2      version3_3      version4_1
 #Min.   :   0   Min.   :    0   Min.   :    0   Min.   :    0   Min.   :    0
 #1st Qu.:1073   1st Qu.: 3428   1st Qu.: 4685   1st Qu.: 6913   1st Qu.: 2092
 #Median :1947   Median : 6042   Median : 8059   Median :12236   Median : 3678
 #Mean   :2113   Mean   : 6550   Mean   : 8837   Mean   :13062   Mean   : 4100
 #3rd Qu.:2984   3rd Qu.: 9121   3rd Qu.:12189   3rd Qu.:17849   3rd Qu.: 5738
 #Max.   :9053   Max.   :33188   Max.   :47578   Max.   :64193   Max.   :22713
 #  version4_2      version4_3    is_equal
 #Min.   :    0   Min.   :    0   True:1001
 #1st Qu.: 2816   1st Qu.: 3064
 #Median : 4903   Median : 5341
 #Mean   : 5456   Mean   : 5867
 #3rd Qu.: 7374   3rd Qu.: 8014
 #Max.   :30969   Max.   :36683