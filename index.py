import requests
import pandas as pd
import json
from pandas.io.json import json_normalize


def get_game_info(year, seasonType='regular', week=None, team=None, home=None, 
                 away=None, conference=None):
    '''
        Takes in year, seasonType, week, team, hometeam, awayteam or conference
        and returns a DataFrame containing results and demographic information
        for all of the games in the queried time period, team or season

        year = year.
        seasonType = regular or postseason. default is regular
        week(optional) = week.
        team(optional) = see get_team_info() for valid team names, queries 
                         for a team regardless of their role in the game (home or away).
        home(optional) = queries by home team. Ex. home=Florida State will return a 
                         DataFrame containing info from all of Florida State's games.
        away(optional) = queries by away team.
        conference(optional) = queries by conference. Ex.conference=SEC will return a 
                               DataFrame containing info from all SEC games.
    '''
    base_url = 'https://api.collegefootballdata.com/games?'
    payload = {}
    payload['year'] = year
    payload['seasonType'] = seasonType

    if week is not None:
        payload['week'] = week
    if team is not None:
        payload['team'] = team
    if home is not None:
        payload['home'] = home
    if away is not None:
        payload['away'] = away
    if conference is not None:
        payload['conference'] = conference

    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        return pd.DataFrame(r.json())
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))

    

def get_game_player_stats(year, week=None, seasonType='regular', team=None, 
                          conference=None, category=None, gameId=None):
    '''
        Takes in year, seasonType, week, team, home, away, conference, or gameID
        and returns a DataFrame with all of the individual player stats for the given
        parameters
        
        Must have either a gameID, week, team or conference. 
        JSON required special parsing in order to massage it into one DataFrame.

        year = year.
        week (optional) = week.
        seasonType = regular or postseason.
        conference(optional) = see get_conference_list() to see list of valid conferences,
                               query by conference.
        category(optional) = valid categories: defensive, fumbles, punting, kicking, 
                             puntReturns, interceptions, receiving, rushing, passing, 
                             kickReturns

        TODO break totalPenaltiesYards, fourthDownEff, thirdDownEff and completionAttempts 
             into seperate stats instead of compound stats
    '''
    base_url = 'https://api.collegefootballdata.com/games/players?'
    payload = {}
    payload['year'] = year
    payload['seasonType'] = seasonType

    #if one of these conditions is not true it will return a bad request
    if week is not None or team is not None or conference is not None or gameId is not None:
        if week is not None:
            payload['week'] = week
        if team is not None:
            payload['team'] = team
        if conference is not None:
            payload['conference'] = conference
        if category is not None:
            payload['category'] = category
        if gameId is not None:
            payload['gameId'] = gameId
    else:
        raise ValueError('Must have 1 of team, week, conference or a valid gameID')

    r = requests.get(base_url, params=payload)

    #nested json, have to normalize at multiple levels
    #creating dataframes containing non nested info then merging back
    #clean this up if you can think of a better way to bring in the meta from the parent
    if r.status_code == 200:
        try:
            games = r.json()
            games_df = json_normalize(games)[['id']]
            teams_df = json_normalize(games, record_path='teams', meta='id')
            categories_df = json_normalize(json.loads(teams_df.to_json(orient='records')), 
                                          record_path='categories', meta=['id','school'])
            types_df = json_normalize(json.loads(categories_df.to_json(orient='records')),
                                      record_path = 'types', meta = ['id','name','school'],
                                      record_prefix = 'play_type_')
            athletes_df = json_normalize(json.loads(types_df.to_json(orient='records')),
                                        record_path = 'play_type_athletes', 
                                        meta = ['school','name','id','play_type_name'],
                                        record_prefix = 'athlete_')


            return games_df.merge(teams_df[['conference','homeAway','points','school','id']])\
                           .merge(categories_df[['name','id','school']])\
                           .merge(types_df[['play_type_name','id','name','school']])\
                           .merge(athletes_df)
        except KeyError:
            raise KeyError('Invalid parameters, no results returned')

    else:
        raise Exception('Request failed with status code: '+str(r.status_code))
    

def get_game_team_stats(year, week=None, seasonType='regular', team=None, conference=None, 
                        gameId=None):
    '''
        Takes in year, week, seasonType, team, conference, or gameID and returns
        a DataFrame showing all of the team stats for each game in the queried parameters

        year=year
        week (optional)=week.
        seasonType (optional) = regular or postseason default to regular
        team (optional) = returns a dataframe containing team stats from each of the 
                         games played by a team in a given season.
        conference (optional) = returns a dataframe containing all of the team stats 
                                from each of the games played by a team in that 
                                conference in a given season.

        TODO break totalPenaltiesYards, fourthDownEff, thirdDownEff and completionAttempts 
             into seperate stats
        
    '''
    base_url = 'https://api.collegefootballdata.com/games/teams?'
    payload = {}
    payload['year'] = year
    payload['seasonType'] = seasonType

<<<<<<< HEAD
    #needs one of these to not return a bad request
=======
>>>>>>> 7481a0dbb5219b8980d9d0608c67a2094664d7b1
    if week is not None or team is not None or conference is not None or gameId is not None:
        if week is not None:
            payload['week'] = week
        if team is not None:
            payload['team'] = team
        if conference is not None:
            payload['conference'] = conference
        if gameId is not None:
            payload['gameId'] = gameId
    else:
        raise ValueError('Must have 1 of team, week, conference or a valid gameID')

<<<<<<< HEAD
    #deeply nested json again
=======
>>>>>>> 7481a0dbb5219b8980d9d0608c67a2094664d7b1
    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        try:
            games = r.json()
            games_df = json_normalize(r.json())[['id']]
            teams_df = json_normalize(games, record_path='teams', meta='id')
            stats_df = json_normalize(json.loads(teams_df.to_json(orient='records')),
                                      record_path='stats', meta=['school','id'])

            return games_df.merge(teams_df[['conference','homeAway','points','school','id']])\
                           .merge(stats_df)
            
        except KeyError:
            raise KeyError('Invalid parameters, no results returned')
            
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_drive_info(year, seasonType='regular', week=None, team=None, offense=None, defense=None, conference=None, offenseConference=None, defenseConference=None):
    '''
        Takes in year, seasonType, week, team, conference or gameId and returns
        a DataFrame containing the drive info from each of the games in the queried
        parameters
        
        year=year
        seasonType (optional) = regular or postseason. Default: regular season
        week (optional) =week
        team (optional) =Gets all of the drives by the queried team in a given season
        offense (optional) =Gets all of the drives by the queried offense in a given season
        defense (optional) =Gets all of the drives the queried defense participated in in a given season

        TODO Break elapsed, start time, end time out into time datatypes
    '''
    
    base_url = 'https://api.collegefootballdata.com/drives?'
    payload = {}
    payload['year'] = year
    payload['seasonType'] = seasonType

    if week is not None:
        payload['week'] = week
    if team is not None:
        payload['team'] = team
    if conference is not None:
        payload['conference'] = conference
    if offense is not None:
        payload['offense'] = offense
    if defense is not None:
        payload['defense'] = defense
    if offenseConference is not None:
        payload['offenseConference'] = offenseConference
    if defenseConference is not None:
        payload['defenseConference'] = defenseConference

    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        return pd.DataFrame(r.json())
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_play_by_play_data(year, seasonType='regular', week=None, team=None, offense=None, 
                          defense=None, conference=None, offenseConference=None, 
                          defenseConference=None, playType=None):
    '''
        Takes in year, seasonType, week, team, offense, defense, conference,
        offenseConference, defenseConference or playType and returns
        a DataFrame containing all of the plays for the games by the queried
        parameters.

        year = year
        seasonType (optional) = regular or postseason. Default='regular'
        week=week
        team=returns all the plays where the queried team was involved
        offense=returns all of the plays where the queried offense was involved
        defense=returns all of the plays where the queried defense was involved
        conference=returns all of the plays where the queried conference was involved
        offenseConference=returns all of the plays where the offenseConference is the
                          queried conference
        defenseConference= returns all of the plays where the defenseConference is the
                           queried conference
        playType=returns all of the plays of the queried type in a given season.

        TODO break clock into time format
    '''
    base_url = 'https://api.collegefootballdata.com/plays?'
    payload = {}
    payload['year'] = year
    payload['seasonType'] = seasonType

    if week is not None:
        payload['week'] = week
    if team is not None:
        payload['team'] = team
    if conference is not None:
        payload['conference'] = conference
    if offense is not None:
        payload['offense'] = offense
    if defense is not None:
        payload['defense'] = defense
    if offenseConference is not None:
        payload['offenseConference'] = offenseConference
    if defenseConference is not None:
        payload['defenseConference'] = defenseConference
    if playType is not None:
        payload['playType'] = playType
    
    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        return pd.DataFrame(r.json())
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))
    

def get_play_types():
    '''
        Returns a DataFrame containing all possible play types
        in the play by play data
    '''
    r = requests.get('https://api.collegefootballdata.com/play/types')

    if r.status_code == 200:
        return pd.DataFrame(r.json())
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_team_info(conference=None):
    '''
        Returns a DataFrame containing color, logo, and mascot info
        about each team in the queried params

        conference (optional) = queries by conference
    '''
    base_url = 'https://api.collegefootballdata.com/teams'
    payload = {}

    if conference is not None:
        payload['conference'] = conference
    
    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        return pd.DataFrame(r.json())
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_team_roster(team):
    '''
        Returns a DataFrame containing all of the players on a given roster

        team=team
    '''
    base_url = 'https://api.collegefootballdata.com/roster?'
    payload = {}

    payload['team'] = team
    
    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        return pd.DataFrame(r.json())
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_team_talent(year=None):
    '''
        Shows the team talent rankings of every team

        year (optional) = year
    '''
    base_url = 'https://api.collegefootballdata.com/talent'
    payload = {}

    if year is not None:
        payload['year'] = year
    
    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        return pd.DataFrame(r.json())
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_matchup_history(team1, team2, minYear=None, maxYear=None):
    '''
        Takes in team1, team2, minYear, maxYear and returns a DataFrame
        containing the record and information about each of the times
        the two teams have met.

        team1 = team1
        team2 = team2
        minYear (optional) = lowest year to consider
        maxYear (optional) = highest year to consider

    '''
    base_url = 'https://api.collegefootballdata.com/teams/matchup?'
    payload = {}

    payload['team1'] = team1
    payload['team2'] = team2

    if minYear is not None:
        payload['minYear'] = minYear
    if maxYear is not None:
        payload['maxYear'] = maxYear
    
    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        return json_normalize(r.json(), record_path='games', 
                              meta=['team1','team1Wins','team2','team2Wins','ties'])
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_conference_list():
    '''
        Returns a DataFrame containing a list of conferences and their full
        names
    '''
    r = requests.get('https://api.collegefootballdata.com/conferences')
    if r.status_code == 200:
        return pd.DataFrame(r.json())
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_venue_info():
    '''
        Returns a DataFrame containing a list of the different venues,
        and information about them such as location, elevation and type of turf

        TODO break location into lat and long columns
    '''
    r = requests.get('https://api.collegefootballdata.com/venues')
    if r.status_code == 200:
        return pd.DataFrame(r.json())
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_coach_info(firstName=None, lastName=None, team=None, year=None, minYear=None, 
                   maxYear=None):
    '''
        Takes in first name, last name, team, year, and a range of years and 
        returns a DataFrame containing a list of the different coaches, how many wins
        they got each season, where they were and ranks before and after the season

        firstName (optional) = first name of the coach
        lastName (optional) = last name of the coach
        team (optional) = team
        year (optional) = year
        minYear (optional) = minimum year considered
        maxYear (optional) = max year considered
    '''
    base_url = 'https://api.collegefootballdata.com/coaches'
    payload = {}

    if firstName is not None:
        payload['firstName'] = firstName
    if lastName is not None:
        payload['lastName'] = lastName
    if team is not None:
        payload['team'] = team
    if year is not None:
        payload['year'] = year
    if minYear is not None:
        payload['minYear'] = minYear
    if maxYear is not None:
        payload['maxYear'] = maxYear

    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        return json_normalize(r.json(),record_path = 'seasons', meta=['first_name','last_name'])
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))


def get_historical_rankings(year, week=None, seasonType=None):
    '''
    Take in year, week and season type and print a DataFrame containing
    each teams ranking within each poll in a given season and week

    Year: int, year
    Week: int, week
    seasonType: string, values: regular or postseason
    '''

    base_url = 'https://api.collegefootballdata.com/rankings?'
    payload = {}

    payload['year'] = year
    if week is not None:
        payload['week'] = week
    if seasonType is not None:
        payload['seasonType'] = seasonType

    r = requests.get(base_url, params=payload)
    if r.status_code == 200:
        polls_df = json_normalize(r.json(), record_path = 'polls', 
                                  meta=['season','seasonType','week'])
        return json_normalize(json.loads(polls_df.to_json(orient='records')), 
                              record_path = 'ranks', 
                              meta=['season','seasonType','week','poll'])
    else:
        raise Exception('Request failed with status code: '+str(r.status_code))

