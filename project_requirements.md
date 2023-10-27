# Banaas Premier League

## Project Description

Banaas Premier League is a web application that allows users to create and join fantasy leagues for the Indian Premier League. Users will be able to create their own leagues and invite their friends to join. Users will be able to create their own teams and compete against other users in their league. Users will be able to view the standings of their league and the standings of the Premier League. Users will be able to view the schedule of the Premier League and the schedule of their league. Users will be able to view the results of the Premier League and the results of their league. Users will be able to view the statistics of the Premier League and the statistics of their league. Users will be able to view the news of the Premier League and the news of their league. Users will be able to view the players of the Premier League and the players of their league. Users will be able to view the teams of the Premier League and the teams of their league.

## Frontend

- [x] Users can create an account
- [x] Users can login to their account
- [ ] Users can create a league
- [ ] Users can join a league
- [ ] Users can create a team
- [ ] Users can view the standings of their league
- [ ] Users can invite their friends to join their league
- [ ] Users can select players for their team
- [ ] Users can select power players for their team

## Backend

- [ ] Program should fetch data from an API of the scorecard of the Indian Premier League
- [ ] Program should compute the scores of the users based on the performance of the players in the Indian Premier League
- [ ] Program should store the data of the users, leagues, teams, and players in a database

## Data Model

Project
Series-1
League-1
Franchise-1
Player-1
Player-2
Franchise-2
Player-3
Player-4
League-2
Franchise-3
Player-3
Player-2
Franchise-4
Player-1
Player-4
Series-2
League-1
Franchise-1
Player-1
Player-2
Franchise-2
Player-3
Player-4
League-2
Franchise-3
Player-3
Player-2
Franchise-4
Player-1
Player-4

### Post Auction Table

| ID  | Tournament  | League | Franchise     | User    | Player       | Price | Power Player |
| --- | ----------- | ------ | ------------- | ------- | ------------ | ----- | ------------ |
| 1   | ODI WC 2023 | BPL    | Bhonsar Balls | Sandeep | Glen Maxwell | 1000  | True         |
| 2   | ODI WC 2023 | BPL    | Bhonsar Balls | Sandeep | Glen Maxwell | 1000  | True         |

### Matchwise Score

| ID   | Match# | Match      | Date  | Player | Batting Points | Bowling Points | Fielding Points | PoM Points | Total Points |
| ---- | ------ | ---------- | ----- | ------ | -------------- | -------------- | --------------- | ---------- | ------------ |
| UUID | 12     | IND vs PAK | 26-10 | Rizwan | 100            | 100            | 100             | 0          | 300          |
| UUID | 14     | AUS vs PAK | 27-10 | Babar  | 100            | 100            | 100             | 0          | 300          |

### Standing Table

| ID  | Tournament  | League | Franchise      | Total Points |
| --- | ----------- | ------ | -------------- | ------------ |
| 1   | ODI WC 2023 | BPL    | Bhonsar Balls  | 1000         |
| 2   | ODI WC 2023 | BPL    | Yenna Rascelas | 1000         |

## Frontend Routes

- [ ] /login
  - public
- [ ] /register
  - public
- [ ] /tournaments
  - [ ] GET
    - public
    - fetch all tournaments
- [ ] /tournaments/:id
  - [ ] GET
    - superuser
    - fetch all tournaments
  - [ ] PUT
    - superuser
    - create a tournament
  - [ ] POST
    - superuser
    - update a tournament
  - [ ] DELETE
    - superuser
    - delete a tournament
- [ ] /tournaments/:id/leagues
  - [ ] GET
    - superuser
    - fetch all leagues
  - [ ] PUT
    - authorized user
    - create a league
  - [ ] POST
    - authorized user
    - update a league
  - [ ] DELETE
    - authorized user
    - delete a league
- [ ] /tournaments/:id/leagues/:id
- [ ] /tournaments/:id/leagues/:id/teams
- [ ] /tournaments/:id/leagues/:id/teams/:id
- [ ] /tournaments/:id/leagues/:id/teams/:id/players
- [ ] /tournaments/:id/leagues/:id/invite
- [ ] /tournaments/:id/leagues/:id/join
