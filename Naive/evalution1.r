experiment1 <- read.csv('experiment1-last.csv', header=T, sep=",")
summary(experiment1)
#plot(experiment1$Full_search,experiment1$Skyline,main="Relationship of step numbers between full search and skyline algorithm", xlab="full search", ylab="skyline algorithm")

#cor(experiment1$Full_search,experiment1$Skyline)




 # Full_search          Skyline       is_equal       time1
 #Min.   :       0   Min.   :   0.0   True:100   Min.   : 0.000
 #1st Qu.:  600395   1st Qu.: 802.5              1st Qu.: 3.551
 #Median : 2019159   Median :1633.0              Median :11.226
 #Mean   : 2999026   Mean   :1974.1              Mean   :16.729
 #3rd Qu.: 4174770   3rd Qu.:2798.8              3rd Qu.:21.724
 #Max.   :12648954   Max.   :6302.0              Max.   :68.304
 #    time2
 #Min.   :0.0000
 #1st Qu.:0.2188
 #Median :0.4787
 #Mean   :0.5128
 #3rd Qu.:0.7052
 #Max.   :1.5587

#[1] 0.1814083