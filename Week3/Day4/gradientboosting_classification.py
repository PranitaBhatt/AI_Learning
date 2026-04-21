from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits

SEED=23 #Setting a seed value which will handle a reproducability in random state

X,y=load_digits(return_X_y=True)

train_x,test_x,train_y,test_y=train_test_split(X,y,test_size=0.25,random_state=SEED)

#creating an object for gradient boosting classifier
gbc=GradientBoostingClassifier(n_estimators=300,learning_rate=0.05,random_state=100,max_features=5)

gbc.fit(train_x,train_y)
pred_y=gbc.predict(test_x)

#printing the accuracy score
accuracy=accuracy_score(test_y,pred_y)
print("Accuracy Score is: ",accuracy)