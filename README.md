# vennt-server
A headless server for making API calls to the Vennt database.


### Running the server
`py -3 venntserver.py vennt.db`


# API Documentation
All communications with the server are done via JSON. Authentication is done via POST which gives you an `auth_token` that can be used to make GET calls. Note that all interactions with the API are case-sensitive.

See `example.py` for an example of API calls.


### Create an account
POST: `{"register":"myusername","password":"mypassword"}`

Returns a JSON:
- `success`: whether the operation was successful
- `info`: on failure, why
- `auth_token`: on success, your authentication token for making GET calls

### Login
POST: `{"login":"myusername","password":"mypassword"}`

Returns a JSON:
- `success`: whether the operation was successful
- `info`: on failure, why
- `auth_token`: on success, your authentication token for making GET calls

### Logout
GET: `<baseURL>/logout?q={"auth_token":"<auth_token>"}`

Returns a JSON:
- `success`: whether the operation was successful (whether `auth_token` was valid prior to logout)

### Create a character
GET: `<baseURL>/create_character?q={"auth_token":"<auth_token>", "name":"myfirstcharacter"[,"ATTR":"<num>"...]}`

Setting attribute properties are optional.
**Valid attributes**: AGI, CHA, DEX, INT, PER, SPI, STR, TEK, WIS, HP, MAX_HP, MP, MAX_MP, VIM, MAX_VIM, ARMOR, HERO, INIT, SPEED


Returns a JSON:
- `success`: whether the operation was successful
-`id`: on success, the unique ID of your new character

### Create a campaign
GET: `<baseURL>/create_campaign?q={"auth_token":"<auth_token>", "name":"myfirstcampaign"}`

Returns a JSON:
- `success`: whether the operation was successful
-`id`: on success, the unique ID of your new campaign

### Get characters
GET: `<baseURL>/get_characters?q={"auth_token":"<auth_token>"}`

Returns a JSON:
- `success`: whether the operation was successful
-`value`: on success, returns a list of IDs for your characters

### Get campaigns
GET: `<baseURL>/get_campaigns?q={"auth_token":"<auth_token>"}`

Returns a JSON:
- `success`: whether the operation was successful
-`value`: on success, returns a list of IDs for your campaigns

### Invite someone to a campaign
GET: `<baseURL>/send_campaign_invite?q={"auth_token":"<auth_token>","username":"<recipient>"}`

Returns a JSON:
- `success`: whether the operation was successful

### View active campaign invites
GET: `<baseURL>/view_campaign_invites?q={"auth_token":"<auth_token>"}`

Returns a JSON:
- `success`: whether the operation was successful
- `value`: list of campaign invites
  - `from`: username of inviter
  - `id`: campaign ID
  
### Accept campaign invite
GET: `<baseURL>/accept_campaign_invite?q={"auth_token":"<auth_token>","id":"<campaign_id>"}`

Returns a JSON:
- `success`: whether the operation was successful

### Decline campaign invite
GET: `<baseURL>/decline_campaign_invite?q={"auth_token":"<auth_token>","id":"<campaign_id>"}`

Returns a JSON:
- `success`: whether the operation was successful

### Set campaign role
You must be the campaign owner to set a role.
GET: `<baseURL>/set_role?q={"auth_token":"<auth_token>","username":"<target>","role":"[GM/player]"}`

Returns a JSON:
- `success`: whether the operation was successful

### Get campaign role
You must be the campaign owner or a member of the campaign to view someone's role.
GET: `<baseURL>/set_role?q={"auth_token":"<auth_token>","username":"<target>"}`

Returns a JSON:
- `success`: whether the operation was successful
- `value`: the user's role (GM or player)

### Set an attribute
GET: `<baseURL>/set_attr?q={"auth_token":"<auth_token>", "char_id":"<character_id>", "attr":"ATTR", "val":"<num>"}`

**Valid attributes**: AGI, CHA, DEX, INT, PER, SPI, STR, TEK, WIS, HP, MAX_HP, MP, MAX_MP, VIM, MAX_VIM, ARMOR, HERO, INIT, SPEED

Returns a JSON:
- `success`: whether the operation was successful

### Get an attribute
GET: `<baseURL>/get_attr?q={"auth_token":"<auth_token>", "char_id":"<character_id>", "attr":"ATTR"}`

**Valid attributes**: AGI, CHA, DEX, INT, PER, SPI, STR, TEK, WIS, HP, MAX_HP, MP, MAX_MP, VIM, MAX_VIM, ARMOR, HERO, INIT, SPEED

Returns a JSON:
- `success`: whether the operation was successful
- `value`: the attribute value

### Get character
GET: `<baseURL>/get_character?q={"auth_token":"<auth_token>"}`

Returns a JSON:
- `success`: whether the operation was successful
- `value`: on success, returns your character (JSON)
