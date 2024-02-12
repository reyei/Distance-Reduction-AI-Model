import random
import math
from geopy.distance import geodesic

#random.seed(123)

# Define teams, stadiums, and their corresponding coordinates (latitude, longitude)
teams = [
    "Man City", "Bayern", "Real Madrid", "Chelsea", "Liverpool", "PSG",
    "Man United", "Inter Milan", "Roma", "Juventus", "Leipzig", "Sevilla",
    "Dortmund", "Barcelona", "Villareal", "Benfica", "Atletico Madrid",
    "Napoli", "Ajax", "Leverkusen", "Porto", "Tottenham", "Frankfurt",
    "Shakhtar Donetsk", "Atalanta", "Basel", "Marseille", "Arsenal",
    "Feyenoord", "Rangers", "AZ Alkmaar", "Lyon", "AC Milan", "Club Brugge",
    "Salzburg", "Sporting CP"
]

stadiums = [
    "Etihad Stadium", "Allianz Arena", "Santiago Bernabéu", "Stamford Bridge", "Anfield", "Parc des Princes",
    "Old Trafford", "San Siro", "Stadio Olimpico", "Allianz Stadium", "Red Bull Arena Leipzig",
    "Estadio Ramón Sánchez-Pizjuán", "Signal Iduna Park", "Camp Nou", "Estadi de la Ceràmica",
    "Estádio da Luz", "Wanda Metropolitano", "Stadio San Paolo", "Johan Cruijff ArenA", "BayArena",
    "Estádio do Dragão", "Tottenham Hotspur Stadium", "Deutsche Bank Park", "Stadion Wojska Polskiego",
    "Gewiss Stadium", "St. Jakob-Park", "Orange Vélodrome", "Emirates Stadium", "Stadion Feijenoord",
    "Ibrox", "AFAS Stadion", "Groupama Stadium", "San Siro", "Jan Breydel Stadium", "Red Bull Arena",
    "Estádio José Alvalade"
]

coordinates = [
    (53.4831, -2.2004), (48.2188, 11.6244), (40.4531, -3.6883), (51.4817, -0.1910), (53.4308, -2.9609),
    (48.8417, 2.2531), (53.4631, -2.2913), (45.4786, 9.1239), (41.9330, 12.4545), (45.1094, 7.6410),
    (51.3452, 12.3616), (37.3754, -5.9823), (51.4926, 7.4516), (41.3809, 2.1228), (39.9321, -0.1039),
    (38.7528, -9.1846), (40.4360, -3.5991), (40.8270, 14.1930), (52.3141, 4.9411), (51.0381, 7.0026),
    (41.1614, -8.5830), (51.6043, -0.0665), (50.0689, 8.6452), (50.4017, 30.2529), (45.6700, 9.6914),
    (47.5473, 7.6193), (43.2693, 5.3950), (51.5549, -0.1084), (51.8930, 4.5235), (55.8532, -4.3090),
    (52.5920, 4.7386), (45.7655, 4.9792), (45.4786, 9.1239), (51.2099, 3.2176), (47.7976, 13.0305), (38.7615, -9.1615)
]

# Define the number of pots and teams per pot
num_pots = 4
teams_per_pot = 9

# Define the maximum number of same-nation matches allowed
max_same_nation_matches = 1  # Adjust this as per UEFA's rules

# Create a dictionary to store the nationality of each team
team_nationality = {
    "Man City": "England", "Bayern": "Germany", "Real Madrid": "Spain", "Chelsea": "England", "Liverpool": "England",
    "PSG": "France", "Man United": "England", "Inter Milan": "Italy", "Roma": "Italy", "Juventus": "Italy",
    "Leipzig": "Germany", "Sevilla": "Spain", "Dortmund": "Germany", "Barcelona": "Spain", "Villareal": "Spain",
    "Benfica": "Portugal", "Atletico Madrid": "Spain", "Napoli": "Italy", "Ajax": "Netherlands", "Leverkusen": "Germany",
    "Porto": "Portugal", "Tottenham": "England", "Frankfurt": "Germany", "Shakhtar Donetsk": "Ukraine", "Atalanta": "Italy",
    "Basel": "Switzerland", "Marseille": "France", "Arsenal": "England", "Feyenoord": "Netherlands", "Rangers": "Scotland",
    "AZ Alkmaar": "Netherlands", "Lyon": "France", "AC Milan": "Italy", "Club Brugge": "Belgium", "Salzburg": "Austria",
    "Sporting CP": "Portugal"
}

# Calculate the number of teams from each nation
nation_counts = {}
for team, nation in team_nationality.items():
    if nation in nation_counts:
        nation_counts[nation] += 1
    else:
        nation_counts[nation] = 1


# Check if nation_counts works correctly
print (nation_counts)


# Calculate the distances between all stadium pairs and store in a dictionary
stadium_distances = {}
for i in range(len(stadiums)):
    for j in range(i + 1, len(stadiums)):
        distance = geodesic(coordinates[i], coordinates[j]).kilometers
        stadium_distances[(stadiums[i], stadiums[j])] = distance

# Define club coefficients for the UEFA seeding pot system
club_coefficients = {
    "Man City": 120, "Bayern": 116, "Real Madrid": 102, "Chelsea": 96, "Liverpool": 96, "PSG": 93,
    "Man United": 85, "Inter Milan": 81, "Roma": 80, "Juventus": 80, "Leipzig": 79, "Sevilla": 78,
    "Dortmund": 68, "Barcelona": 68, "Villareal": 66, "Benfica": 65, "Atletico Madrid": 65, "Napoli": 63,
    "Ajax": 62, "Leverkusen": 61, "Porto": 58, "Tottenham": 54, "Frankfurt": 53, "Shakhtar Donetsk": 53,
    "Atalanta": 53, "Basel": 52, "Marseille": 30, "Arsenal": 50, "Feyenoord": 49, "Rangers": 49,
    "AZ Alkmaar": 46, "Lyon": 44, "AC Milan": 43, "Club Brugge": 43, "Salzburg": 43, "Sporting CP": 42.5
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

# Simulated Annealing Parameters
initial_temperature = 1000
cooling_rate = 0.95
iterations_per_temperature = 100

# Define the objective function to minimize (total travel distance)
def objective_function(schedule):
    total_distance = sum(stadium_distances.get((match["team1_stadium"], match["team2_stadium"]), 0) for match in schedule)
    return total_distance

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

        if len(home_matches[team1]) < 4 and len(away_matches[team2]) < 4:
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

# Initialize best schedule
best_schedule = schedule.copy()

# Calculate the initial total distance
initial_total_distance = objective_function(best_schedule)

# Simulated Annealing Loop
temperature = initial_temperature
best_objective = initial_total_distance

while temperature > 1:
    for _ in range(iterations_per_temperature):
        # Randomly select two matches to swap
        i, j = random.sample(range(len(schedule)), 2)

        # Swap the matches
        schedule[i], schedule[j] = schedule[j], schedule[i]

        # Calculate the objective value for the neighbor solution
        neighbor_objective = objective_function(schedule)

        # Calculate the change in objective value
        delta_objective = neighbor_objective - best_objective

        # If the neighbor solution is better or accepted with a probability based on delta_objective and temperature, update the current solution
        if delta_objective < 0 or random.random() < math.exp(-delta_objective / temperature):
            best_schedule = schedule.copy()
            best_objective = neighbor_objective

        else:
            # Revert the swap if the neighbor solution is not accepted
            schedule[i], schedule[j] = schedule[j], schedule[i]

    # Cool down the temperature
    temperature *= cooling_rate

# Ensure there are exactly 189 matches in the schedule to avoid "index out of range" errors 
while len(best_schedule) > 189:
    # Randomly remove excess matches
    i = random.randint(0, len(best_schedule) - 1)
    del best_schedule[i]

# Print the generated schedule
print("\nBest Schedule:")
for match in best_schedule:
    print(f"{match['team1']} (Home) vs. {match['team2']} (Away) at {match['team1_stadium']} - Distance: {stadium_distances.get((match['team1_stadium'], match['team2_stadium']), 0)} km")

print("\nBest Objective Value:", best_objective)

# Calculate the final total distance
final_total_distance = objective_function(best_schedule)

# Calculate the distance saved
distance_saved = initial_total_distance - final_total_distance

print(f"\nTotal Distance Saved: {distance_saved} km")