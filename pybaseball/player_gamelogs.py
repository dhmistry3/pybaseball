import bs4 as bs
import pandas as pd

from .datasources.bref import BRefSession

session = BRefSession()

def get_gamelog_soup(playerid: str, year: int, pitching_splits: bool = False) -> bs.BeautifulSoup:
    """
    gets soup for gamelog.
    """
    pitch_or_bat = 'p' if pitching_splits else 'b'
    url = f"https://www.baseball-reference.com/players/gl.fcgi?id={playerid}&t={pitch_or_bat}&year={year}"
    html = session.get(url).content
    soup = bs.BeautifulSoup(html, 'lxml')
    return soup

def get_player_gamelog(playerid: str, year: int, pitching_splits: bool = False):
    """
    Returns a dataframe of the player's gamelog
    """
    soup = get_gamelog_soup(playerid, year, pitching_splits)
    if pitching_splits:
        table_id = "pitching_gamelogs"
    else:
        table_id = "batting_gamelogs"
    table = soup.find("table", attrs=dict(id=table_id))
    if table is None:
        raise RuntimeError("Table with expected id not found on scraped page.")
    data = pd.read_html(str(table))[0]
    return data
