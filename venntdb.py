# Josh Aaron Miller 2021
# Vennt DB

import _pickle as cPickle
import json
import os

from authentication import Authenticator
from constants import *

import importlib
logClass = importlib.import_module("logger")
logger = logClass.Logger("VenntDB")


class VenntDB:

    from db_campaigns import create_campaign, get_campaign_invites, send_campaign_invite, remove_campaign_invite, add_user_to_campaign, get_campaign, get_campaigns, get_role, set_role, add_to_campaign, remove_from_campaign
    from db_characters import character_exists, get_character, create_character, get_characters, get_attr, set_attr
    from db_inventory import get_standard_weapon, get_custom_weapon, get_weapon, remove_weapon, add_weapon, add_item, view_items, remove_item
    from db_abilities import get_cached_ability, cache_ability, remove_cached_ability, find_ability, get_abilities, get_ability, get_or_make_ability, add_ability, validate_abilities, remove_ability
    from db_initiative import add_to_combat, remove_from_combat, start_combat, end_combat, next_turn, update_initiative_style, reset_actions
    #from db_combat import push_undo, pop_undo, get_undo_history

    def __init__(self, filename):
        self.filename = filename
        self.auth = Authenticator()

        if os.path.exists(self.filename):
            self.db = cPickle.load(open(self.filename, 'rb'))
        else:
            self.db = {}
            self.db["accounts"] = {}
            self.db["campaigns"] = {}
            self.db["ability_cache"] = [None] * (MAX_ABILITY_CACHE + 1)  # list of Ability dicts
            self.db["ability_cache_index"] = 0
        # Not including static json files in DB for efficiency
        if os.path.exists("weapons.json"):
            with open("weapons.json") as f:
                self.weapons = json.load(f)
        if os.path.exists("abilities.json"):
            with open("abilities.json", encoding="utf8") as f:  # encoding for smart quotes
                self.abilities = json.load(f)
                # self.validate_abilities() # TODO continue

    def dump(self):
        print(json.dumps(self.db, indent=4, separators=(',', ': '), sort_keys=True))

    def permissions(self, username, character_id):
        # TODO Permission.EDIT unused
        if self.is_valid("accounts", username, "characters", character_id):
            return Permission.OWN
        else:
            for campaign_id in self.db["accounts"][username]["campaigns"]:
                campaign = self.db["campaigns"][campaign_id]
                role = campaign["members"][username]
                if role == "GM":
                    if character_id in campaign["members"].keys():
                        return Permission.PRIVATE_VIEW
                elif role == "player":
                    if character_id in campaign["members"].keys():
                        return Permission.ADD  # maybe COMBAT?
                else:
                    if character_id in campaign["members"].keys():
                        return Permission.PUBLIC_VIEW

        return Permission.NONE

    def assert_valid(self, *args, dict=None):
        logger.log("assert_valid", ">".join(args))
        if not self.is_valid(*args, dict=dict):
            raise AssertionError("Database path does not exist")

    def is_valid(self, *args, dict=None):  # check valid path through DB
        if dict is None:
            dict = self.db
        if len(args) < 1:
            return True
        elif len(args) == 1:
            return args[0] in dict
        else:
            return args[0] in dict and self.is_valid(*args[1:], dict=dict[args[0]])

    def create_account(self, username, salt, pass_hash):
        self.db["accounts"][username] = {}
        self.db["accounts"][username]["salt"] = salt
        self.db["accounts"][username]["password"] = pass_hash
        self.db["accounts"][username]["characters"] = {}
        # ids & campaign names only
        self.db["accounts"][username]["campaigns"] = []
        self.db["accounts"][username]["campaign_invites"] = []
        self.db["accounts"][username]["weapons"] = []
        self.db["accounts"][username]["enemies"] = []
        self.save_db()

    def get_account_salt(self, username):
        if not self.is_valid("accounts", username):
            return False
        return self.db["accounts"][username]["salt"]

    def does_password_match(self, username, pass_hash):
        if not self.is_valid("accounts", username):
            raise AssertionError("Tried to access non-existent user")
        return pass_hash == self.db["accounts"][username]["password"]

    def save_db(self):
        cPickle.dump((self.db), open(self.filename, 'wb'))
