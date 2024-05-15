from obimovement import ObiMovement
import time

obirobot = ObiMovement()
obirobot.scoop_from_bowlno(0)
obirobot.move_to_mouth()
obirobot.scrape_bowlno(1)
obirobot.scoop_from_bowlno()
obirobot.scoop_from_bowlno(2)
obirobot.move_to_mouth()
time.sleep(3)
obirobot.close()