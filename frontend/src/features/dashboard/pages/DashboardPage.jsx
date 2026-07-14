import { useEffect, useState } from "react"
import { getTasks, getTasksMaxPageCount } from "../../../services/tasks.service"
import TaskList from "../components/TaskList"
import PanelRouter from "../panels/PanelRouter"
import styles from "./DashboardPage.module.css"
import { getTeams } from "../../../services/teams.service"
import ListFilter from "../../../components/ListFilter/ListFilter"

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

    useEffect(() => {
        update_tasks();
        get_teams();
    }, [page, selectedTeamFilters]);

    return (
        <div className={styles.dashboard_container}>
            <TaskList tasks={tasks} page={page} setPage={setPage} maxPageCount={maxPageCount} setSelectedTask={setSelectedTask} selectedTask={selectedTask}/>
            <PanelRouter update_tasks={update_tasks} selectedTask={selectedTask}/>
            <ListFilter title="Teams" options={teams} isSingular={false} id_key="id" text_key="EN_name" setParentSelection={setSelectedTeamFilters}/>
        </div>
    )
}

export default Dashboard
