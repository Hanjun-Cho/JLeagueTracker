function PanelHeader(props) {
    return (
        <div>
            <h3>Panel Header ({props.player["JP_name"]}, {props.player["EN_name"]}, {props.player["team"]}, {props.player["date_of_birth"]})</h3>
        </div>
    ) 
}

export default PanelHeader
