import { submitDateofBirth } from "../services/players.service"

function MissingBirthdayPanel(props) {
    const submit = async() => {
        var birthday = document.getElementById("birthday").value
        
        if (birthday.length > 0) {
            submitDateofBirth(props.player["id"], birthday)
            props.remove()
        }
    }

    return (
        <div>
            Missing Date of Birth
            <h4>{props.player["EN_name"] == null ? props.player["JP_name"] : props.player["EN_name"]}</h4>

            <input type="date" id="birthday" name="birthday"/>
            <button type="submit" onClick={() => submit()}>submit</button>
        </div>
    )
}

export default MissingBirthdayPanel 
