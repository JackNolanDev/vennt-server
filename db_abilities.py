# Josh Aaron Miller 2021
# VenntDB methods for Abilities

import venntdb, webscraper
import ability as Ability
from constants import *

# VenntDB Methods

def add_ability(self, username, abiObj):
	if "abilities" not in self.db["accounts"][username]:
		self.db["accounts"][username]["abilities"] = []
	self.db["accounts"][username]["abilities"].append(abiObj)

def get_abilities(self, username):
	if "abilities" not in self.db["accounts"][username]:
		return []
	return [abiObj.name for abiObj in self.db["accounts"][username]["abilities"]]

def get_ability(self, username, ability):
	if "abilities" not in self.db["accounts"][username]:
		return None
	for abiObj in self.db["accounts"][username]["abilities"]:
		if ability == abiObj.name:
			return abiObj
	return None
	

def get_cached_ability(self, name):
	for ability in self.db["ability_cache"]:
		if ability is not None and name == ability.name:
			return ability
	return None
		
def cache_ability(self, abiObj):
	self.db["ability_cache"][self.db["ability_cache_index"]] = abiObj
	self.db["ability_cache_index"] += 1
	if self.db["ability_cache_index"] > MAX_ABILITY_CACHE:
		self.db["ability_cache_index"] = 0

def find_ability(self, ability_name):
	approximations = []
	URL = ""
	for a in self.db["abilities"]:
		if ability_name.lower() in a["ability"].lower(): # approximate
			if a["ability"].lower() == ability_name.lower():
				URL = a["url"]
				return [a["ability"]], URL
			else:
				approximations.append(a["ability"])
				URL = a["url"]
	return approximations, URL
	
def get_or_make_ability(self, name):
	cached = self.get_cached_ability(name)
	if cached is not None:
		return cached
	if not webscraper.ability_exists(self, name):
		raise AssertionError("Bad call to db_abilities.get_or_make_ability, incorrect number of approximations (" + str(len(approximations)) + "): " + ", ".join(approximations))
	
	approximations, URL = self.find_ability(name)
	contents = webscraper.get_ability_contents(approximations[0], URL)
	new_ability = Ability.make_ability(contents)
	self.cache_ability(new_ability)
	return new_ability