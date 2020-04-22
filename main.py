import logging
import sys
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
}
BASE_URL = "https://www.transfermarkt.co.uk"

logger = logging.getLogger(__name__)


def main():
    submitted_players = list()
    player = dict()
    intro()
    # Ask the user for new input as long as there are not 11 correctly submitted players
    while len(submitted_players) != 11:
        while not player:
            player_name = input("Enter a players name: ")
            player = get_player(player_name)
            if not player:
                print(
                    f"A player with the name {player_name} could not be found. Please try again."
                )
        print(f'Found and added this player: {player.get("name")}')
        submitted_players.append(player)
        print(f"Current players: ")
        for i, player in enumerate(submitted_players, 1):
            print(f'{i}. {player.get("name")}')
        # Reset the player so that the program asks the user again for a new name
        player = dict()

    valid = validate_submitted_players(submitted_players)
    if valid:
        print("Congratulations! Your team is valid! :)")
        for i, player in enumerate(submitted_players, 1):
            print(f'{i}. {player.get("name")}')


def intro():
    print(
        f"Hi and welcome to football unique club/nationality all-team builder™ by Max Schubmann"
    )
    print(
        f"Enter 11 football players (exact names please) and we will validate if this team is a valid submission or not."
    )


def get_player(input_player_name: str) -> Optional[dict]:
    player = {}
    teams = []
    national_teams = []
    page = f"{BASE_URL}/schnellsuche/ergebnis/schnellsuche?query={input_player_name}&x=0&y=0"

    search_tree = requests.get(page, headers=HEADERS)
    soup = BeautifulSoup(search_tree.content, "html.parser")
    players = soup.find_all("a", {"class": "spielprofil_tooltip"})
    player_name = players[0] if players else None
    if not player_name:
        logger.info("Player {input_player_name} could not be found.")
        return

    player_url = player_name.attrs.get("href")
    pageTree = requests.get(BASE_URL + player_url, headers=HEADERS)
    pageSoup = BeautifulSoup(pageTree.content, "html.parser")
    transfers = pageSoup.find_all("tr", {"class": "zeile-transfer"})

    for transfer in transfers:
        transfer_table_rows = transfer.findAll("a", {"class": "vereinprofil_tooltip"})
        left_team = transfer_table_rows[2].text
        try:
            joined_team = transfer_table_rows[5].text
            teams.append(joined_team)
        except IndexError:
            logger.warning(
                "The club table with transfers does not have a fifth column. The player probably retired."
            )
            pass
        teams.append(left_team)

    national_team_header = pageSoup.find(string="National team career")
    if national_team_header:
        national_team_table = national_team_header.find_parent("div", {"class": "box"})
        all_national_team_links = national_team_table.findAll(
            "a", {"class": "vereinprofil_tooltip"}
        )
        national_teams = [team.text for team in all_national_team_links]
    player["name"] = player_name.text
    player["teams"] = list(set(teams))
    player["national_teams"] = national_teams
    return player


def validate_submitted_players(submitted_players: List[dict]) -> bool:

    all_teams = list()
    all_national_teams = list()
    valid = True
    for player in submitted_players:
        teams_played_for = player.get("teams", [])
        for team in teams_played_for:
            if team not in all_teams:
                all_teams.append(team)
            else:
                print(
                    f'This entry is not valid because {player.get("name")} played for {team}. Someone in the list already played there.'
                )
                return False

        national_teams_played_for = player.get("national_teams", [])
        for national_team in national_teams_played_for:
            if national_team not in all_national_teams:
                all_national_teams.append(national_team)
            else:
                print(
                    f'This entry is not valid because {player.get("name")} played for {national_team.strip()}. Someone in the list already played there.'
                )
                return False
    return True


if __name__ == "__main__":
    main()


def example_fixture() -> dict:
    # TODO: Can use this to implement testing further down the line.
    players = [
        {
            "name": "Jan Oblak",
            "teams": [
                "Olimpija U19",
                "Atlético Madrid",
                "Beira-Mar",
                "Leiria",
                "Olhanense",
                "Rio Ave FC",
                "NK Olimpija",
                "Benfica",
            ],
            "national_teams": [
                "Slovenia",
                "Slovenia U21",
                "Slovenia U16",
                "Slowenien U15",
            ],
        },
        {
            "name": "Branislav Ivanovic",
            "teams": [
                "OFK Beograd",
                "Chelsea",
                "Remont Cacak",
                "Zenit S-Pb",
                "Loko Moscow",
                "FK Srem",
            ],
            "national_teams": [
                "Serbia",
                "Serbia and Montenegro",
                "Serbia U21",
                "Serbia and Montenegro U21",
            ],
        },
        {
            "name": "Paolo Maldini",
            "teams": ["Milan", "Milan U19", "AC Milan"],
            "national_teams": ["Italy", "Italy U21", "Italy Olympic Team"],
        },
        {
            "name": "Kalidou Koulibaly",
            "teams": ["KRC Genk", "FC Metz", "SR Saint-Dié", "SSC Napoli", "FC Metz B"],
            "national_teams": ["Senegal", "France U20"],
        },
        {
            "name": "Philipp Lahm",
            "teams": [
                "VfB Stuttgart",
                "FC Bayern U17",
                "FTM Gern Yth.",
                "FC Bayern II",
                "FC Bayern Münche",
                "FC Bayern U19",
                "Bayern Munich ",
            ],
            "national_teams": [
                "Germany",
                "Germany U21",
                "Germany U20",
                "Germany U19",
                "Germany U18",
                "Germany U17",
            ],
        },
        {
            "name": "Wesley Sneijder",
            "teams": [
                "OGC Nice",
                "Real Madrid",
                "Ajax",
                "Ajax U19",
                "Ajax U17",
                "Ajax U21",
                "Galatasaray",
                "Inter",
                "Al Gharafa",
                "Ajax Youth ",
            ],
            "national_teams": [
                "Netherlands",
                "Netherlands U21",
                "Netherlands U19",
                "Netherlands U17",
            ],
        },
        {
            "name": "Thiago Silva",
            "teams": [
                "Paris SG",
                "Juventude",
                "AC Milan",
                "Fluminense",
                "FC Porto",
                "RS Futebol",
                "Dinamo Moscow",
            ],
            "national_teams": ["Brazil", "Brazil Olympic Team"],
        },
        {
            "name": "Paul Gascoigne",
            "teams": [
                "GS Tianma",
                "Lazio",
                "Newcastle U18",
                "Newcastle",
                "Everton",
                "Boston United",
                "Spurs",
                "Rangers",
                "Middlesbrough",
                "Burnley",
            ],
            "national_teams": ["England", "England U21"],
        },
        {
            "name": "Ryan Giggs",
            "teams": ["Man Utd U18", "Man Utd", "Man Utd Youth", "Man City Youth"],
            "national_teams": [
                "Wales",
                "Great Britain Olympic Team",
                "Wales U21",
                "England U16",
            ],
        },
        {
            "name": "Erling Haaland",
            "teams": [
                "Bryne FK",
                "RB Salzburg",
                "Molde FK",
                "Bryne FK U19",
                "Bor. Dortmund",
            ],
            "national_teams": [
                "Norway",
                "Norway U21",
                "Norway U20",
                "Norway U19",
                "Norway U18",
                "Norway U17",
                "Norway U16",
                "Norway U15",
            ],
        },
        {
            "name": "Lionel Messi",
            "teams": [
                "Newell's U19",
                "Barcelona C",
                "Barcelona Yth.",
                "Barça U17",
                "FC Barcelona",
                "FC Barcelona B",
                "Barça U19",
            ],
            "national_teams": ["Argentina", "Argentina U20", "Argentina Olympic Team"],
        },
    ]
    return players
