import styles from "./ListFilter.module.css";

function ListFilterCard(props) {
    return (
        <div 
            className={`${styles.list_filter_card} ${
                (props.selectedOptions.includes(props.id)) ? styles.selected_list_filter_card : ""}`}
            onClick={() => props.selectOption(props.id)}>
            {props.data[props.text_key]}
        </div>
    )
}

export default ListFilterCard;
