import styles from "./TeamFilterList.module.css";
import TeamFilterListCard from "./TeamFilterListCard";

function TeamFilterList(props) {
    return (
        <div className={styles.team_list_container}>
            <div className={styles.team_list_header}>
                <h3>Teams</h3>
            </div>
            <div className={styles.team_list_card_container}>
                { props.teams.map((team) => {
                    return <TeamFilterListCard key={team.id} team={team} toggleTeamFilter={props.toggleTeamFilter}/>
                })}
            </div>
        </div>

    )
}

export default TeamFilterList;
