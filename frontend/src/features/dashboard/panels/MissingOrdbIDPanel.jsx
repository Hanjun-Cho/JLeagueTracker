import { submitOrdbID } from "../services/players.service"

function MissingOrdbIDPanel(props) {
    const submit = async() => {
        var ordb_id = document.getElementById("ordb_id").value
        
        if (ordb_id.length > 0) {
            submitOrdbID(props.player["id"], ordb_id)
            props.remove()
        }
    }

    return (
        <div>
            Missing ORDB ID 
            <h4>{props.player["EN_name"] == null ? props.player["JP_name"] : props.player["EN_name"]}</h4>

            <input type="text" id="ordb_id" name="ordb_id" placeholder="enter ORDB ID"/>
            <button type="submit" onClick={() => submit()}>submit</button>
        </div>
    )
}

export default MissingOrdbIDPanel
