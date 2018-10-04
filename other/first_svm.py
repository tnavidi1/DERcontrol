import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline



def svm_train(X, y):
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.31)

    from sklearn.svm import SVC
    svclassifier = SVC(kernel='linear')

    svclassifier.fit(X_train, y_train)

    y_pred = svclassifier.predict(X_test)

    y_final = svclassifier.predict(X[2].reshape(1, -1))
    print('predicted')
    print(y_final)

    y_final = svclassifier.predict(X[75].reshape(1, -1))
    print('predicted')
    print(y_final)

    y_final = svclassifier.predict(X[540].reshape(1, -1))
    print('predicted')
    print(y_final)

    print('original')
    print(y)


    #print('X_test')
    #print(np.shape(X_test))
    #print(np.mean(X_test,1))
    #print(X_test)
    #print('y_test')
    #print(np.shape(y_test))
    #print(y_test)
    #print('y_train')
    #print(np.shape(y_train))
    #print(y_train)
    #print('X_train')
    #print(np.shape(X_train))
    #print(X_train)

    # nodes over chosen: 1, 6, 12, 35, 55
    # nodes within chosen: 57, 63
    # nodes under chosen: 64, 65, 78, 120




    from sklearn.metrics import classification_report, confusion_matrix
    print
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))


    print('intercept:')
    print(np.shape(svclassifier.intercept_))
    print(svclassifier.intercept_.reshape(1, 3))
    print('coefficients')
    print(np.shape(svclassifier.coef_))
    print(svclassifier.coef_)


    return svclassifier