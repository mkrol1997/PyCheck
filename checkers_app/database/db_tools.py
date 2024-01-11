from typing import Union

from checkers_app.checkers.main import collection


def add_player(channel: str, player_sid: str) -> None:
    doc = collection.find_one({"channel": channel})

    if doc:
        players = doc.get("players", {})
        if not players:
            collection.update_one({"channel": channel}, {"$set": {"players": {player_sid: 1}}})
        elif len(players) == 1:
            collection.update_one({"channel": channel}, {"$set": {f"players.{player_sid}": -1}})


def get_current_player(channel: str, player_sid: str) -> str:
    game_data = collection.find_one({"channel": channel})
    sid = game_data["players"].get(str(player_sid))
    return sid


def current_player_sid(channel: str, player_value: int) -> Union[str, None]:
    game_data = collection.find_one({"channel": channel})
    if game_data and "players" in game_data:
        players = game_data["players"]
        for sid, value in players.items():
            if player_value == value:
                return sid
    return None
