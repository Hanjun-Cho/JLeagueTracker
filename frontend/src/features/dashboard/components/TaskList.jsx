import { useEffect, useState } from "react"
import { getTasks, getTasksMaxPageCount } from "../services/tasks.service"
import styles from "./TaskList.module.css"
import TaskListCard from "./TaskListCard";
import TaskListPageSelector from "./TaskListPageSelector";

function TaskList() {
    const [tasks, setTasks] = useState([]);
    const [page, setPage] = useState(1);
    const [maxPageCount, setMaxPageCount] = useState(0);

    useEffect(() => {
        getTasksMaxPageCount().then(setMaxPageCount);
        getTasks(page).then(setTasks);
        console.log(page);
    }, [page]);

    return (
        <div className={styles.task_list_container}>
            <div className={styles.task_list_header}>
                <h3>Tasks</h3>
            </div>
            <div className={styles.task_list_card_container}>
                {tasks.map((task) => {
                    return <TaskListCard key={task.id} task_data={task}/>
                })}
            </div>
            <TaskListPageSelector page={page} maxPageCount={maxPageCount} setPage={setPage}/>
        </div>
    )
}

export default TaskList
