import { useEffect, useState } from "react";
import { getPlayer } from "../services/players.service";
import MissingEnNamePanel from "./MissingENNamePanel";
import MissingTransfermarktURLPanel from "./MissingTransfermarktURLPanel";
import PanelHeader from "./PanelHeader";
import { removeTask } from "../services/players.service";
import MissingOrdbIDPanel from "./MissingOrdbIDPanel";

function PanelRouter(props) {
    const [player, setPlayer] = useState({});

    useEffect(() => {
        if (props.selectedTask["player_id"]) {
            getPlayer(props.selectedTask["player_id"]).then(setPlayer)
        }
    }, [props.selectedTask["player_id"]])

    const remove = async() => {
        removeTask(props.selectedTask["id"])
        props.update_tasks()
    }

    return (
        <div>
            <PanelHeader player={player}/>
            { props.selectedTask["task_type"] == "MISSING EN_NAME" &&
                <MissingEnNamePanel remove={remove} player={player}/>
            }
            { props.selectedTask["task_type"] == "MISSING TRANSFERMARKT_URL" &&
                <MissingTransfermarktURLPanel remove={remove} player={player}/>
            }
            { props.selectedTask["task_type"] == "MISSING ORDB_ID" &&
                <MissingOrdbIDPanel remove={remove} player={player}/>
            }
        </div>
    )
}

export default PanelRouter;
