import styles from "./TaskListCard.module.css"

function TaskListCard(props) {
    return (
        <div className={styles.task_list_card}>
            {props.task_data["name"]}
        </div>
    )
}

export default TaskListCard
