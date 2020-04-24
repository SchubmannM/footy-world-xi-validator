# Footy World XI Validator

The intention of this app is to be a validator for a little game that was started on Twitter: https://twitter.com/MundialMag/status/1250080258122022915

```
Pick the greatest World XI under these the rules:
 
- No two players from the same country
- No two can have played for the same club
- All eleven have to have played in your lifetime
```

The app asks you to enter 11 different footballer names and then runs a validation to check if any of the above stated rules were broken or not.

Version 1 does not include the "played in your lifetime" rule as that's still a bit vague to be defined in code.

This is the CLI version of the program. A web version is also available here: https://github.com/SchubmannM/footy-world-xi-validator-web and live here https://footy.schubmann.dev/

# Setup
1. Clone this directory onto your local environment: `git clone https://github.com/SchubmannM/footy-world-xi-validator.git && cd footy-world-xi-validator/`
3. Run `python3 -m pip install --user --upgrade pipenv` to install pipenv locally (or run `brew install pipenv` on MacOS). If this does not work, refer to https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv for more instructions.
4. Run `pipenv sync && pipenv shell` to install all packages needed to run this programa and enable the virtual environment
5. Run `python main.py`to run the program
6. ???
7. Profit

# Example
Entered players: 
1. Jan Oblak
2. Franco Baresi
3. Vincent Kompany
4. Paul McGrath
5. Danny Blind
6. Matthias Sammer
7. Dunga
8. Steven Gerrard
9. Didier Drogba
10. Zinédine Zidane
11. Lionel Messi

Result:
This entry is not valid because Dunga played for VfB Stuttgart. Someone in the list already played there.
