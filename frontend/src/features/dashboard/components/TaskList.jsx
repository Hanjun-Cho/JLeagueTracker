import styles from "./TaskList.module.css"
import TaskListCard from "./TaskListCard";
import TaskListPageSelector from "./TaskListPageSelector";

function TaskList(props) {
    return (
        <div className={styles.task_list_container}>
            <div className={styles.task_list_header}>
                <h3>Tasks</h3>
            </div>
            <div className={styles.task_list_card_container}>
                {props.tasks.map((task) => {
                    return <TaskListCard key={task.id} task_data={task} setSelectedTask={props.setSelectedTask}/>
                })}
            </div>
            <TaskListPageSelector page={props.page} maxPageCount={props.maxPageCount} setPage={props.setPage}/>
        </div>
    )
}

export default TaskList
