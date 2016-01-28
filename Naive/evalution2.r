experiment2 <- read.csv('experiment2_kai-last.csv', header=T, sep=",")

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

fangan <- function(col){#生成方案
	if (col[1] == 1){
		if (col[4] < col[5]){
			col[4] <- -1
		}
		if (col[2] < col[5]){
			col[2] <- -1
		}
		if (col[6] < col[5] | col[6] < col[4]){
			col[6] <- -1
		}
		if (col[8] < col[5] | col[8] < col[2]){
			col[8] <- -1
		}
		if (col[3] < col[6] | col[3] < col[4] | col[3] < col[5] | col[3] < col[2]){
			col[3] <- -1
		}
		if (col[7] < col[8] | col[7] < col[2] | col[7] < col[5] | col[7] < col[4]){
			col[7] <- -1
		}
		for (i in 2:8){
			if (col[9] < col[i]){
				col[9] <- -1
			}
		}
	}
	return (col)
}

result1 <- apply(result,1, fangan)

type <- result1[,1]
type <- type[which(type != -1)]#del invaild example(all 0): vaild example
type0 <- type[which(type == 0)]#not improved
type1 <- type[which(type == 1)]#improved

type_result <- c(length(type) , length(type0) , length(type1))
#> type_result
#[1] 828 271 557


#all_result = array(0.0,dim=c(8,2))


c1 <- 0 #count for strong
v1 <- 0 #improved value for strong
c2 <- 0 #count for second strong
v2 <- 0 # 
c3 <- 0 #count for all
v3 <- 0

for(k in (1:1001)){

	temp <- result1[k,]
	if (temp[1] == 1){#be improved

		if (temp[4] > 0 | temp[5] > 0 | temp[2] > 0){
			c1 <- c1 + 1
			for (i in c(4,5,2)){
				if(temp[i] > 0){
					v1 <- v1 + temp[i]
				}
			}
		}

		if (temp[4] > 0 | temp[5] > 0 |temp[2] > 0 | temp[6] > 0 |temp[8] > 0){
			c2 <- c2 + 1
			for (i in c(4,5,2,6,8)){
				if(temp[i] > 0){
					v2 <- v2 + temp[i]
				}
			}
		}

		if (temp[4] > 0 | temp[5] > 0 |temp[2] > 0 | temp[6] > 0 |temp[8] > 0 |temp[3] > 0 | temp[7] > 0 |temp[9] > 0){
			c3 <- c3 + 1
			for (i in c(4,5,2,6,8,3,7,9)){
				if(temp[i] > 0){
					v3 <- v3 + temp[i]
				}
			}
		}
	}
} 
print(c1)
print(v1/c1)

print(c2)
print(v2/c2)

print(c3)
print(v3/c3)

#[1] 453
#[1] 0.05089129
#[1] 485
#[1] 0.08827387
#[1] 566
#[1] 0.1180829


#[1] 438
#[1] 0.0647594
#[1] 467
#[1] 0.1171189
#[1] 557
#[1] 0.1604719









#unused
if (F){

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

}










