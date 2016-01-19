experiment2 <- read.csv('experiment2_kai.csv', header=T, sep=",")

#input: experiment2
#output: 8 column. The proportion of improved.
#condition1 : fixed = 0 and other are not 0
#condition2 : fixed != 0 and other are better than fixed

#so for each column , I will calculate : how many times it is better than fixed, and how much percent it is better.


#output example : all 0 -> [-1] * 8
#fixed = 0 but not all 0 -> ok
#fixed != 0  

pro_imp <- function(col) {
	ans <- c(0,0,0,0,0,0,0,0,0)
	if (col[1] == 0 ){
		flag <- -1
		for (i in 2:9) {
   			if (col[i] > 0) {
   				ans[i] <- 1#is improved by me!
   				flag <- 1
   			}
   			else {ans[i] <- -1}#not improved by me :(
   		}
   		ans[1] <- flag#is improved
	}
	else{
		fixed <- col[1]
		flag <- 0
		for (i in 2:9) {
   			if (col[i] > fixed) {
   				ans[i] <- col[i]/fixed - 1.0#is improved by me! how many?
   				flag <- 1
   			}
   			else {ans[i] <- -1}#not improved by me :(
   		}
   		ans[1] <- flag
	}
	return(ans)
}
result <- apply(experiment2,1, pro_imp)

type <- result[1,]
type <- type[which(type != -1)]#del invaild example(all 0): vaild example
type0 <- type[which(type == 0)]#not improved
type1 <- type[which(type == 1)]#improved

type_result <- c(length(type) , length(type0) , length(type1))
#[1] 818 252 566


all_result = array(0.0,dim=c(8,2))

for (i in 2:9){
	temp <- result[i,]
	temp <- temp[which(temp != -1)]#del not improved : be improved
	improved_number <- length(temp)
	all_result[i-1,1] <- improved_number
	all_result[i-1,2] <- mean(temp)*100.0
}

#     [,1]     [,2]
#[1,]  251 1.409310
#[2,]  228 1.345434
#[3,]  266 4.194524
#[4,]  181 4.618206
#[5,]  177 5.962361
#[6,]  247 4.358419
#[7,]  158 5.826388
#[8,]  166 6.138065
#make a table here(in latex)!


plot(all_result,xlim=c(150,280),ylim=c(0,7),main="Performance of 8 conditions in 566 total improved cases", xlab="Improved cases", ylab="Average improvement ratio (in % of fixed-fixed)")
text(all_result, labels = c("fixed,strong","fixed,one_weak","strong,fixed","strong,strong","strong,one_weak","one_weak,fixed","one_weak,strong","one_weak,one_weak"), cex= 0.7,pos=3)












