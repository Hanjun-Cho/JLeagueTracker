import styles from "./TaskListPageSelector.module.css"
import nextIcon from "./../../../assets/icons/icons_next.svg"
import jumpIcon from "./../../../assets/icons/icons_jump.svg"
import { useState } from "react";

function TaskListPageSelector(props) {
    const [start, setStart] = useState(props.page);
    const jumpIncrement = 5;

    const revertPage = (increment) => {
        if (props.page <= increment) {
            props.setPage(1)
        }
        else {
            props.setPage(props.page - increment)
        }
        setStart(Math.max(1, 
            Math.min(props.maxPageCount - jumpIncrement + 1, props.page - increment)))
    }

    const jumpPage = (increment) => {
        if (props.page + increment > props.maxPageCount) {
            props.setPage(props.maxPageCount)
        }
        else {
            props.setPage(props.page + increment)
        }
        setStart(Math.max(1, Math.min(props.maxPageCount - jumpIncrement + 1, props.page + increment)))
    }

    return (
        <div className={styles.task_list_page_selector}>
            <button className={styles.page_move_button} onClick={() => revertPage(jumpIncrement)}>
                <img className={styles.revert_button} src={jumpIcon}/>
            </button>
            <button className={styles.page_move_button} onClick={() => revertPage(1)}>
                <img className={styles.back_button} src={nextIcon}/>
            </button>

            <div className={styles.page_selector_container}>
                {Array.from({length: Math.min(props.maxPageCount, jumpIncrement)}, (_, i) => {
                    const page_value = start + i;
                    return <button key={i} disabled={props.page == page_value} onClick={() => props.setPage(page_value)}>{page_value}</button>
                })}
            </div>

            <button className={styles.page_move_button} onClick={() => jumpPage(1)}>
                <img className={styles.next_button} src={nextIcon}/>
            </button>
            <button className={styles.page_move_button} onClick={() => jumpPage(jumpIncrement)}>
                <img src={jumpIcon}/>
            </button>
        </div>
    )
}

export default TaskListPageSelector
