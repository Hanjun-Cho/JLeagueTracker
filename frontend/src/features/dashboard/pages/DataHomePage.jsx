import { useEffect, useState } from "react";
import { getTeams, getTeamSquad } from "../../../services/teams.service"
import styles from "./DataHomePage.module.css"
import ListFilter from "../../../components/ListFilter/ListFilter.jsx";
import { getPlayer } from "../../../services/players.service.js";
import PlayerInformationPanel from "../panels/PlayerInformationPanel.jsx";

function DataHomePage() {
    const [teams, setTeams] = useState([]);
    const [squad, setSquad] = useState([]);
    const [selectedTeam, setSelectedTeam] = useState("");
    const [selectedPlayer, setSelectedPlayer] = useState({});
    const [selectedPlayerID, setSelectedPlayerID] = useState("");

    const get_teams = async() => {
        const teams = await getTeams();
        setTeams(teams);
    }

    const updateSquad = async() => {
        setSquad([]);
        if (selectedTeam.length == 0) {
            return;
        }
        const squad = await getTeamSquad(selectedTeam);
        setSquad(squad);
    }

    useEffect(() => {
        if (teams.length == 0) {
            get_teams();
        }
        updateSquad();
    }, [selectedTeam]);

    useEffect(() => {
        const updateSelectedPlayer = async() => {
            var player = await getPlayer(selectedPlayerID);
            setSelectedPlayer(player);
        }

        updateSelectedPlayer();
    }, [selectedPlayerID])

    return (
        <div className={styles.data_home_container}>
            <ListFilter title="Teams" options={teams} isSingular={true} id_key="id" text_key="EN_name" setParentSelection={setSelectedTeam}/>
            <ListFilter title="Squad" options={squad} isSingular={true} id_key="id" text_key="EN_name" setParentSelection={setSelectedPlayerID}/>
            <PlayerInformationPanel player={selectedPlayer}/>
        </div>
    )
}

export default DataHomePage
