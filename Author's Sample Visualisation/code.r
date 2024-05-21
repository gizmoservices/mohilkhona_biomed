library(mvtnorm)
Sigma0 <- 0.5* (-1)^abs(outer(1:10,1:10,"-"))
Sigma1 <- array(0.5,dim=c(10,10))
adjM <- array(1,dim=c(10,10))
adjM[lower.tri(adjM,diag=T)] <- 0
adjM[1,5] <- adjM[3,6] <- adjM[4,8] <- 0
adjM
##       [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8] [,9] [,10]
##  [1,]    0    1    1    1    0    1    1    1    1     1
##  [2,]    0    0    1    1    1    1    1    1    1     1
##  [3,]    0    0    0    1    1    0    1    1    1     1
##  [4,]    0    0    0    0    1    1    1    0    1     1
##  [5,]    0    0    0    0    0    1    1    1    1     1
##  [6,]    0    0    0    0    0    0    1    1    1     1
##  [7,]    0    0    0    0    0    0    0    1    1     1
##  [8,]    0    0    0    0    0    0    0    0    1     1
##  [9,]    0    0    0    0    0    0    0    0    0     1
## [10,]    0    0    0    0    0    0    0    0    0     0

EDGE <- which(adjM!=0, arr.ind=T)
head(EDGE)
##      row col
## [1,]   1   2
## [2,]   1   3
## [3,]   2   3
## [4,]   1   4
## [5,]   2   4
## [6,]   3   4

set.seed(2017)
size0 <- size1 <- 50
class0 <- rmvnorm( n = size0, sigma = Sigma0,method = "svd")
class1 <- rmvnorm( n = size1, sigma = Sigma1,method = "svd" ) 
dataset <- rbind(class0,class1)
classLabel <- c(rep(0,size0),rep(1,size1))

difnet <- jdinac(EDGE=EDGE,classLabel=classLabel,DataFit=dataset,DataPre=dataset,nsplit=10,nfolds=5)
head(difnet$yPre)
## [1] 3.893804e-01 3.459244e-08 9.624137e-07 8.148533e-09 4.774174e-07
## [6] 3.384799e-05

head(difnet$Eset)
##    row col numb
## 1    1   2   20
## 3    2   3   16
## 5    2   4   14
## 6    3   4   13
## 11   2   6   13
## 21   2   8   13
