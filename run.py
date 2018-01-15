import sys, os
import argparse

import tensor
import tensor.tools as tools
from tensor.read import *

if __name__ == "__main__":

  parser = argparse.ArgumentParser(
    description='Link Prediction Experiment'
  )

  parser.add_argument('--model', metavar='', 
    help='model to run: {Complex, DistMult, Polyadic, TransE}')
  parser.add_argument('--lmbda', type=float, default=0.1, metavar='', 
    help='value of lambda  (default: 0.1)')
  parser.add_argument('--data', metavar='', 
    help='dataset to be used: {wn18, fb15k, yago3, ml100k, kinship}')
  parser.add_argument('--k', type=int, default=50, metavar='', 
    help='embedding size (default: 50)')
  parser.add_argument('--lr', type=float, default=0.5, metavar='', 
    help='Learning rate (default: 0.5)')
  parser.add_argument('--epoch', type=int, default=1000, metavar='', 
    help='Number of epochs (default: 1000)')
  parser.add_argument('--bsize', type=int, default=500, metavar='', 
    help='Number of examples in the batch sample (default: 500)')
  parser.add_argument('--negative', type=int, default=10, metavar='', 
    help='Number of negative examples generated (default: 10)')
  parser.add_argument('--valid', type=int, default=10, metavar='', 
    help='Number of iterations before validation (default: 10)')
  parser.add_argument('--rand', default=1234, type=int, metavar='',
    help='Set the random seed (default: 1234')

  args = parser.parse_args()

  np.random.seed(args.rand)

  path = os.path.dirname(os.path.realpath( os.path.basename(__file__)))
  data, train, valid, test, entities, relations = load(path, args.data + ".txt")

  param = Parameters(args.model, lmbda=args.lmbda, k=args.k, lr=args.lr, 
    epoch=args.epoch, bsize=args.bsize, negative=args.negative, 
    valid=args.valid)

  model = Experiment(data, train, valid, test, entities, relations, param)

  print("Technique: " + str(param.model))
  print("Learning rate: " + str(param.lr))
  print("Max epochs: " + str(param.epoch))
  print("Generated negatives ratio: " + str(param.neg_ratio))
  print("Batch size: " + str(param.batch_size))

  model.induce()
  model.evaluate()
