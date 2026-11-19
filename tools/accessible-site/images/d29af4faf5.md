# alt
Slide "Lab: Classification Tree on Titanic with Python" con codice Python di un albero decisionale e l'albero stampato come funzione.
# descrizione
Screenshot della slide 166 del corso "Practical Machine Learning". Riproduce un ambiente di sviluppo Python (stile Spyder): in alto l'editor con codice che prepara i dati, addestra un DecisionTreeClassifier sul campo "Survived" e ne stampa il punteggio sul dataset di prova; in basso la console che esegue il file decision-tree.py e stampa l'albero come funzione Python con una serie di istruzioni "if" annidate sulle caratteristiche (Pclass, Age, SibSp, Parch, sqrt_Fare, Sex, Embarked).
# testo
Lab: Classification Tree on Titanic with Python
Editor (righe 67-78):
```
67 features = prepare_data(data_train)
68 features[:5]
69 model = DecisionTreeClassifier()
70 model.fit(features, data_train["Survived"])
71
72 #print model.decision_path(features)
73
74 tree_to_code(model, features.columns)
75 print model.score(prepare_data(data_test), data_test["Survived"])
```
Console Python:
In [38]: %run "C:/Users/thimo/Dropbox/corsi/machine_learning/real-world-machine-learning-master/decision-tree.py"
```
def tree(Pclass, Age, SibSp, Parch, sqrt_Fare, Sex=female, Sex=male, Embarked=C, Embarked=Q, Embarked=S, Embarked=nan):
  if Sex=female <= 0.5:
    if Pclass <= 1.5:
      if Age <= 53.0:
        if Age <= -0.0399999916553:
          if sqrt_Fare <= 6.2348575592:
            if sqrt_Fare <= 5.93713378906:
              if sqrt_Fare <= 5.12584447861:
                return [[ 3.  0.]]
              else:  # if sqrt_Fare > 5.12584447861
```
Numero di slide: 166
