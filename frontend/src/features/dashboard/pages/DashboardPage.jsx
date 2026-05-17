import TaskList from "../components/TaskList"
import styles from "./DashboardPage.module.css"

function Dashboard() {
    return (
        <div className={styles.dashboard_container}>
            <TaskList/>
        </div>
    )
}

export default Dashboard
