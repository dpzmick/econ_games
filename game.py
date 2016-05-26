import numpy.polynomial.polynomial as poly
import scipy.optimize as opt
import random
import matplotlib.pyplot as plt

class RandomPlayer:
  def __init__(self, name):
    self.name = name

  # returns a Quantity
  def take_turn(self):
    return float(random.randrange(200))

  def update_history(self, quantity, profit):
    pass

  def final_report(self):
    pass

class Player:
  def __init__(self, name):
    self.name = name
    self.xs = []
    self.ys = []

  # returns a Quantity
  def take_turn(self):
    if len(self.xs) < 9000:
      return float(random.randrange(200))

    # do curve fitting
    # in the form A + Bx + Cx^2
    coeffs = poly.polyfit(self.xs, self.ys, 2) # fit a polynomial of degree 2
    func = poly.Polynomial(coeffs) # create the polynomial
    m = opt.minimize(-func, 100)
    return m.x[0]

  def update_history(self, quantity, profit):
    self.xs.append(quantity)
    self.ys.append(profit)

  def final_report(self):
    coeffs = poly.polyfit(self.xs, self.ys, 2) # fit a polynomial of degree 2

    xs = range(0,200)
    ffit = poly.polyval(xs, coeffs)
    plt.figure()
    plt.plot(xs, ffit)
    plt.savefig(self.name + '.png', bbox_inches='tight')
 
    plt.figure()
    plt.plot(self.xs, self.ys, '.')
    plt.savefig(self.name + 'scatter.png', bbox_inches='tight')

# game starts here
p1 = Player("player1")
p2 = RandomPlayer("player2")

price = 10
mc = 8
mq = 200

print "iteration\tp1_q\tp2_q"

turn_counter = 0
while turn_counter < 10000:
  p1_q = p1.take_turn()
  p2_q = p2.take_turn()

  print turn_counter, "\t", p1_q, "\t", p2_q

  total = p1_q + p2_q

  p1_qa = p1_q
  p2_qa = p2_q

  if p1_q < 0:
    p1.update_history(p1_q, -1000000000)
    p1_q = 0

  if p2_q < 0:
    p1.update_history(p2_q, -1000000000)
    p2_q = 0

  if total > mq:
    percent = float(total)/float(mq)

    p1_qa = 1/percent * p1_q
    p2_qa = 1/percent * p2_q

  p1_profit = price*p1_qa - p1_q*mc
  p2_profit = price*p2_qa - p2_q*mc

  p1.update_history(p1_q, p1_profit)
  p2.update_history(p2_q, p2_profit)

  turn_counter += 1
 
p1.final_report()
p2.final_report()
