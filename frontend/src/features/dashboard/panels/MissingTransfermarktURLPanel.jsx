import { submitTransfermarktURL } from "../services/players.service"

function MissingTransfermarktURLPanel(props) {
    const submit = async() => {
        var url = document.getElementById("transfermarkt_URL").value
        submitTransfermarktURL(props.player["id"], url)
        props.remove()
    }

    return (
        <div>
            Missing Transfermarkt_URL
            <h4>{props.player["JP_name"]}</h4>

            <input text="text" id="transfermarkt_URL" name="url" placeholder="enter transfermarkt URL"/>
            <button type="submit" onClick={() => submit()}>submit</button>
        </div>
    )
}

export default MissingTransfermarktURLPanel
