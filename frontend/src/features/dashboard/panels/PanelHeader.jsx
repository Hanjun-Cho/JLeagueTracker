function PanelHeader(props) {
    return (
        <div>
            <h3>Panel Header ({props.player["JP_name"]}, {props.player["EN_name"]}, {props.player["team"]}, {props.player["date_of_birth"]}, {props.player["back_number"]})</h3>
            <a href={props.player["transfermarkt_URL"]} target="_blank">transfermarkt</a>
        </div>
    ) 
}

export default PanelHeader
