import { useEffect, useState } from "react";
import { getTeams } from "../../../services/teams.service"
import styles from "./DataHomePage.module.css"
import ListFilter from "../../../components/ListFilter/ListFilter.jsx";

function DataHomePage() {
    const [teams, setTeams] = useState([]);
    const [selectedTeam, setSelectedTeam] = useState("");

    const get_teams = async() => {
        const teams = await getTeams();
        setTeams(teams);
    }

    useEffect(() => {
        get_teams();
    }, []);

    return (
        <div className={styles.data_home_container}>
            <ListFilter title="Teams" options={teams} isSingular={true} id_key="id" text_key="EN_name" setParentSelection={setSelectedTeam}/>
        </div>
    )
}

export default DataHomePage
