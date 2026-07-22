import ListFilter from "../../../components/ListFilter/ListFilter";
import styles from "./TaskList.module.css"
import TaskListPageSelector from "./TaskListPageSelector";

function TaskList(props) {
    return (
        <div className={styles.task_list_container}>
            <div className={styles.task_list_header}>
                
            </div>
            <ListFilter title="Tasks" removeHeader={true} options={props.tasks} isSingular={true} id_key='id' text_key="name" setParentSelection={props.setSelectedTask}/>
            <TaskListPageSelector page={props.page} maxPageCount={props.maxPageCount} setPage={props.setPage}/>
        </div>
    )
}

export default TaskList
