"""
blocklist.py
this file just contains the blocklist of the JWT tokens. it will be iported by
app adn the logout resource so taht tokens can be added to bhe blocklist when the
user logs out.
"""
BLOCKLIST = set()
