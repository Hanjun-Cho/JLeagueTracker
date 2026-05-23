import styles from "./TaskListCard.module.css"

function TaskListCard(props) {
    return (
        <div 
            className={`${styles.task_list_card} ${
                props.selectedTask == props.task_data
                    ? styles.selected_task_list_card
                    : ""
            }`}
            onClick={() => props.setSelectedTask(props.task_data)}>
            {props.task_data["name"]}
        </div>
    )
}

export default TaskListCard
