import random
from geopy.distance import geodesic

# Define teams, stadiums, and their corresponding coordinates (latitude, longitude)
teams = [
    "Manchester City", "Manchester United", "Liverpool", "Chelsea", "Atletico Madrid",
    "Real Madrid", "Barcelona", "Sevilla", "Villarreal", "Inter Milan", "AC Milan",
    "Juventus", "Atalanta", "Bayern Munich", "RB Leipzig", "Borussia Dortmund",
    "Wolfsburg", "Paris Saint-Germain", "Lille", "Porto", "Benfica", "Sporting CP",
    "Shakhtar Donetsk", "Dynamo Kiev", "Ajax", "Salzburg", "Zenit", "Besiktas",
    "Club Brugge", "Young Boys", "Malmo", "Sheriff"
]

stadiums = [
    "Etihad Stadium", "Old Trafford", "Anfield", "Stamford Bridge", "Wanda Metropolitano Stadium",
    "Santiago Bernabeu Stadium", "Camp Nou", "Ramon Sanchez-Pizjuan Stadium", "Estadio de la Ceramica",
    "San Siro", "San Siro", "Allianz Stadium", "Gewiss Stadium", "Allianz Arena", "Red Bull Arena",
    "Signal Iduna Park", "Volkswagen Arena", "Parc des Princes", "Stade Pierre-Mauroy",
    "Estadio do Dragao", "Estadio da Luz", "Estadio Jose Alvalade", "NSC Olimpiyskiy Stadium",
    "NSC Olimpiyskiy Stadium", "Johan Cruyff Arena", "Red Bull Arena", "Gazprom Arena", "Vodafone Park",
    "Jan Breydel Stadium", "Stade de Suisse Wankdorf", "Eleda Stadion", "Sheriff Stadium"
]

coordinates = [
    (53.4831, -2.2004), (53.4631, -2.2913), (53.4308, -2.9608), (51.4817, -0.1900), (40.4362, -3.5998),
    (40.4531, -3.6883), (41.3809, 2.1228), (37.3902, -5.9837), (39.9403, -0.1000), (45.4780, 9.1246),
    (45.4780, 9.1246), (45.1093, 7.6413), (45.7081, 9.5242), (48.2188, 11.6244), (51.3478, 12.3694),
    (51.4926, 7.4516), (52.4259, 10.7883), (48.8417, 2.2535), (50.6295, 3.1395), (41.1616, -8.5832),
    (38.7528, -9.1843), (38.7610, -9.1607), (50.4330, 30.5216), (50.4330, 30.5216), (52.3147, 4.9417),
    (47.7094, 13.0684), (59.9720, 30.2207), (41.0369, 28.9862), (51.1838, 3.2056), (46.9631, 7.4658),
    (55.5837, 13.0469), (47.2443, 29.5713)
]

# Define the number of pots and teams per pot
num_pots = 4
teams_per_pot = 8

# Define the maximum number of same-nation matches allowed
max_same_nation_matches = 1  # Adjust this as per UEFA's rules

# Create a dictionary to store the nationality of each team
team_nationality = {
    "Manchester City": "England",
    "Manchester United": "England",
    "Liverpool": "England",
    "Chelsea": "England",
    "Atletico Madrid": "Spain",
    "Real Madrid": "Spain",
    "Barcelona": "Spain",
    "Sevilla": "Spain",
    "Villarreal": "Spain",
    "Inter Milan": "Italy",
    "AC Milan": "Italy",
    "Juventus": "Italy",
    "Atalanta": "Italy",
    "Bayern Munich": "Germany",
    "RB Leipzig": "Germany",
    "Borussia Dortmund": "Germany",
    "Wolfsburg": "Germany",
    "Paris Saint-Germain": "France",
    "Lille": "France",
    "Porto": "Portugal",
    "Benfica": "Portugal",
    "Sporting CP": "Portugal",
    "Shakhtar Donetsk": "Ukraine",
    "Dynamo Kiev": "Ukraine",
    "Ajax": "Netherlands",
    "Salzburg": "Austria",
    "Zenit": "Russia",
    "Besiktas": "Turkey",
    "Club Brugge": "Belgium",
    "Young Boys": "Switzerland",
    "Malmo": "Sweden",
    "Sheriff": "Moldova"
}

# Calculate the number of teams from each nation
nation_counts = {}
for team, nation in team_nationality.items():
    if nation in nation_counts:
        nation_counts[nation] += 1
    else:
        nation_counts[nation] = 1


# Define club coefficients for the UEFA seeding pot system
club_coefficients = {
    "Manchester City": 120, "Manchester United": 85, "Liverpool": 96, "Chelsea": 96, "Atletico Madrid": 65,
    "Real Madrid": 102, "Barcelona": 68, "Sevilla": 83, "Villarreal": 66, "Inter Milan": 81, "AC Milan": 43,
    "Juventus": 80, "Atalanta": 53, "Bayern Munich": 116, "RB Leipzig": 79, "Borussia Dortmund": 68,
    "Wolfsburg": 22.5, "Paris Saint-Germain": 93, "Lille": 32, "Porto": 58, "Benfica": 65, "Sporting CP": 42.5,
    "Shakhtar Donetsk": 53, "Dynamo Kiev": 26.5, "Ajax": 62, "Salzburg": 43, "Zenit": 22, "Besiktas": 10,
    "Club Brugge": 43, "Young Boys": 31.5, "Malmo": 18.5, "Sheriff": 17
}

# Sort teams by club coefficient in descending order
sorted_teams = sorted(teams, key=lambda team: club_coefficients[team], reverse=True)

# Divide teams into four pots
pots = [sorted_teams[i:i + teams_per_pot] for i in range(0, len(sorted_teams), teams_per_pot)]

# Initialize the schedule as an empty list
schedule = []

# Create a list of all possible matches
matches = [(teams[i], teams[j]) for i in range(len(teams)) for j in range(i + 1, len(teams))]

# Ensure teams play an equal number of home and away matches (4 home, 4 away)
home_matches = {}
away_matches = {}

for team in teams:
    home_matches[team] = []
    away_matches[team] = []

# Randomly assign matches to teams' home and away
random.shuffle(matches)

# Create the initial schedule
for pot in pots:
    for match in matches:
        team1, team2 = match
        team1_nation = team_nationality[team1]
        team2_nation = team_nationality[team2]

        # Check if both teams are from the same nation and if the limit for same-nation matches has been reached
        if team1_nation == team2_nation and nation_counts[team1_nation] > max_same_nation_matches:
            continue

        if len(home_matches[team1]) < 3 and len(away_matches[team2]) < 3:
            home_matches[team1].append(match)
            away_matches[team2].append(match)

            # Update the nation counts if the teams are from the same nation
            if team1_nation == team2_nation:
                nation_counts[team1_nation] += 1

# Flatten the home and away matches
home_matches = [match for matches in home_matches.values() for match in matches]
away_matches = [match for matches in away_matches.values() for match in matches]

# Combine home and away matches
combined_matches = home_matches + away_matches

# Shuffle the combined matches
random.shuffle(combined_matches)

# Create the initial schedule
for match in combined_matches:
    team1, team2 = match
    schedule.append({
        "team1": team1,
        "team2": team2,
        "team1_stadium": stadiums[teams.index(team1)],
        "team2_stadium": stadiums[teams.index(team2)],
    })

# Define a function to calculate the distance between two stadiums
def calculate_distance(stadium1, stadium2):
    coordinates1 = coordinates[stadiums.index(stadium1)]
    coordinates2 = coordinates[stadiums.index(stadium2)]
    return geodesic(coordinates1, coordinates2).kilometers

# Calculate the total travel distance
total_travel_distance = 0

for match in schedule:
    team1_stadium = match["team1_stadium"]
    team2_stadium = match["team2_stadium"]
    distance = calculate_distance(team1_stadium, team2_stadium)
    total_travel_distance += distance

# Print the generated schedule
print("Generated Schedule:")
for match in schedule:
    print(f"{match['team1']} (Home) vs. {match['team2']} (Away) at {match['team1_stadium']}")

# You can add any additional checks or validations as needed for your specific use case.
print("\nTotal Travel Distance:", total_travel_distance, "km")