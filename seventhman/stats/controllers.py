from flask import request, Blueprint, jsonify
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
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy import literal_column, case, cast, String, and_, Numeric

stats = Blueprint("stats", __name__, url_prefix="/stats/api/v2/")


@stats.route("players/", methods=["GET"])
def api_players():
    """
    this is the main players api endpoint for regular counting stats both
    by season and aggregated
    """
    # TODO create an API endpoint model class for each of my endpoints that can
    # be passed the args and returned the query results Matt Barlowe 2020-04-11

    # parse players
    if request.args.get("player", "") == "":
        players = (
            playerbygamestats.query.with_entities(playerbygamestats.player_id)
            .filter((playerbygamestats.toc > 0))
            .distinct()
            .all()
        )
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = [
            playerbygamestats.query.with_entities(
                func.max(playerbygamestats.season)
            ).all()[0][0]
        ]
        print(seasons)
    else:
        seasons = request.args["season"].split(" ")
    # parse time on court
    if request.args.get("toc", "") == "":
        toc = 1
    else:
        toc = float(request.args["toc"]) * 60
    # parse teams
    if request.args.get("team", "") == "":
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
    else:
        teams = request.args["team"].split(" ")
    print(request.args)
    if request.args.get("agg", "no") == "no":
        data = (
            playerbygamestats.query.join(
                player_details, player_details.player_id == playerbygamestats.player_id
            )
            .with_entities(
                playerbygamestats.player_name,
                playerbygamestats.season,
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
                    func.avg(cast(playerbygamestats.toc, Numeric)) / 60, 1
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
                playerbygamestats.season,
            )
            .filter(
                (playerbygamestats.toc >= toc)
                & (playerbygamestats.player_id.in_(players))
                & (playerbygamestats.season.in_(seasons))
                & (playerbygamestats.team_id.in_(teams))
            )
            .all()
        )
        return jsonify(data)
    else:
        data = (
            playerbygamestats.query.join(
                player_details, player_details.player_id == playerbygamestats.player_id
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
                func.round(func.avg(playerbygamestats.toc) / 60, 1).label("mins"),
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

        return jsonify(data)


@stats.route("/players/shots/", methods=["GET"])
def api_player_shot_locations():
    # parse players
    if request.args.get("player", "") == "" and request.args.get("team", "") == "":
        players = ["201939"]
    elif request.args.get("player", "") == "" and request.args.get("team", "") != "":
        players = (
            playerbygamestats.query.with_entities(playerbygamestats.player_id)
            .filter((playerbygamestats.toc > 0))
            .distinct()
            .all()
        )
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = [
            playerbygamestats.query.with_entities(
                func.max(playerbygamestats.season)
            ).all()[0][0]
        ]
    else:
        seasons = request.args["season"].split(" ")
    if request.args.get("team", "") == "":
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
    else:
        teams = request.args["team"].split(" ")

    lg_avg = (
        shot_locations.query.join(
            teambygamestats,
            and_(
                shot_locations.team_id == teambygamestats.team_id,
                shot_locations.game_id == teambygamestats.game_id,
            ),
        )
        .with_entities(
            shot_locations.loc_x.label("lg_x"),
            shot_locations.loc_y.label("lg_y"),
            func.sum(shot_locations.shot_made_flag).label("lg_made"),
            func.count(shot_locations.shot_made_flag).label("lg_attempted"),
        )
        .group_by(shot_locations.loc_x, shot_locations.loc_y)
        .filter(teambygamestats.season.in_(seasons))
        .subquery()
    )

    data = (
        shot_locations.query.join(
            teambygamestats,
            and_(
                shot_locations.team_id == teambygamestats.team_id,
                shot_locations.game_id == teambygamestats.game_id,
            ),
        )
        .join(
            lg_avg,
            and_(
                lg_avg.c.lg_x == shot_locations.loc_x,
                lg_avg.c.lg_y == shot_locations.loc_y,
            ),
        )
        .with_entities(
            shot_locations.loc_x.label("x"),
            shot_locations.loc_y.label("y"),
            lg_avg.c.lg_made,
            lg_avg.c.lg_attempted,
            lg_avg.c.lg_x,
            lg_avg.c.lg_y,
            func.sum(shot_locations.shot_made_flag).label("made"),
            func.count(shot_locations.shot_made_flag).label("attempted"),
        )
        .group_by(
            shot_locations.loc_x,
            shot_locations.loc_y,
            lg_avg.c.lg_made,
            lg_avg.c.lg_attempted,
            lg_avg.c.lg_x,
            lg_avg.c.lg_y,
        )
        .filter(
            (shot_locations.player_id.in_(players))
            & (teambygamestats.season.in_(seasons))
            & (shot_locations.team_id.in_(teams))
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
        players = (
            playerbygamestats.query.with_entities(playerbygamestats.player_id)
            .filter((playerbygamestats.toc > 0))
            .distinct()
            .all()
        )
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = [
            playerbygamestats.query.with_entities(
                func.max(playerbygamestats.season)
            ).all()[0][0]
        ]
        print(seasons)
    else:
        seasons = request.args["season"].split(" ")
    # parse time on court
    if request.args.get("toc", "") == "":
        toc = 1
    else:
        toc = float(request.args["toc"]) * 60
    # parse teams
    if request.args.get("team", "") == "":
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
    else:
        teams = request.args["team"].split(" ")
    print(request.args)
    if request.args.get("agg", "no") == "no":
        data = (
            playerbygamestats.query.join(
                player_details, player_details.player_id == playerbygamestats.player_id
            )
            .with_entities(
                playerbygamestats.player_name,
                playerbygamestats.season,
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
                    func.avg(cast(playerbygamestats.toc, Numeric)) / 60, 1
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
            )
            .group_by(
                playerbygamestats.player_name,
                player_details.position,
                playerbygamestats.player_id,
                playerbygamestats.season,
            )
            .filter(
                (playerbygamestats.toc >= toc)
                & (playerbygamestats.player_id.in_(players))
                & (playerbygamestats.season.in_(seasons))
                & (playerbygamestats.team_id.in_(teams))
            )
            .all()
        )
        return jsonify(data)
    else:
        data = (
            playerbygamestats.query.join(
                player_details, player_details.player_id == playerbygamestats.player_id
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
                func.round(func.avg(playerbygamestats.toc) / 60, 1).label("mins"),
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
                (playerbygamestats.toc >= toc)
                & (playerbygamestats.player_id.in_(players))
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
        seasons = [
            teambygamestats.query.with_entities(func.max(teambygamestats.season)).all()[
                0
            ][0]
        ]
    else:
        seasons = request.args["season"].split(" ")
    # parse teams
    if request.args.get("team", "") == "":
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
    else:
        teams = request.args["team"].split(" ")
    agg = request.args.get("agg", "no")
    print(agg)
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
        seasons = [
            teambygamestats.query.with_entities(func.max(teambygamestats.season)).all()[
                0
            ][0]
        ]
    else:
        seasons = request.args["season"].split(" ")
    # parse teams
    if request.args.get("team", "") == "":
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
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
        seasons = [
            playerbygamestats.query.with_entities(
                func.max(playerbygamestats.season)
            ).all()[0][0]
        ]
        print(seasons)
    else:
        seasons = request.args["season"].split(" ")

    # parse teams
    if request.args.get("team", "") == "":
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
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
        players = (
            playerbygamestats.query.with_entities(playerbygamestats.player_id)
            .filter((playerbygamestats.toc > 0))
            .distinct()
            .all()
        )
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = [
            playerbygamestats.query.with_entities(
                func.max(playerbygamestats.season)
            ).all()[0][0]
        ]
        print(seasons)
    else:
        seasons = request.args["season"].split(" ")

    data = (
        player_advanced.query.join(
            player_details, player_details.player_id == player_advanced.player_id
        )
        .with_entities(
            player_details.display_first_last,
            player_advanced.min_season.label("season"),
            player_advanced.player_id,
            player_details.position,
            player_advanced.team_abbrev,
            func.round(cast(player_advanced.efg_percent * 100, Numeric), 1).label(
                "efg_percentage"
            ),
            func.round(cast(player_advanced.ts_percent * 100, Numeric), 1).label(
                "true_shooting_percentage"
            ),
            func.round(cast(player_advanced.oreb_percent, Numeric), 1).label(
                "oreb_percentage"
            ),
            func.round(cast(player_advanced.dreb_percent, Numeric), 1).label(
                "dreb_percentage"
            ),
            func.round(cast(player_advanced.ast_percent, Numeric), 1).label(
                "ast_percentage"
            ),
            func.round(cast(player_advanced.stl_percent, Numeric), 1).label(
                "stl_percentage"
            ),
            func.round(cast(player_advanced.blk_percent, Numeric), 1).label(
                "blk_percentage"
            ),
            func.round(cast(player_advanced.tov_percent, Numeric), 1).label(
                "tov_percentage"
            ),
            func.round(cast(player_advanced.usg_percent, Numeric), 1).label(
                "usg_percentage"
            ),
            func.round(cast(player_advanced.off_rating, Numeric), 1).label(
                "off_rating"
            ),
            func.round(cast(player_advanced.def_rating, Numeric), 1).label(
                "def_rating"
            ),
        )
        .filter(
            (player_advanced.player_id.in_(players))
            & (player_advanced.min_season.in_(seasons))
        )
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
        players = (
            playerbygamestats.query.with_entities(playerbygamestats.player_id)
            .filter((playerbygamestats.toc > 0))
            .distinct()
            .all()
        )
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("season", "") == "":
        seasons = [
            playerbygamestats.query.with_entities(
                func.max(playerbygamestats.season)
            ).all()[0][0]
        ]
        print(seasons)
    else:
        seasons = request.args["season"].split(" ")

    teams = (
        playerbygamestats.query.with_entities(
            playerbygamestats.season,
            playerbygamestats.player_id,
            func.count().label("gp"),
            func.string_agg(
                playerbygamestats.team_abbrev.distinct(),
                aggregate_order_by(
                    literal_column("'/'"), playerbygamestats.team_abbrev.desc()
                ),
            ).label("teams"),
        )
        .group_by(playerbygamestats.player_id, playerbygamestats.season)
        .filter(
            (playerbygamestats.player_id.in_(players))
            & (playerbygamestats.season.in_(seasons))
        )
        .subquery()
    )

    data = (
        player_single_year_rapm.query.join(
            teams,
            and_(
                teams.c.season == player_single_year_rapm.min_season,
                teams.c.player_id == player_single_year_rapm.player_id,
            ),
        )
        .with_entities(
            player_single_year_rapm.player_name,
            player_single_year_rapm.player_id,
            teams.c.teams,
            teams.c.gp,
            player_single_year_rapm.rapm,
            player_single_year_rapm.rapm_off,
            player_single_year_rapm.rapm_def,
            player_single_year_rapm.rapm_off_rank,
            player_single_year_rapm.rapm_def_rank,
            player_single_year_rapm.rapm_rank,
            player_single_year_rapm.min_season.label("season"),
        )
        .filter(
            (player_single_year_rapm.player_id.in_(players))
            & (player_single_year_rapm.min_season.in_(seasons))
        )
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
        seasons = [
            playerbygamestats.query.with_entities(
                func.max(playerbygamestats.season)
            ).all()[0][0]
        ]
    else:
        seasons = request.args["season"].split(" ")

    # parse teams
    if request.args.get("team", "") == "":
        teams = team_details.query.with_entities(team_details.team_id).distinct().all()
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
        players = (
            playerbygamestats.query.with_entities(playerbygamestats.player_id)
            .filter((playerbygamestats.toc > 0))
            .distinct()
            .all()
        )
    else:
        players = request.args["player"].split(" ")
    # parse seasons
    if request.args.get("min_season", "") == "":
        min_season = [
            x[0]
            for x in player_multi_year_rapm.query.with_entities(
                player_multi_year_rapm.min_season
            )
            .distinct()
            .order_by(player_multi_year_rapm.min_season.desc())
            .all()
        ]
        team_seasons = list(range(int(min_season[0]), int(min_season[0]) + 2))
        print(team_seasons)
    else:
        min_season = request.args["min_season"].split(" ")
        team_seasons = list(range(int(min_season[0]), int(min_season[0]) + 3))

    teams = (
        playerbygamestats.query.with_entities(
            playerbygamestats.player_id,
            func.count().label("gp"),
            func.string_agg(
                playerbygamestats.team_abbrev.distinct(),
                aggregate_order_by(
                    literal_column("'/'"), playerbygamestats.team_abbrev.desc()
                ),
            ).label("teams"),
        )
        .group_by(playerbygamestats.player_id)
        .filter(
            (playerbygamestats.player_id.in_(players))
            & (playerbygamestats.season.in_(team_seasons))
        )
        .subquery()
    )

    data = (
        player_multi_year_rapm.query.join(
            teams, teams.c.player_id == player_multi_year_rapm.player_id
        )
        .with_entities(
            player_multi_year_rapm.player_name,
            player_multi_year_rapm.player_id,
            teams.c.teams,
            teams.c.gp,
            player_multi_year_rapm.rapm,
            player_multi_year_rapm.rapm_off,
            player_multi_year_rapm.rapm_def,
            player_multi_year_rapm.rapm_off_rank,
            player_multi_year_rapm.rapm_def_rank,
            player_multi_year_rapm.rapm_rank,
            player_multi_year_rapm.min_season,
            player_multi_year_rapm.max_season,
            player_multi_year_rapm.seasons.label('season'),
        )
        .filter(
            (player_multi_year_rapm.player_id.in_(players))
            & (player_multi_year_rapm.min_season.in_(min_season))
        )
        .all()
    )

    return jsonify(data)


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
        playerbygamestats.query.with_entities(playerbygamestats.season)
        .distinct()
        .order_by(playerbygamestats.season.desc())
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


@stats.route("players/distinct/", methods=["GET"])
def api_all_players():
    """
    this endpoing returns all the distinct players for the select boxes
    """
    data = (
        playerbygamestats.query.with_entities(
            playerbygamestats.player_id, playerbygamestats.player_name
        )
        .filter(playerbygamestats.toc > 0)
        .distinct()
        .all()
    )
    data.sort(key=lambda x: x[1])

    return jsonify(data)


@stats.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
