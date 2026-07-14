import { useState } from "react";
import styles from "./ListFilter.module.css";
import ListFilterCard from "./ListFilterCard.jsx";

function ListFilter(props) {
    const [selectedOptions, setSelectedOptions] = useState([]);

    const selectOption = (option_id) => {
        if (props.isSingular) {
            setSelectedOptions([option_id]);
            props.setParentSelection(option_id);
        }
        else {
            var new_list = [...selectedOptions];
            if (selectedOptions.includes(option_id)) {
                new_list = selectedOptions.filter(id => id != option_id);
            }
            else {
                new_list.push(option_id);
            }
            setSelectedOptions(new_list);
            props.setParentSelection(new_list);
        }
    }

    return (
        <div className={styles.list_filter_container}>
            <div className={styles.list_filter_header}>
                <h3>{props.title}</h3>
            </div>
            <div className={styles.list_filter_card_container}>
                { props.options.map((option) => {
                    var id = option[props.id_key]
                    return <ListFilterCard key={id} id={id} data={option} text_key={props.text_key} selectedOptions={selectedOptions} selectOption={selectOption}/>
                }) }
            </div>
        </div>
    )
}

export default ListFilter;
