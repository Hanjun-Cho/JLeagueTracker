import { submitWyscoutID } from "../services/players.service"

function MissingWyscoutIDPanel(props) {
    const submit = async() => {
        var wyscout_id = document.getElementById("wyscout_id").value
        
        if (wyscout_id.length > 0) {
            submitWyscoutID(props.player["id"], wyscout_id)
            props.remove()
        }
    }

    return (
        <div>
            Missing Wyscout ID 
            <h4>{props.player["EN_name"] == null ? props.player["JP_name"] : props.player["EN_name"]}</h4>

            <input type="text" id="wyscout_id" name="wyscout_id" placeholder="enter WYSCOUT ID"/>
            <button type="submit" onClick={() => submit()}>submit</button>
        </div>
    )
}

export default MissingWyscoutIDPanel
