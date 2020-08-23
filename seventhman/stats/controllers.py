from flask import request, Blueprint, jsonify
import time
from seventhman.stats.models import (
    playerbygamestats,
    team_details,
    teambygamestats,
    player_single_year_rapm,
    player_advanced,
    team_advanced,
    player_details,
    player_multi_year_rapm,
    team_single_year_rapm,
    shot_locations,
    seasons,
    player_single_rapm_view,
    player_multi_rapm_view,
    per_poss_stats,
    per_game_stats,
    pa_stats_view,
    shot_locations_view,
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy import literal_column, case, cast, String, and_, Numeric

stats = Blueprint("stats", __name__, url_prefix="/stats/api/v2/")
current_season = [2020]
min_rapm_season = [2018]
current_team_ids = [
    1610612753,
    1610612740,
    1610612741,
    1610612746,
    1610612745,
    1610612739,
    1610612744,
    1610612761,
    1610612742,
    1610612765,
    1610612760,
    1610612755,
    1610612750,
    1610612749,
    1610612754,
    1610612764,
    1610612766,
    1610612751,
    1610612763,
    1610612757,
    1610612747,
    1610612743,
    1610612759,
    1610612756,
    1610612758,
    1610612752,
    1610612762,
    1610612748,
    1610612738,
    1610612737,
]


@stats.route("players/", methods=["GET"])
def api_players():
    """
    this is the main players api endpoint for regular counting stats both
    by season and aggregated
    """
    # parse players
    if request.args.get("player", "") == "":
        players = None
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = current_season
    else:
        seasons = request.args["season"].split(" ")
    # parse time on court
    if request.args.get("toc", "") == "":
        toc = 1
    else:
        toc = float(request.args["toc"]) * 60
    # parse teams
    if request.args.get("team", "") == "":
        teams = current_team_ids
    else:
        teams = request.args["team"].split(" ")

    if players is not None:
        if request.args.get("agg", "no") == "no" and teams == current_team_ids:
            data = (
                per_game_stats.query.with_entities(
                    per_game_stats.player_name,
                    per_game_stats.player_id,
                    per_game_stats.position,
                    per_game_stats.season,
                    per_game_stats.teams,
                    per_game_stats.gp,
                    per_game_stats.mins,
                    per_game_stats.fgm,
                    per_game_stats.fga,
                    per_game_stats.tpm,
                    per_game_stats.tpa,
                    per_game_stats.ftm,
                    per_game_stats.fta,
                    per_game_stats.oreb,
                    per_game_stats.dreb,
                    per_game_stats.ast,
                    per_game_stats.tov,
                    per_game_stats.blk,
                    per_game_stats.stl,
                    per_game_stats.pf,
                    per_game_stats.points,
                    per_game_stats.plus_minus,
                )
                .filter(
                    (per_game_stats.mins >= toc)
                    & (per_game_stats.player_id.in_(players))
                    & (per_game_stats.season.in_(seasons))
                )
                .all()
            )
            return jsonify(data)
        else:
            data = (
                playerbygamestats.query.join(
                    player_details,
                    player_details.player_id == playerbygamestats.player_id,
                )
                .with_entities(
                    playerbygamestats.player_name,
                    case(
                        [
                            (
                                func.min(playerbygamestats.season)
                                == func.max(playerbygamestats.season),
                                cast(func.min(playerbygamestats.season), String),
                            )
                        ],
                        else_=func.concat(
                            func.min(playerbygamestats.season),
                            literal_column("'-'"),
                            func.max(playerbygamestats.season),
                        ),
                    ).label("season"),
                    playerbygamestats.player_id,
                    player_details.position,
                    func.string_agg(
                        playerbygamestats.team_abbrev.distinct(),
                        aggregate_order_by(
                            literal_column("'/'"), playerbygamestats.team_abbrev.desc()
                        ),
                    ).label("teams"),
                    func.count(playerbygamestats.player_id).label("gp"),
                    func.round(
                        cast(func.avg(playerbygamestats.toc) / 60, Numeric), 1
                    ).label("mins"),
                    func.round(func.avg(playerbygamestats.fgm), 1).label("fgm"),
                    func.round(func.avg(playerbygamestats.fga), 1).label("fga"),
                    func.round(func.avg(playerbygamestats.tpm), 1).label("tpm"),
                    func.round(func.avg(playerbygamestats.tpa), 1).label("tpa"),
                    func.round(func.avg(playerbygamestats.ftm), 1).label("ftm"),
                    func.round(func.avg(playerbygamestats.fta), 1).label("fta"),
                    func.round(func.avg(playerbygamestats.oreb), 1).label("oreb"),
                    func.round(func.avg(playerbygamestats.dreb), 1).label("dreb"),
                    func.round(func.avg(playerbygamestats.ast), 1).label("ast"),
                    func.round(func.avg(playerbygamestats.tov), 1).label("tov"),
                    func.round(func.avg(playerbygamestats.stl), 1).label("stl"),
                    func.round(func.avg(playerbygamestats.blk), 1).label("blk"),
                    func.round(func.avg(playerbygamestats.pf), 1).label("pf"),
                    func.round(func.avg(playerbygamestats.points), 1).label("points"),
                    func.round(func.avg(playerbygamestats.plus_minus), 1).label(
                        "plus_minus"
                    ),
                )
                .group_by(
                    playerbygamestats.player_name,
                    player_details.position,
                    playerbygamestats.player_id,
                )
                .filter(
                    (playerbygamestats.toc >= toc)
                    & (playerbygamestats.player_id.in_(players))
                    & (playerbygamestats.season.in_(seasons))
                    & (playerbygamestats.team_id.in_(teams))
                )
                .all()
            )
    else:
        if request.args.get("agg", "no") == "no" and teams == current_team_ids:
            data = (
                per_game_stats.query.with_entities(
                    per_game_stats.player_name,
                    per_game_stats.player_id,
                    per_game_stats.position,
                    per_game_stats.season,
                    per_game_stats.teams,
                    per_game_stats.gp,
                    per_game_stats.mins,
                    per_game_stats.fgm,
                    per_game_stats.fga,
                    per_game_stats.tpm,
                    per_game_stats.tpa,
                    per_game_stats.ftm,
                    per_game_stats.fta,
                    per_game_stats.oreb,
                    per_game_stats.dreb,
                    per_game_stats.ast,
                    per_game_stats.tov,
                    per_game_stats.blk,
                    per_game_stats.stl,
                    per_game_stats.pf,
                    per_game_stats.points,
                    per_game_stats.plus_minus,
                )
                .filter(
                    (per_game_stats.mins >= toc) & (per_game_stats.season.in_(seasons))
                )
                .all()
            )
            return jsonify(data)
        else:
            data = (
                playerbygamestats.query.join(
                    player_details,
                    player_details.player_id == playerbygamestats.player_id,
                )
                .with_entities(
                    playerbygamestats.player_name,
                    case(
                        [
                            (
                                func.min(playerbygamestats.season)
                                == func.max(playerbygamestats.season),
                                cast(func.min(playerbygamestats.season), String),
                            )
                        ],
                        else_=func.concat(
                            func.min(playerbygamestats.season),
                            literal_column("'-'"),
                            func.max(playerbygamestats.season),
                        ),
                    ).label("season"),
                    playerbygamestats.player_id,
                    player_details.position,
                    func.string_agg(
                        playerbygamestats.team_abbrev.distinct(),
                        aggregate_order_by(
                            literal_column("'/'"), playerbygamestats.team_abbrev.desc()
                        ),
                    ).label("teams"),
                    func.count(playerbygamestats.player_id).label("gp"),
                    func.round(
                        cast(func.avg(playerbygamestats.toc) / 60, Numeric), 1
                    ).label("mins"),
                    func.round(func.avg(playerbygamestats.fgm), 1).label("fgm"),
                    func.round(func.avg(playerbygamestats.fga), 1).label("fga"),
                    func.round(func.avg(playerbygamestats.tpm), 1).label("tpm"),
                    func.round(func.avg(playerbygamestats.tpa), 1).label("tpa"),
                    func.round(func.avg(playerbygamestats.ftm), 1).label("ftm"),
                    func.round(func.avg(playerbygamestats.fta), 1).label("fta"),
                    func.round(func.avg(playerbygamestats.oreb), 1).label("oreb"),
                    func.round(func.avg(playerbygamestats.dreb), 1).label("dreb"),
                    func.round(func.avg(playerbygamestats.ast), 1).label("ast"),
                    func.round(func.avg(playerbygamestats.tov), 1).label("tov"),
                    func.round(func.avg(playerbygamestats.stl), 1).label("stl"),
                    func.round(func.avg(playerbygamestats.blk), 1).label("blk"),
                    func.round(func.avg(playerbygamestats.pf), 1).label("pf"),
                    func.round(func.avg(playerbygamestats.points), 1).label("points"),
                    func.round(func.avg(playerbygamestats.plus_minus), 1).label(
                        "plus_minus"
                    ),
                )
                .group_by(
                    playerbygamestats.player_name,
                    player_details.position,
                    playerbygamestats.player_id,
                )
                .filter(
                    (playerbygamestats.toc >= toc)
                    & (playerbygamestats.season.in_(seasons))
                    & (playerbygamestats.team_id.in_(teams))
                )
                .all()
            )

        return jsonify(data)


# TODO rework this to be faster as well
@stats.route("/players/shots/", methods=["GET"])
def api_player_shot_locations():
    # parse players
    if request.args.get("player", "") == "" and request.args.get("team", "") == "":
        players = ["201939"]
    elif request.args.get("player", "") == "" and request.args.get("team", "") != "":
        players = None
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = current_season
    else:
        seasons = request.args["season"].split(" ")
    if request.args.get("team", "") == "":
        teams = current_team_ids
    else:
        teams = request.args["team"].split(" ")

    if players is not None:
        data = (
            shot_locations_view.query.with_entities(
                shot_locations_view.x,
                shot_locations_view.y,
                shot_locations_view.lg_made,
                shot_locations_view.lg_attempted,
                shot_locations_view.lg_x,
                shot_locations_view.lg_y,
                shot_locations_view.made,
                shot_locations_view.attempted,
            )
            .filter(
                (shot_locations_view.player_id.in_(players))
                & (shot_locations_view.season.in_(seasons))
                & (shot_locations_view.team_id.in_(teams))
            )
            .all()
        )
    else:
        data = (
            shot_locations_view.query.with_entities(
                shot_locations_view.x,
                shot_locations_view.y,
                shot_locations_view.lg_made,
                shot_locations_view.lg_attempted,
                shot_locations_view.lg_x,
                shot_locations_view.lg_y,
                shot_locations_view.made,
                shot_locations_view.attempted,
            )
            .filter(
                (shot_locations_view.season.in_(seasons))
                & (shot_locations_view.team_id.in_(teams))
            )
            .all()
        )
    return jsonify(data)


@stats.route("players/possession/", methods=["GET"])
def api_players_possession():
    """
    api endpoint for possesion rate states
    """
    # parse players
    if request.args.get("player", "") == "":
        players = None
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = current_season
    else:
        seasons = request.args["season"].split(" ")
    # parse time on court
    if request.args.get("toc", "") == "":
        toc = 1
    else:
        toc = float(request.args["toc"])
    # parse teams
    if request.args.get("team", "") == "":
        teams = current_team_ids
    else:
        teams = request.args["team"].split(" ")
    if players is not None:
        if request.args.get("agg", "no") == "no" and teams == current_team_ids:
            data = (
                per_poss_stats.query.with_entities(
                    per_poss_stats.player_name,
                    per_poss_stats.player_id,
                    per_poss_stats.position,
                    per_poss_stats.season,
                    per_poss_stats.teams,
                    per_poss_stats.gp,
                    per_poss_stats.mins,
                    per_poss_stats.fgm,
                    per_poss_stats.fga,
                    per_poss_stats.tpm,
                    per_poss_stats.tpa,
                    per_poss_stats.ftm,
                    per_poss_stats.fta,
                    per_poss_stats.oreb,
                    per_poss_stats.dreb,
                    per_poss_stats.ast,
                    per_poss_stats.tov,
                    per_poss_stats.blk,
                    per_poss_stats.stl,
                    per_poss_stats.points,
                )
                .filter(
                    (per_poss_stats.mins >= toc)
                    & (per_poss_stats.player_id.in_(players))
                    & (per_poss_stats.season.in_(seasons))
                )
                .all()
            )
            return jsonify(data)
        else:
            data = (
                playerbygamestats.query.join(
                    player_details,
                    player_details.player_id == playerbygamestats.player_id,
                )
                .with_entities(
                    playerbygamestats.player_name,
                    case(
                        [
                            (
                                func.min(playerbygamestats.season)
                                == func.max(playerbygamestats.season),
                                cast(func.min(playerbygamestats.season), String),
                            )
                        ],
                        else_=func.concat(
                            func.min(playerbygamestats.season),
                            literal_column("'-'"),
                            func.max(playerbygamestats.season),
                        ),
                    ).label("season"),
                    playerbygamestats.player_id,
                    player_details.position,
                    func.string_agg(
                        playerbygamestats.team_abbrev.distinct(),
                        aggregate_order_by(
                            literal_column("'/'"), playerbygamestats.team_abbrev.desc()
                        ),
                    ).label("teams"),
                    func.count(playerbygamestats.player_id).label("gp"),
                    func.round(
                        cast(func.avg(playerbygamestats.toc) / 60, Numeric), 1
                    ).label("mins"),
                    func.round(
                        (
                            func.sum(cast(playerbygamestats.fgm, Numeric))
                            / func.sum(cast(playerbygamestats.possessions, Numeric))
                            * 100
                        ),
                        1,
                    ).label("fgm"),
                    func.round(
                        (
                            func.sum(cast(playerbygamestats.fga, Numeric))
                            / func.sum(cast(playerbygamestats.possessions, Numeric))
                            * 100
                        ),
                        1,
                    ).label("fga"),
                    func.round(
                        func.sum(cast(playerbygamestats.tpm, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("tpm"),
                    func.round(
                        func.sum(cast(playerbygamestats.tpa, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("tpa"),
                    func.round(
                        func.sum(cast(playerbygamestats.ftm, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("ftm"),
                    func.round(
                        func.sum(cast(playerbygamestats.fta, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("fta"),
                    func.round(
                        func.sum(cast(playerbygamestats.oreb, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("oreb"),
                    func.round(
                        func.sum(cast(playerbygamestats.dreb, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("dreb"),
                    func.round(
                        func.sum(cast(playerbygamestats.ast, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("ast"),
                    func.round(
                        func.sum(cast(playerbygamestats.tov, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("tov"),
                    func.round(
                        func.sum(cast(playerbygamestats.stl, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("stl"),
                    func.round(
                        func.sum(cast(playerbygamestats.blk, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("blk"),
                    func.round(
                        func.sum(cast(playerbygamestats.pf, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("pf"),
                    func.round(
                        func.sum(cast(playerbygamestats.points, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("points"),
                    func.round(
                        func.sum(cast(playerbygamestats.fgm, Numeric))
                        / (func.sum(cast(playerbygamestats.fga, Numeric))),
                        2,
                    ).label("fg_percentage"),
                )
                .group_by(
                    playerbygamestats.player_name,
                    player_details.position,
                    playerbygamestats.player_id,
                )
                .filter(
                    (playerbygamestats.toc >= toc * 60)
                    & (playerbygamestats.player_id.in_(players))
                    & (playerbygamestats.season.in_(seasons))
                    & (playerbygamestats.team_id.in_(teams))
                )
                .all()
            )
    else:
        if request.args.get("agg", "no") == "no" and teams == current_team_ids:
            data = (
                per_poss_stats.query.with_entities(
                    per_poss_stats.player_name,
                    per_poss_stats.player_id,
                    per_poss_stats.position,
                    per_poss_stats.season,
                    per_poss_stats.teams,
                    per_poss_stats.gp,
                    per_poss_stats.mins,
                    per_poss_stats.fgm,
                    per_poss_stats.fga,
                    per_poss_stats.tpm,
                    per_poss_stats.tpa,
                    per_poss_stats.ftm,
                    per_poss_stats.fta,
                    per_poss_stats.oreb,
                    per_poss_stats.dreb,
                    per_poss_stats.ast,
                    per_poss_stats.tov,
                    per_poss_stats.blk,
                    per_poss_stats.stl,
                    per_poss_stats.points,
                )
                .filter(
                    (per_poss_stats.mins >= toc) & (per_poss_stats.season.in_(seasons))
                )
                .all()
            )

            return jsonify(data)
        else:
            data = (
                playerbygamestats.query.join(
                    player_details,
                    player_details.player_id == playerbygamestats.player_id,
                )
                .with_entities(
                    playerbygamestats.player_name,
                    case(
                        [
                            (
                                func.min(playerbygamestats.season)
                                == func.max(playerbygamestats.season),
                                cast(func.min(playerbygamestats.season), String),
                            )
                        ],
                        else_=func.concat(
                            func.min(playerbygamestats.season),
                            literal_column("'-'"),
                            func.max(playerbygamestats.season),
                        ),
                    ).label("season"),
                    playerbygamestats.player_id,
                    player_details.position,
                    func.string_agg(
                        playerbygamestats.team_abbrev.distinct(),
                        aggregate_order_by(
                            literal_column("'/'"), playerbygamestats.team_abbrev.desc()
                        ),
                    ).label("teams"),
                    func.count(playerbygamestats.player_id).label("gp"),
                    func.round(
                        cast(func.avg(playerbygamestats.toc) / 60, Numeric), 1
                    ).label("mins"),
                    func.round(
                        (
                            func.sum(cast(playerbygamestats.fgm, Numeric))
                            / func.sum(cast(playerbygamestats.possessions, Numeric))
                            * 100
                        ),
                        1,
                    ).label("fgm"),
                    func.round(
                        (
                            func.sum(cast(playerbygamestats.fga, Numeric))
                            / func.sum(cast(playerbygamestats.possessions, Numeric))
                            * 100
                        ),
                        1,
                    ).label("fga"),
                    func.round(
                        func.sum(cast(playerbygamestats.tpm, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("tpm"),
                    func.round(
                        func.sum(cast(playerbygamestats.tpa, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("tpa"),
                    func.round(
                        func.sum(cast(playerbygamestats.ftm, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("ftm"),
                    func.round(
                        func.sum(cast(playerbygamestats.fta, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("fta"),
                    func.round(
                        func.sum(cast(playerbygamestats.oreb, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("oreb"),
                    func.round(
                        func.sum(cast(playerbygamestats.dreb, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("dreb"),
                    func.round(
                        func.sum(cast(playerbygamestats.ast, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("ast"),
                    func.round(
                        func.sum(cast(playerbygamestats.tov, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("tov"),
                    func.round(
                        func.sum(cast(playerbygamestats.stl, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("stl"),
                    func.round(
                        func.sum(cast(playerbygamestats.blk, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("blk"),
                    func.round(
                        func.sum(cast(playerbygamestats.pf, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("pf"),
                    func.round(
                        func.sum(cast(playerbygamestats.points, Numeric))
                        / func.sum(cast(playerbygamestats.possessions, Numeric))
                        * 100,
                        1,
                    ).label("points"),
                    func.round(
                        func.sum(cast(playerbygamestats.fgm, Numeric))
                        / (func.sum(cast(playerbygamestats.fga, Numeric))),
                        2,
                    ).label("fg_percentage"),
                )
                .group_by(
                    playerbygamestats.player_name,
                    player_details.position,
                    playerbygamestats.player_id,
                )
                .filter(
                    (playerbygamestats.toc >= toc * 60)
                    & (playerbygamestats.season.in_(seasons))
                    & (playerbygamestats.team_id.in_(teams))
                )
                .all()
            )

        return jsonify(data)


@stats.route("teams/", methods=["GET"])
def api_teams():
    """
    this is the api endpoint for the home page of the teams data
    """

    # parse seasons
    if request.args.get("season", "") == "":
        seasons = current_season
    else:
        seasons = request.args["season"].split(" ")
    # parse teams
    if request.args.get("team", "") == "":
        teams = current_team_ids
    else:
        teams = request.args["team"].split(" ")
    agg = request.args.get("agg", "no")
    if agg == "no":
        data = (
            teambygamestats.query.with_entities(
                teambygamestats.team_abbrev.label("team"),
                teambygamestats.season,
                func.count(teambygamestats.team_id).label("gp"),
                func.round(func.avg(teambygamestats.points_for), 1).label("points"),
                func.round(func.avg(teambygamestats.points_against), 1).label(
                    "points_against"
                ),
                func.sum(teambygamestats.is_win).label("wins"),
                func.round(func.avg(teambygamestats.fouls_drawn), 1).label(
                    "fouls_drawn"
                ),
                func.round(func.avg(teambygamestats.shots_blocked), 1).label(
                    "shots_blocked"
                ),
                func.round(func.avg(teambygamestats.toc) / 60, 1).label("mins"),
                func.round(func.avg(teambygamestats.fgm), 1).label("fgm"),
                func.round(func.avg(teambygamestats.fga), 1).label("fga"),
                func.round(func.avg(teambygamestats.tpm), 1).label("tpm"),
                func.round(func.avg(teambygamestats.tpa), 1).label("tpa"),
                func.round(func.avg(teambygamestats.ftm), 1).label("ftm"),
                func.round(func.avg(teambygamestats.fta), 1).label("fta"),
                func.round(func.avg(teambygamestats.oreb), 1).label("oreb"),
                func.round(func.avg(teambygamestats.dreb), 1).label("dreb"),
                func.round(func.avg(teambygamestats.ast), 1).label("ast"),
                func.round(func.avg(teambygamestats.tov), 1).label("tov"),
                func.round(func.avg(teambygamestats.stl), 1).label("stl"),
                func.round(func.avg(teambygamestats.blk), 1).label("blk"),
                func.round(func.avg(teambygamestats.pf), 1).label("pf"),
                func.round(func.avg(teambygamestats.plus_minus), 1).label("plus_minus"),
            )
            .group_by(
                teambygamestats.team_abbrev,
                teambygamestats.team_id,
                teambygamestats.season,
            )
            .filter(
                (teambygamestats.season.in_(seasons))
                & (teambygamestats.team_id.in_(teams))
            )
            .all()
        )
    else:
        data = (
            teambygamestats.query.with_entities(
                teambygamestats.team_abbrev.label("team"),
                case(
                    [
                        (
                            func.min(teambygamestats.season)
                            == func.max(teambygamestats.season),
                            cast(func.min(teambygamestats.season), String),
                        )
                    ],
                    else_=func.concat(
                        func.min(teambygamestats.season),
                        literal_column("'-'"),
                        func.max(teambygamestats.season),
                    ),
                ).label("season"),
                func.count(teambygamestats.team_id).label("gp"),
                func.round(func.avg(teambygamestats.points_for), 1).label("points"),
                func.round(func.avg(teambygamestats.points_against), 1).label(
                    "points_against"
                ),
                func.sum(teambygamestats.is_win).label("wins"),
                func.round(func.avg(teambygamestats.pf_drawn), 1).label("fouls_drawn"),
                func.round(func.avg(teambygamestats.shots_blocked), 1).label(
                    "shots_blocked"
                ),
                func.round(func.avg(teambygamestats.toc) / 60, 1).label("mins"),
                func.round(func.avg(teambygamestats.fgm), 1).label("fgm"),
                func.round(func.avg(teambygamestats.fga), 1).label("fga"),
                func.round(func.avg(teambygamestats.tpm), 1).label("tpm"),
                func.round(func.avg(teambygamestats.tpa), 1).label("tpa"),
                func.round(func.avg(teambygamestats.ftm), 1).label("ftm"),
                func.round(func.avg(teambygamestats.fta), 1).label("fta"),
                func.round(func.avg(teambygamestats.oreb), 1).label("oreb"),
                func.round(func.avg(teambygamestats.dreb), 1).label("dreb"),
                func.round(func.avg(teambygamestats.ast), 1).label("ast"),
                func.round(func.avg(teambygamestats.tov), 1).label("tov"),
                func.round(func.avg(teambygamestats.stl), 1).label("stl"),
                func.round(func.avg(teambygamestats.blk), 1).label("blk"),
                func.round(func.avg(teambygamestats.pf), 1).label("pf"),
                func.round(func.avg(teambygamestats.plus_minus), 1).label("plus_minus"),
            )
            .group_by(teambygamestats.team_abbrev, teambygamestats.team_id)
            .filter(
                (teambygamestats.season.in_(seasons))
                & (teambygamestats.team_id.in_(teams))
            )
            .all()
        )

    return jsonify(data)


@stats.route("teams/possession/", methods=["GET"])
def api_teams_possession():
    """
    api endpoint for possesion rate states
    """
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = current_season
    else:
        seasons = request.args["season"].split(" ")
    # parse teams
    if request.args.get("team", "") == "":
        teams = current_team_ids
    else:
        teams = request.args["team"].split(" ")
    if request.args.get("agg", "no") == "no":
        data = (
            teambygamestats.query.with_entities(
                teambygamestats.team_abbrev,
                teambygamestats.season,
                teambygamestats.team_id,
                func.count(teambygamestats.team_id).label("gp"),
                func.round(func.avg(teambygamestats.toc) / 60, 1).label("mins"),
                func.round(
                    (
                        func.sum(cast(teambygamestats.fgm, Numeric))
                        / func.sum(cast(teambygamestats.possessions, Numeric))
                        * 100
                    ),
                    1,
                ).label("fgm"),
                func.round(
                    (
                        func.sum(cast(teambygamestats.fga, Numeric))
                        / func.sum(cast(teambygamestats.possessions, Numeric))
                        * 100
                    ),
                    1,
                ).label("fga"),
                func.round(
                    func.sum(cast(teambygamestats.tpm, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("tpm"),
                func.round(
                    func.sum(cast(teambygamestats.tpa, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("tpa"),
                func.round(
                    func.sum(cast(teambygamestats.ftm, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("ftm"),
                func.round(
                    func.sum(cast(teambygamestats.fta, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("fta"),
                func.round(
                    func.sum(cast(teambygamestats.oreb, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("oreb"),
                func.round(
                    func.sum(cast(teambygamestats.dreb, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("dreb"),
                func.round(
                    func.sum(cast(teambygamestats.ast, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("ast"),
                func.round(
                    func.sum(cast(teambygamestats.tov, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("tov"),
                func.round(
                    func.sum(cast(teambygamestats.stl, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("stl"),
                func.round(
                    func.sum(cast(teambygamestats.blk, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("blk"),
                func.round(
                    func.sum(cast(teambygamestats.pf, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("pf"),
                func.round(
                    func.sum(cast(teambygamestats.points_for, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("points"),
            )
            .group_by(
                teambygamestats.team_abbrev,
                teambygamestats.team_id,
                teambygamestats.season,
            )
            .filter(
                (teambygamestats.season.in_(seasons))
                & (teambygamestats.team_id.in_(teams))
            )
            .all()
        )
        return jsonify(data)
    else:
        data = (
            teambygamestats.query.with_entities(
                teambygamestats.team_abbrev,
                case(
                    [
                        (
                            func.min(teambygamestats.season)
                            == func.max(teambygamestats.season),
                            cast(func.min(teambygamestats.season), String),
                        )
                    ],
                    else_=func.concat(
                        func.min(teambygamestats.season),
                        literal_column("'-'"),
                        func.max(teambygamestats.season),
                    ),
                ).label("season"),
                teambygamestats.team_id,
                func.count(teambygamestats.team_id).label("gp"),
                func.round(func.avg(teambygamestats.toc) / 60, 1).label("mins"),
                func.round(
                    (
                        func.sum(cast(teambygamestats.fgm, Numeric))
                        / func.sum(cast(teambygamestats.possessions, Numeric))
                        * 100
                    ),
                    1,
                ).label("fgm"),
                func.round(
                    (
                        func.sum(cast(teambygamestats.fga, Numeric))
                        / func.sum(cast(teambygamestats.possessions, Numeric))
                        * 100
                    ),
                    1,
                ).label("fga"),
                func.round(
                    func.sum(cast(teambygamestats.tpm, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("tpm"),
                func.round(
                    func.sum(cast(teambygamestats.tpa, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("tpa"),
                func.round(
                    func.sum(cast(teambygamestats.ftm, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("ftm"),
                func.round(
                    func.sum(cast(teambygamestats.fta, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("fta"),
                func.round(
                    func.sum(cast(teambygamestats.oreb, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("oreb"),
                func.round(
                    func.sum(cast(teambygamestats.dreb, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("dreb"),
                func.round(
                    func.sum(cast(teambygamestats.ast, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("ast"),
                func.round(
                    func.sum(cast(teambygamestats.tov, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("tov"),
                func.round(
                    func.sum(cast(teambygamestats.stl, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("stl"),
                func.round(
                    func.sum(cast(teambygamestats.blk, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("blk"),
                func.round(
                    func.sum(cast(teambygamestats.pf, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("pf"),
                func.round(
                    func.sum(cast(teambygamestats.points_for, Numeric))
                    / func.sum(cast(teambygamestats.possessions, Numeric))
                    * 100,
                    1,
                ).label("points"),
            )
            .group_by(teambygamestats.team_abbrev, teambygamestats.team_id)
            .filter(
                (teambygamestats.season.in_(seasons))
                & (teambygamestats.team_id.in_(teams))
            )
            .all()
        )

        return jsonify(data)


@stats.route("teams/advanced/", methods=["GET"])
def teams_advanced():
    """
    endpoint for the team advanced stats tables
    """
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = current_season
    else:
        seasons = request.args["season"].split(" ")

    # parse teams
    if request.args.get("team", "") == "":
        teams = current_team_ids
    else:
        teams = request.args["team"].split(" ")
    data = (
        team_advanced.query.with_entities(
            team_advanced.team_abbrev,
            team_advanced.min_season.label("season"),
            team_advanced.team_id,
            func.round(cast(team_advanced.efg_percentage * 100, Numeric), 1).label(
                "efg_percentage"
            ),
            func.round(
                cast(team_advanced.true_shooting_percentage * 100, Numeric), 1
            ).label("true_shooting_percentage"),
            func.round(cast(team_advanced.tov_percentage, Numeric), 1).label(
                "tov_percentage"
            ),
            func.round(cast(team_advanced.oreb_percentage, Numeric), 1).label(
                "oreb_percentage"
            ),
            func.round(cast(team_advanced.ft_per_fga, Numeric), 2).label("ft_per_fga"),
            func.round(cast(team_advanced.opp_efg_percentage * 100, Numeric), 2).label(
                "opp_efg_percentage"
            ),
            func.round(cast(team_advanced.opp_tov_percentage, Numeric), 1).label(
                "opp_tov_percentage"
            ),
            func.round(cast(team_advanced.dreb_percentage, Numeric), 1).label(
                "dreb_percentage"
            ),
            func.round(cast(team_advanced.opp_ft_per_fga, Numeric), 2).label(
                "opp_ft_per_fga"
            ),
            func.round(cast(team_advanced.off_rating, Numeric), 1).label("off_rating"),
            func.round(cast(team_advanced.def_rating, Numeric), 1).label("def_rating"),
        )
        .filter(
            (team_advanced.team_id.in_(teams)) & (team_advanced.min_season.in_(seasons))
        )
        .all()
    )
    return jsonify(data)


@stats.route("players/advanced/", methods=["GET"])
def players_advanced():
    """
    endpoint for the player advanced stats tables
    """
    # parse players
    if request.args.get("player", "") == "":
        players = None
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = current_season
    else:
        seasons = request.args["season"].split(" ")

    if players is not None:

        data = (
            pa_stats_view.query.with_entities(
                pa_stats_view.player_name,
                pa_stats_view.min_season.label("season"),
                pa_stats_view.player_id,
                pa_stats_view.position,
                pa_stats_view.team_abbrev,
                pa_stats_view.gp,
                pa_stats_view.efg_percent,
                pa_stats_view.ts_percent,
                pa_stats_view.oreb_percent,
                pa_stats_view.dreb_percent,
                pa_stats_view.ast_percent,
                pa_stats_view.stl_percent,
                pa_stats_view.blk_percent,
                pa_stats_view.tov_percent,
                pa_stats_view.usg_percent,
                func.round(cast(pa_stats_view.off_rating, Numeric), 1).label(
                    "off_rating"
                ),
                func.round(cast(pa_stats_view.def_rating, Numeric), 1).label(
                    "def_rating"
                ),
            )
            .filter(
                (pa_stats_view.player_id.in_(players))
                & (pa_stats_view.min_season.in_(seasons))
            )
            .all()
        )
    else:
        data = (
            pa_stats_view.query.with_entities(
                pa_stats_view.player_name,
                pa_stats_view.min_season.label("season"),
                pa_stats_view.player_id,
                pa_stats_view.position,
                pa_stats_view.team_abbrev,
                pa_stats_view.gp,
                pa_stats_view.efg_percent,
                pa_stats_view.ts_percent,
                pa_stats_view.oreb_percent,
                pa_stats_view.dreb_percent,
                pa_stats_view.ast_percent,
                pa_stats_view.stl_percent,
                pa_stats_view.blk_percent,
                pa_stats_view.tov_percent,
                pa_stats_view.usg_percent,
                func.round(cast(pa_stats_view.off_rating, Numeric), 1).label(
                    "off_rating"
                ),
                func.round(cast(pa_stats_view.def_rating, Numeric), 1).label(
                    "def_rating"
                ),
            )
            .filter((pa_stats_view.min_season.in_(seasons)))
            .all()
        )

    return jsonify(data)


@stats.route("players/rapm/", methods=["GET"])
def player_one_year_rapm():
    """
    endpoint for player single year rapm values
    """

    # parse players
    if request.args.get("player", "") == "":
        players = None
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = current_season
    else:
        seasons = request.args["season"].split(" ")

    if players is not None:

        data = (
            player_single_rapm_view.query.with_entities(
                player_single_rapm_view.player_name,
                player_single_rapm_view.player_id,
                player_single_rapm_view.teams,
                player_single_rapm_view.gp,
                player_single_rapm_view.rapm,
                player_single_rapm_view.rapm_off,
                player_single_rapm_view.rapm_def,
                player_single_rapm_view.rapm_off_rank,
                player_single_rapm_view.rapm_def_rank,
                player_single_rapm_view.rapm_rank,
                player_single_rapm_view.min_season.label("season"),
            )
            .filter(
                (player_single_rapm_view.player_id.in_(players))
                & (player_single_rapm_view.min_season.in_(seasons))
            )
            .all()
        )
    else:
        data = (
            player_single_rapm_view.query.with_entities(
                player_single_rapm_view.player_name,
                player_single_rapm_view.player_id,
                player_single_rapm_view.teams,
                player_single_rapm_view.gp,
                player_single_rapm_view.rapm,
                player_single_rapm_view.rapm_off,
                player_single_rapm_view.rapm_def,
                player_single_rapm_view.rapm_off_rank,
                player_single_rapm_view.rapm_def_rank,
                player_single_rapm_view.rapm_rank,
                player_single_rapm_view.min_season.label("season"),
            )
            .filter((player_single_rapm_view.min_season.in_(seasons)))
            .all()
        )

    return jsonify(data)


@stats.route("teams/rapm/", methods=["GET"])
def team_one_year_rapm():
    """
    endpoint for teams single year rapm values
    """
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = current_season
    else:
        seasons = request.args["season"].split(" ")

    # parse teams
    if request.args.get("team", "") == "":
        teams = current_team_ids
    else:
        teams = request.args["team"].split(" ")

    data = (
        team_single_year_rapm.query.with_entities(
            team_single_year_rapm.team_abbrev,
            team_single_year_rapm.team_id,
            team_single_year_rapm.rapm,
            team_single_year_rapm.rapm_off,
            team_single_year_rapm.rapm_def,
            team_single_year_rapm.rapm_off_rank,
            team_single_year_rapm.rapm_def_rank,
            team_single_year_rapm.rapm_rank,
            team_single_year_rapm.min_season.label("season"),
        )
        .filter(
            (team_single_year_rapm.team_id.in_(teams))
            & (team_single_year_rapm.min_season.in_(seasons))
        )
        .all()
    )

    return jsonify(data)


@stats.route("players/multirapm/", methods=["GET"])
def player_three_year_rapm():
    """
    endpoint for player single year rapm values
    """

    # parse players
    if request.args.get("player", "") == "":
        start = time.time()
        players = None
        end = time.time()
        print(f"Time to query all players {end-start}")
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("min_season", "") == "":
        min_season = min_rapm_season
    else:
        min_season = request.args["min_season"].split(" ")

    if players is not None:

        data = (
            player_multi_rapm_view.query.with_entities(
                player_multi_rapm_view.player_name,
                player_multi_rapm_view.player_id,
                player_multi_rapm_view.teams,
                player_multi_rapm_view.gp,
                player_multi_rapm_view.rapm,
                player_multi_rapm_view.rapm_off,
                player_multi_rapm_view.rapm_def,
                player_multi_rapm_view.rapm_off_rank,
                player_multi_rapm_view.rapm_def_rank,
                player_multi_rapm_view.rapm_rank,
                player_multi_rapm_view.min_season.label("season"),
            )
            .filter(
                (player_multi_rapm_view.player_id.in_(players))
                & (player_multi_rapm_view.min_season.in_(min_season))
            )
            .all()
        )
    else:
        data = (
            player_multi_rapm_view.query.with_entities(
                player_multi_rapm_view.player_name,
                player_multi_rapm_view.player_id,
                player_multi_rapm_view.teams,
                player_multi_rapm_view.gp,
                player_multi_rapm_view.rapm,
                player_multi_rapm_view.rapm_off,
                player_multi_rapm_view.rapm_def,
                player_multi_rapm_view.rapm_off_rank,
                player_multi_rapm_view.rapm_def_rank,
                player_multi_rapm_view.rapm_rank,
                player_multi_rapm_view.min_season.label("season"),
            )
            .filter((player_multi_rapm_view.min_season.in_(min_season)))
            .all()
        )

    d = jsonify(data)

    return d


@stats.route("teams/all/", methods=["GET"])
def api_all_teams():
    """
    this endpoing returns all the distinct teams for the select boxes
    """
    data = team_details.query.with_entities(
        team_details.team_id, team_details.abbreviation
    ).all()

    return jsonify(data)


@stats.route("seasons/all/", methods=["GET"])
def api_all_seasons():
    """
    this endpoing returns all the distinct seasons for the select boxes
    """
    data = (
        teambygamestats.query.with_entities(teambygamestats.season)
        .distinct()
        .order_by(teambygamestats.season.desc())
        .all()
    )

    return jsonify(data)


@stats.route("multirapmseasons/all/", methods=["GET"])
def api_rapm_multi_seasons():
    """
    this endpoint returns all the distinct seasons for the select boxes
    """
    data = (
        player_multi_year_rapm.query.with_entities(player_multi_year_rapm.seasons)
        .distinct()
        .all()
    )
    data.sort()

    return jsonify(data)


# change this to player_details table so it doesn't have to filter and distinct
@stats.route("players/distinct/", methods=["GET"])
def api_all_players():
    """
    this endpoing returns all the distinct players for the select boxes
    """
    data = (
        player_details.query.with_entities(
            player_details.player_id,
            player_details.display_first_last.label("player_name"),
        )
        .order_by(player_details.display_first_last)
        .all()
    )

    return jsonify(data)


@stats.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
