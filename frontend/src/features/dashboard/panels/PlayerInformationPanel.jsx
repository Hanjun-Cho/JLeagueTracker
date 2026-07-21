import PanelHeader from "./PanelHeader";

function PlayerInformationPanel(props) {
    return (
        <div>
            <PanelHeader player={props.player}/>
        </div>
    )
}

export default PlayerInformationPanel;
