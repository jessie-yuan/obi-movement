import obi, time, csv

with open('saved-positions/bowls.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  BOWL_COORDS = list(csv_reader)

with open('saved-positions/bowl0-scoop-refined.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  SCOOP_0 = list(csv_reader)[:-1]

with open('saved-positions/bowl1-scoop-refined.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  SCOOP_1 = list(csv_reader)[:-1]

with open('saved-positions/bowl2-scoop-refined.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  SCOOP_2 = list(csv_reader)[:-1]

with open('saved-positions/bowl3-scoop-refined.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  SCOOP_3 = list(csv_reader)[:-1]

with open('saved-positions/bowl0-scrape-refined.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  SCRAPE_0 = list(csv_reader)

with open('saved-positions/bowl1-scrape-refined.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  SCRAPE_1 = list(csv_reader)

with open('saved-positions/bowl2-scrape-refined.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  SCRAPE_2 = list(csv_reader)

with open('saved-positions/bowl3-scrape-refined.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  SCRAPE_3 = list(csv_reader)

with open('saved-positions/mouth-pos.csv', 'r') as read_obj:
  csv_reader = csv.reader(read_obj)
  MOUTH_POS = list(csv_reader)[0]

class ObiMovement():
  def __init__(self):
    self.robot = obi.Obi('/dev/cu.usbserial-FTBXXIGY') # '/dev/ttyUSB0' for ubuntu
    self.bowlno = 0
    self.just_scraped = False
    self.speed = 6000
    self.accel = 16000
    self.mouthpos = MOUTH_POS
    print(self.robot.SerialIsOpen())
    print(self.robot.VersionInfo())
    self.robot.Wakeup()
    self.robot.WaitForCMUResponse()
    print("I'm up!")

  def scoop_from_bowlno(self, bowlno="previous"):
    if bowlno != "previous":
      self.bowlno = bowlno
    print(f"Scooping from bowl {str(self.bowlno)} at max speed {self.speed} and max accel {self.accel}")
    
    if not self.just_scraped:
      if self.bowlno == 0:
        waypoints = SCOOP_0
      elif self.bowlno == 1:
        waypoints = SCOOP_1
      elif self.bowlno == 2:
        waypoints = SCOOP_2
      else:
        waypoints = SCOOP_3
    else:
      if self.bowlno == 0:
        waypoints = [SCRAPE_0[-1]] + SCOOP_0[1:]
      elif self.bowlno == 1:
        waypoints = [SCRAPE_1[-1]] + SCOOP_1[1:]
      elif self.bowlno == 2:
        waypoints = [SCRAPE_2[-1]] + SCOOP_2[1:]
      else:
        waypoints = [SCRAPE_3[-1]] + SCOOP_3[1:]

    self.just_scraped = False
    
    for i in range(9):
      waypoint = waypoints[i] + [self.speed, self.accel, 0]
      self.robot.SendOnTheFlyWaypointToObi(i, waypoint)
    self.robot.ExecuteOnTheFlyPath()
    self.robot.WaitForCMUResponse()
    
  def scrape_bowlno(self, bowlno="previous"):
    self.just_scraped = True
    if bowlno != "previous":
      self.bowlno = bowlno
    print(f"Scraping down bowl {str(self.bowlno)} at max speed {self.speed} and max accel {self.accel}")

    if self.bowlno == 0:
      waypoints = SCRAPE_0
    elif self.bowlno == 1:
      waypoints = SCRAPE_1
    elif self.bowlno == 2:
      waypoints = SCRAPE_2
    else:
      waypoints = SCRAPE_3
    
    for i in range(9):
      waypoint = waypoints[i] + [self.speed, self.accel, 0]
      self.robot.SendOnTheFlyWaypointToObi(i, waypoint)
    self.robot.ExecuteOnTheFlyPath()
    self.robot.WaitForCMUResponse()

  def move_to_mouth(self):
    self.just_scraped = False
    print(f"Moving to mouth at max speed {self.speed} and max accel {self.accel}")
    waypoint = self.mouthpos + [self.speed, self.accel, 0]
    self.robot.SendOnTheFlyWaypointToObi(0, waypoint)
    self.robot.ExecuteOnTheFlyPath()
    self.robot.WaitForCMUResponse()

  def close(self):
    self.robot.GoToSleep()
    self.robot.Close()
    print(self.robot.SerialIsOpen())
    print("All done")