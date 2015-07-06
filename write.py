from rdkit import Chem
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit import DataStructs
from rdkit import RDConfig
import os
import csv
import gzip
import numpy as np
import math
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from rdkit.Chem import Descriptors as Ds

train_filename = 'liltrain.csv'
test_filename  = 'liltest.csv'
pred_filename  = 'svrfeaturesplot.csv'

D = 331
LAMBDA_TWO = 0.00000001
LAMBDA_ONE = 0.00000001

# Splits array into n even parts
def split(arr, n):
   ret = []
   l = len(arr) / n
   for i in xrange(0, len(arr), l):
       ret.append(arr[i:i+l])
   return ret

# calculates rms value
def rmse(predictions, truths):
   dot_product = predictions - truths
   return math.sqrt(np.dot(dot_product.T, dot_product) / len(predictions))


# Load the training file.
data = []
with open(train_filename, 'r') as train_fh:

   # Parse it as a CSV file.
   train_csv = csv.reader(train_fh, delimiter=',', quotechar='"')

   # Skip the header row.
   next(train_csv, None)

   # Load the data.
   for row in train_csv:
       smiles   = row[0]
       features = np.array([float(x) for x in row[1:257]])
       gap      = float(row[257])

       data.append({ 'smiles':   smiles,
                         'features': features,
                         'gap':      gap })


print '1'

# accepts name of smiles, features, or gaps
def get_array(data, name):
   ret = []
   for row in data:
       ret.append(row[name])
   return ret

# divide data into training and validation parts
S = 10
def cross_train(i):
   print "iteration #", i
   splitted = split(data, S)
   validation_data = splitted.pop(i)
   train_data = [datum for sublist in splitted for datum in sublist]
   return train_data, validation_data

def regress(train_data):
   # get the gaps and the features from the data
   features = np.array([datum['features'] for datum in train_data])
   gaps = np.array([datum['gap'] for datum in train_data])

   # add in L2 regularization factor
   lhs = np.add(LAMBDA_TWO * np.identity(D), np.dot(features.T, features))
   rhs = np.dot(features.T, gaps) - LAMBDA_ONE * np.ones(D)

   # solve the linear regression
   w = np.linalg.solve(lhs, rhs)
   return w

def predict(w, test_data):
   predictions = []
   for row in test_data:
       prediction = np.dot(w.T, row['features'])
       predictions.append(prediction)
   return predictions





# Load the test file.
# test_data = []
# with open(test_filename, 'r') as test_fh:

#     # Parse it as a CSV file.
#     test_csv = csv.reader(test_fh, delimiter=',', quotechar='"')

#     # Skip the header row.
#     next(test_csv, None)

#     # Load the data.
#     for row in test_csv:
#         id       = row[0]
#         smiles   = row[1]
#         features = np.array([float(x) for x in row[2:258]])

#         test_data.append({ 'id':       id,
#                          'smiles':   smiles,
#                          'features': features })

# print '2'

# # # w = regress(data)
# # # predictions = predict(w, test_data)

N = len(data)
print(N)
descriptors_lst = [Ds.Kappa1, Ds.Kappa2, Ds.Kappa3, Ds.Chi0, Ds.Chi1, Ds.Chi0n, Ds.Chi1n, Ds.Chi2n, Ds.Chi3n, Ds.Chi4n, Ds.Chi0v, 
Ds.Chi1v, Ds.Chi2v, Ds.Chi3v, Ds.Chi4v, Ds.MolLogP, Ds.MolMR, Ds.MolWt, Ds.ExactMolWt, Ds.HeavyAtomCount, Ds.HeavyAtomMolWt, Ds.NHOHCount,
Ds.NOCount, Ds.NumHAcceptors, Ds.NumHDonors, Ds.NumHeteroatoms, Ds.NumRotatableBonds, Ds.NumValenceElectrons,
Ds.NumAromaticRings, Ds.NumSaturatedRings, Ds.NumAliphaticRings, Ds.NumAromaticHeterocycles, Ds.NumAromaticCarbocycles,
Ds.NumAliphaticHeterocycles, Ds.NumAliphaticCarbocycles, Ds.RingCount, Ds.FractionCSP3, Ds.TPSA, Ds.LabuteASA, Ds.PEOE_VSA1,
Ds.PEOE_VSA2, Ds.PEOE_VSA3, Ds.PEOE_VSA4, Ds.PEOE_VSA5, Ds.PEOE_VSA6, Ds.PEOE_VSA7, Ds.PEOE_VSA8, Ds.PEOE_VSA9, 
Ds.PEOE_VSA10, Ds.PEOE_VSA11, Ds.PEOE_VSA12, Ds.PEOE_VSA13, Ds.PEOE_VSA14, Ds.SMR_VSA1, Ds.SMR_VSA2, Ds.SMR_VSA3, Ds.SMR_VSA4, Ds.SMR_VSA5,
Ds.SMR_VSA6, Ds.SMR_VSA7, Ds.SMR_VSA8, Ds.SMR_VSA9, Ds.SMR_VSA10, Ds.SlogP_VSA1, Ds.SlogP_VSA2, Ds.SlogP_VSA3, Ds.SlogP_VSA4, 
Ds.SlogP_VSA5, Ds.SlogP_VSA6, Ds.SlogP_VSA7, Ds.SlogP_VSA8, Ds.SlogP_VSA9, Ds.SlogP_VSA10, Ds.SlogP_VSA11, Ds.SlogP_VSA12]   

print(len(descriptors_lst))

gaps = np.array([datum['gap'] for datum in data])
features = np.array([datum['features'] for datum in data])

train_gaps = gaps[:(N/2)]
validation_gaps = gaps[N/2:]
train_features = features[:(N/2)]
validation_features = features[(N/2):]

mols = np.array([Chem.MolFromSmiles(datum["smiles"]) for datum in data])
train_mols = mols[:(N/2)]
validation_mols = mols[(N/2):]
train_fingerprints = []
train_newgaps = []
for i in range(len(train_mols)):
  additional_features = []
  for func in descriptors_lst:
    additional_features.append(func(train_mols[i]))
  additional_features = np.array(additional_features)
  fingerprint = np.append(train_features[i], additional_features)
  train_fingerprints.append(fingerprint)
  train_newgaps.append(train_gaps[i])

print(2)

validation_fingerprints = []
validation_newgaps = []
for i in range(len(validation_mols)):
  additional_features = []
  for func in descriptors_lst:
    additional_features.append(func(validation_mols[i]))
  additional_features = np.array(additional_features)
  fingerprint = np.append(validation_features[i], additional_features)
  validation_fingerprints.append(fingerprint)
  validation_newgaps.append(validation_gaps[i])

# print(3)

  # fingerprint = np.append(fingerprint, validation_features[i])
  # # print(fingerprint.size)
  # validation_fingerprints.append(fingerprint)
  # validation_newgaps.append(validation_gaps[i])

# fingerprints = []
# badones = 0
# for mol in mols:
#   fingerprint = np.array(FingerprintMols.FingerprintMol(mol))
#   if fingerprint.size != 2048:
#     badones += 1
#   fingerprints.append(fingerprint)
# print(badones)

train_fingerprints = np.array(train_fingerprints)
validation_fingerprints = np.array(validation_fingerprints)
train_newgaps = np.array(train_newgaps)
validation_newgaps = np.array(validation_newgaps)

# # get the gaps and the features from the data
# features = np.array([datum['features'] for datum in data])


# test_features = np.array([datum['features'] for datum in test_data])

# test_fingerprints = []
# mols = np.array([Chem.MolFromSmiles(datum["smiles"]) for datum in test_data])
# for i in range(len(mols)):
#   if i % 100000 == 0:
#     print(i)
#   additional_features = []
#   for func in descriptors_lst:
#     additional_features.append(func(mols[i]))
#   additional_features = np.array(additional_features)
#   fingerprint = np.append(test_features[i], additional_features)
#   test_fingerprints.append(fingerprint)
  # train_newgaps.append(train_gaps[i])


# Fit regression model (radial basis functions)
# svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)

# # print(fingerprints.size)

# # make a prediction for new data based on our model
# gaps_rbf = svr_rbf.fit(train_fingerprints, train_newgaps).predict(validation_fingerprints)

# print("The RMSE value is ", rmse(np.array(gaps_rbf), validation_newgaps))

lhs = np.add(LAMBDA_TWO * np.identity(D), np.dot(train_fingerprints.T, train_fingerprints))
rhs = np.dot(train_fingerprints.T, train_newgaps)
w = np.linalg.solve(lhs, rhs)

print(5)

predictions = []
for row in validation_fingerprints:
  prediction = np.dot(w.T, row)
  predictions.append(prediction)


print("The RMSE value is ", rmse(predictions, validation_newgaps))

# print("GAAAA")


# #for i in range(S):
# #    train_data, validation_data = cross_train(i)
# #    w = regress(train_data)
# #    predictions = predict(w, validation_data)
# #    truths = get_array(validation_data, 'gap')
# #    rmses.append(rmse(np.array(predictions), np.array(truths)))
   # print "The RMSE value is ", rmse(np.array(predictions), np.array(truths))


# # print '3'


# Write a prediction file.
with open(pred_filename, 'w') as pred_fh:

   # Produce a CSV file.
   pred_csv = csv.writer(pred_fh, delimiter=',', quotechar='"')

   # Write the header row.
   pred_csv.writerow(['Id', 'Prediction'])

   for i in range(len(predictions)):
       pred_csv.writerow([i+1, predictions[i]])

# print '4'