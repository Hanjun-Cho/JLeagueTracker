import { useEffect, useState } from "react"
import { getTasks, getTasksMaxPageCount } from "../services/tasks.service"
import TaskList from "../components/TaskList"
import PanelRouter from "../panels/PanelRouter"
import styles from "./DashboardPage.module.css"
import TeamFilterList from "../components/TeamFilterList"
import { getTeams } from "../services/teams.service"

function Dashboard() {
    const [selectedTask, setSelectedTask] = useState({});
    const [selectedTeamFilters, setSelectedTeamFilters] = useState([]);
    const [tasks, setTasks] = useState([]);
    const [teams, setTeams] = useState([]);
    const [page, setPage] = useState(1);
    const [maxPageCount, setMaxPageCount] = useState(0);

    const get_teams = async() => {
        const teams = await getTeams();
        setTeams(teams);
    }

    const update_tasks = async() => {
        const team_filters_flat = selectedTeamFilters.join(",");

        const maxPage = await getTasksMaxPageCount(team_filters_flat);
        setMaxPageCount(maxPage);

        const newTasks = await getTasks(page, team_filters_flat);
        setTasks(newTasks);
        
        setSelectedTask({});
    }

    const toggleTeamFilter = (team_id) => {
        // false means it is now no longer selected
        // true means it is now selected
        if (selectedTeamFilters.includes(team_id)) {
            setSelectedTeamFilters(selectedTeamFilters => selectedTeamFilters.filter(id => id !== team_id));
            return false;
        }
        else {
            setSelectedTeamFilters(selectedTeamFilters => [...selectedTeamFilters, team_id]);
            return true;
        }
    }

    useEffect(() => {
        update_tasks();
        get_teams();
    }, [page, selectedTeamFilters]);

    return (
        <div className={styles.dashboard_container}>
            <TaskList tasks={tasks} page={page} setPage={setPage} maxPageCount={maxPageCount} setSelectedTask={setSelectedTask} selectedTask={selectedTask}/>
            <PanelRouter update_tasks={update_tasks} selectedTask={selectedTask}/>
            <TeamFilterList teams={teams} toggleTeamFilter={toggleTeamFilter} update_tasks={update_tasks}/>
        </div>
    )
}

export default Dashboard
