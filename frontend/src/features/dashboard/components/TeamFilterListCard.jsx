import { useState } from "react";
import styles from "./TeamFilterListCard.module.css";

function TeamFilterListCard(props) {
    const [toggled, setToggled] = useState(false);

    const toggleFilter = () => {
        setToggled(props.toggleTeamFilter(props.team.id));
    }

    return (
        <div 
            className={`${styles.team_filter_list_card} ${
                toggled ? styles.selected_team_filter_list_card : ""}`}
            onClick={() => toggleFilter()}>
            {props.team.EN_name}
        </div>
    )
}

export default TeamFilterListCard
