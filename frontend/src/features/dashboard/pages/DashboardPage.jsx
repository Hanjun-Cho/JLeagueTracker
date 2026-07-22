import { useEffect, useRef, useState } from "react"
import { getTasks, getTasksMaxPageCount } from "../../../services/tasks.service"
import TaskList from "../components/TaskList"
import PanelRouter from "../panels/PanelRouter"
import styles from "./DashboardPage.module.css"
import { getTeams } from "../../../services/teams.service"
import ListFilter from "../../../components/ListFilter/ListFilter"

function Dashboard() {
    const [selectedTask, setSelectedTask] = useState({});
    const [selectedTeamFilters, setSelectedTeamFilters] = useState([]);
    const [selectedTaskFilters, setSelectedTaskFilters] = useState([]);
    const [tasks, setTasks] = useState([]);
    const [teams, setTeams] = useState([]);
    const [page, setPage] = useState(1);
    const [maxPageCount, setMaxPageCount] = useState(0);
    const controller = useRef(null);

    const get_teams = async() => {
        const teams = await getTeams();
        setTeams(teams);
    }

    const update_tasks = async() => {
        controller.current?.abort();
        controller.current = new AbortController();

        setSelectedTask({});
        setTasks([]);
        const team_filters_flat = selectedTeamFilters.join(",");
        const task_filters_flat = selectedTaskFilters.join(",");

        try {
            const maxPage = await getTasksMaxPageCount(team_filters_flat, task_filters_flat, {
                signal: controller.current.signal,
            });
            setMaxPageCount(maxPage);

            if (page > maxPage) {
                setPage(maxPage)
            }

            const newTasks = await getTasks(page, team_filters_flat, task_filters_flat, {
                signal: controller.current.signal,
            });
            setTasks(newTasks);
        }
        catch (err) {
            if (err.code == "ERR_CANCELLED") return;
            throw err;
        }
    }

    useEffect(() => {
        get_teams();
    }, []);

    useEffect(() => {
        update_tasks();
    }, [page, selectedTeamFilters, selectedTaskFilters]);

    return (
        <div className={styles.dashboard_container}>
            <TaskList tasks={tasks} page={page} setPage={setPage} maxPageCount={maxPageCount} setSelectedTask={setSelectedTask} selectedTask={selectedTask} setSelectedTaskFilters={setSelectedTaskFilters}/>
            <div>
            { Object.keys(selectedTask).length > 0 &&
                <PanelRouter update_tasks={update_tasks} selectedTask={selectedTask}/>
            }
            </div>
            <div className={styles.team_filter_container}>
                <ListFilter title="Teams" options={teams} isSingular={false} id_key="id" text_key="EN_name" setParentSelection={setSelectedTeamFilters}/>
            </div>
        </div>
    )
}

export default Dashboard
