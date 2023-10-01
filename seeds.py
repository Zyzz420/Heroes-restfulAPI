import requests
from models import db, Hero, Power, Hero_powers
from datetime import datetime

# Fetch data from the external URL
url = "https://hero.id/"
response = requests.get(url)
content = response.text

# Check if JavaScript needs to be enabled
if "necessary to enable JavaScript" in content:
    print("Please enable JavaScript in your web browser.")
    exit()

# Seeding powers
print("🦸‍♀️ Seeding powers...")
powers_data = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]

for power_data in powers_data:
    power = Power(name=power_data["name"], description=power_data["description"])
    db.session.add(power)

# Seeding heroes
print("🦸‍♀️ Seeding heroes...")
heroes_data = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"}
]

for hero_data in heroes_data:
    hero = Hero(name=hero_data["name"], super_name=hero_data["super_name"])
    db.session.add(hero)

# Commit the changes to the database
db.session.commit()

# Adding powers to heroes
print("🦸‍♀️ Adding powers to heroes...")
strengths = ["Strong", "Weak", "Average"]
heroes = Hero.query.all()
powers = Power.query.all()

import random

for hero in heroes:
    for _ in range(random.randint(1, 3)):
        power = random.choice(powers)
        hero_power = Hero_powers(hero_id=hero.id, power_id=power.id, strength=random.choice(strengths))
        db.session.add(hero_power)

# Commit the changes to the database
db.session.commit()

print("🦸‍♀️ Done seeding!")