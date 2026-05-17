import { submitEnName } from "../services/players.service"

function MissingEnNamePanel(props) {
    const submit = async() => {
        var EnName = document.getElementById("EN_name").value
        submitEnName(props.player["id"], EnName)
        props.remove()
    }

    return (
        <div>
            Missing EN_Name
            <h4>{props.player["JP_name"]}</h4>

            <input type="text" id="EN_name" name="name" placeholder="enter EN_name"/>
            <button type="submit" onClick={() => submit()}>submit</button>
        </div>
    )
}

export default MissingEnNamePanel
