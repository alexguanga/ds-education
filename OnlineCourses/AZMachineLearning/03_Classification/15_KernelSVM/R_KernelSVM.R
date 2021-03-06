# Kernel SVM

# Importing the dataset
df <- read.csv("./archive/Social_Network_Ads.csv")
df <- subset(df, select=c("Gender", "Age", "EstimatedSalary", "Purchased"))

# Changing the categorical data of gender
df$Gender <- factor(df$Gender,
                    levels = c('Male','Female'),
                    labels = c(0,1))

######################################################
# Splitting the dataset into training and testing
######################################################
library(caTools)
set.seed(123)
split <- sample.split(df$Purchased, SplitRatio = 0.8)

training.set <- subset(df, split == TRUE)
testing.set <- subset(df, split == FALSE)

# Checking the datatype of the variables
sapply(testing.set, class)

# Gender is a factor, must change it to integer
training.set$Gender <- as.numeric(training.set$Gender)
testing.set$Gender <- as.numeric(testing.set$Gender)


######################################################
# Feature Scaling
######################################################
testing.set[, c("Age","EstimatedSalary")] <-  
  scale(subset(testing.set, select = c("Age", "EstimatedSalary")))

training.set[, c("Age","EstimatedSalary")] <- 
  scale(subset(training.set, select = c("Age", "EstimatedSalary")))

####
# Fitting the SVM
####
library(e1071)

kernels <- c('polynomial', 'radial', 'sigmoid')
for (kernel in kernels){
  classifier <- svm(Purchased ~.,
                    data = training.set,
                    type = 'C-classification',
                    kernel = kernel)
  
  # Predicting the results
  y.pred <- predict(classifier, newdata = testing.set[,c("Age", "EstimatedSalary", "Gender")])
  
  # Make the confusion matrix
  confusion.matrix <- table(testing.set$Purchased, y.pred)
  print(kernel)
  print(confusion.matrix)
}


####
# Visualizing the results
# For visuals, I need to make this a 2-Variable Regression
# Radial provided the best confusion matrix
####

library(ElemStatLearn)
set = training.set[,c("Age", "EstimatedSalary", "Purchased")]
X1 = seq(min(set[, 1]) - 1, max(set[, 1]) + 1, by = 0.01)
X2 = seq(min(set[, 2]) - 1, max(set[, 2]) + 1, by = 0.01)
classifier <- svm(Purchased ~., 
                  data = set,
                  type = 'C-classification',
                  kernel = 'radial')

grid_set = expand.grid(X1, X2)
colnames(grid_set) = c('Age', 'EstimatedSalary')
y_grid = predict(classifier, newdata = grid_set)

plot(set[, -3],
     main = 'SVM: Kernel (Train set)',
     xlab = 'Age', ylab = 'Salary',
     xlim = range(X1), ylim = range(X2))
contour(X1, X2, matrix(as.numeric(y_grid), length(X1), length(X2)), add = TRUE)
points(grid_set, pch = '.', col = ifelse(y_grid == 1, 'springgreen3', 'tomato'))
points(set, pch = 21, bg = ifelse(set[, 3] == 1, 'green4', 'red3'))



### Comparing it to the testing set
set = testing.set[,c("Age", "EstimatedSalary", "Purchased")]
X1 = seq(min(set[, 1]) - 1, max(set[, 1]) + 1, by = 0.01)
X2 = seq(min(set[, 2]) - 1, max(set[, 2]) + 1, by = 0.01)
classifier <- svm(Purchased ~., 
                  data = set,
                  type = 'C-classification',
                  kernel = 'radial')

grid_set = expand.grid(X1, X2)
colnames(grid_set) = c('Age', 'EstimatedSalary')
y_grid = predict(classifier, newdata = grid_set)

plot(set[, -3],
     main = 'SVM: Kernel (Test set)',
     xlab = 'Age', ylab = 'Salary',
     xlim = range(X1), ylim = range(X2))
contour(X1, X2, matrix(as.numeric(y_grid), length(X1), length(X2)), add = TRUE)
points(grid_set, pch = '.', col = ifelse(y_grid == 1, 'springgreen3', 'tomato'))
points(set, pch = 21, bg = ifelse(set[, 3] == 1, 'green4', 'red3'))
