import math

OFFSETS = [14100, 17400, 7200, 19000, 17800, 18700]

def rad2units(rad):
  return int((rad * 180 / math.pi) * 100)

def units2rad(units):
  return (units / 100) * math.pi / 180

def urdf2motor(joints):
  res = []
  for i in range(len(joints)):
    res.append((rad2units(joints[i]) + OFFSETS[i]) % 36000)
  return res

def motor2urdf(motors):
  res = []
  for i in range(len(motors)):
    res.append(units2rad(motors[i] - OFFSETS[i]))
  return res

motors = motor2urdf([25511,16895,15525,17863,15683,26628])
print(motors)
print(urdf2motor(motors))

