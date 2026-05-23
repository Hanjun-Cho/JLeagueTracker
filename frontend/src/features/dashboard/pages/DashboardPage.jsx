import { useEffect, useState } from "react"
import { getTasks, getTasksMaxPageCount } from "../services/tasks.service"
import TaskList from "../components/TaskList"
import PanelRouter from "../panels/PanelRouter"
import styles from "./DashboardPage.module.css"

function Dashboard() {
    const [selectedTask, setSelectedTask] = useState({});
    const [tasks, setTasks] = useState([]);
    const [page, setPage] = useState(1);
    const [maxPageCount, setMaxPageCount] = useState(0);

    const update_tasks = async() => {
        const maxPage = await getTasksMaxPageCount();
        setMaxPageCount(maxPage);

        const newTasks = await getTasks(page);
        setTasks(newTasks);
        
        setSelectedTask({});
    }

    useEffect(() => {
        update_tasks()
    }, [page]);

    return (
        <div className={styles.dashboard_container}>
            <TaskList tasks={tasks} page={page} setPage={setPage} maxPageCount={maxPageCount} setSelectedTask={setSelectedTask} selectedTask={selectedTask}/>
            <PanelRouter update_tasks={update_tasks} selectedTask={selectedTask}/>
        </div>
    )
}

export default Dashboard
