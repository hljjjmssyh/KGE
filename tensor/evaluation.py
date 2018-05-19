import operator

from tools import *

class Scorer(object):

  def __init__(self, train, test):

    self.obj = {}
    self.sub = {}

    self.update(train.indexes)
    self.update(test.indexes)

  def update(self, triples):

    for i, j, k in triples:

      if (i, j) not in self.obj:
        self.obj[(i, j)] = [k]
      elif k not in self.obj[(i, j)]:
        self.obj[(i, j)].append(k)

      if (j, k) not in self.sub:
        self.sub[(j, k)] = [i]
      elif i not in self.sub[(j, k)]:
        self.sub[(j, k)].append(i)

  def evaluation(self, model, test):

    nb_test = len(test.values)
    nrank = np.empty(2*nb_test)
    rrank = np.empty(2*nb_test)

    for a, (i, j, k) in enumerate(test.indexes):

      res_obj = model.objects(i, j)
      rrank[a] = 1 + np.sum(res_obj > res_obj[k])
      nrank[a] = rrank[a] - np.sum(res_obj[self.obj[(i,j)]] > res_obj[k])

      res_sub = model.subjects(j, k)
      rrank[nb_test + a] = 1 + np.sum(res_sub > res_sub[i])
      nrank[nb_test + a] = rrank[nb_test + a] - np.sum(
        res_sub[self.sub[(j,k)]] > res_sub[i])

    return nrank

  def prediction(self, model, test):

    aux = []
    for a, (i, j, k) in enumerate(test.indexes):
      obj = model.objects(i, j)
      sub = model.subjects(j, k)
      aux.append(obj[k]*sub[i])

    return aux
