import { useEffect, useRef, useState } from "react";
import ListFilter from "../../../components/ListFilter/ListFilter";
import filterIcon from "./../../../assets/icons/icons_filter.svg";
import styles from "./TaskList.module.css"
import TaskListPageSelector from "./TaskListPageSelector";
import { getTask, getTaskFilters } from "../../../services/tasks.service";

function TaskList(props) {
    const [taskFilters, setTaskFilters] = useState([]);
    const [showFilters, setShowFilters] = useState(false);
    const controller = useRef(null);

    const toggleFilters = () => {
        setShowFilters(!showFilters);
    }

    useEffect(() => {
        const getFilters = async() => {
            const filters = await getTaskFilters();
            setTaskFilters(filters);
        }
        getFilters()
    }, []);

    const selectTask = async(taskID) => {
        console.log(taskID);
        controller.current?.abort();
        controller.current = new AbortController();
        props.setSelectedTask({});

        try {
            const task = await getTask(taskID, {
                signal: controller.current.signal,
            });
            props.setSelectedTask(task);
        }
        catch (err) {
            if (err === "ERR_CANCELED") {
                return;
            }
            throw err;
        }
    }

    return (
        <div className={styles.task_list_container}>
            <div className={styles.task_list_header}>
                <div className={styles.task_list_header_text}>
                    <h3>Tasks</h3>
                </div>
                <div className={styles.task_list_filter} onClick={() => toggleFilters()}>
                    <img src={filterIcon}/>
                </div>
                <div className={`${styles.task_list_filter_dropdown} ${showFilters ? '' : styles.hidden}`}>
                    <ListFilter removeHeader={true} options={taskFilters} isSingular={false} id_key='id' text_key='display' setParentSelection={props.setSelectedTaskFilters}/>
                </div>
            </div>
            <ListFilter removeHeader={true} options={props.tasks} isSingular={true} id_key='id' text_key="name" setParentSelection={selectTask}/>
            <TaskListPageSelector page={props.page} maxPageCount={props.maxPageCount} setPage={props.setPage}/>
        </div>
    )
}

export default TaskList
