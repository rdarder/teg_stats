import random
import logging

logging.basicConfig(level=logging.WARNING)

def dices(n):
  return [dice() for i in range(n)]
def dice():
  return random.randint(0,5)


def results(a_dices, b_dices, significant):
  a_wins, b_wins = 0, 0
  a_dices.sort(reverse=True)
  b_dices.sort(reverse=True)
  for a,b,i in zip(a_dices, b_dices,range(significant)):
    if a > b:
      a_wins += 1
    else:
      b_wins+=1
  logging.debug("results: %s - %s. %s attacks %s.",
                a_wins, b_wins, a_dices, b_dices)
  return a_wins, b_wins


def attack(a_armies, b_armies, significant):
  assert(min(a_armies, b_armies, significant) == significant)
  return results(dices(a_armies), dices(b_armies), significant)

def normal_combat_attack(a, b):
  a_dices=min(a-1, 3)
  b_dices=min(b, 3)
  significant=min(a_dices, b_dices)
  if b >= 3 and a > 2*b: a_dices=4
  return attack(a_dices, b_dices, significant)

def snow_combat_attack(a,b):
  a_dices=min(a-1, 3)
  b_dices=min(b, 3)+1
  significant=min(a_dices, b_dices-1)
  if b >= 3 and a >= 2*b: a_dices=4
  return attack(a_dices, b_dices, significant)

def tail_wind_combat_attack(a,b):
  a_dices=min(a, 4)
  b_dices=min(b, 3)
  significant=min(a_dices-1, b_dices)
  return attack(a_dices, b_dices, significant)

class avg(object):
  def __init__(self, f, runs=1000):
    self.f = f
    self.runs = runs
  def test(self, res):
    return 1 if res > 0 else 0
  def __call__(self, *args, **kwargs):
    result=0
    for i in range(self.runs):
      result+=self.test(self.f(*args, **kwargs))
    res =float(result) / self.runs
    logging.debug("%s runs, %s positive. %s avg",
                  self.runs, result, res)
    return res

class deathmatch(object):
  def __init__(self, attack_impl):
    self.attack = attack_impl
  def exhaust_attack(self, a, b):
    while a > 1 and b > 0:
      wa, wb = self.attack(a,b)
      a -= wb
      b -= wa
    if b == 0:
      return a
    else:
      return -b

def stats(up_to):
  attack1 = avg(deathmatch(normal_combat_attack).exhaust_attack)
  attack2 = avg(deathmatch(snow_combat_attack).exhaust_attack)
  attack3 = avg(deathmatch(tail_wind_combat_attack).exhaust_attack)
  for b in range(1,up_to):
    for a in range(2,up_to):
      yield a,b,attack1(a,b),attack2(a,b),attack3(a,b)

for res in stats(10):
  print("%2i %2i %1.2f %1.2f %1.2f" % res)

#avg(deathmatch(normal_combat_attack).exhaust_attack)(4,3)

