import { dashboard_api } from "./api";

export const getPlayer = async(playerID) => {
    const res = await dashboard_api.get(`/players?id=${playerID}`);
    return res.data;
};

const updatePlayer = async(playerID, data) => {
    const res = await dashboard_api.patch(`/players/update_player?id=${playerID}`, data);
    return res.data;
}

export const submitEnName = async(playerID, EnName) => {
    return updatePlayer(playerID, {
        "EN_name": EnName
    });
};

export const submitTransfermarktURL = async(playerID, transfermarktURL) => {
    return updatePlayer(playerID, {
        "transfermarkt_URL": transfermarktURL
    });
};

export const submitDateofBirth = async(playerID, dob) => {
    return updatePlayer(playerID, {
        "date_of_birth": dob
    });
}

export const submitOrdbID = async(playerID, ordbID) => {
    return updatePlayer(playerID, {
        "ordb_id": ordbID
    });
};

export const submitWyscoutID = async(playerID, wyscoutID) => {
    return updatePlayer(playerID, {
        "wyscout_id": wyscoutID
    });
};

export const removeTask = async(taskID) => {
    const res = await dashboard_api.delete(`/tasks/delete?id=${taskID}`);
    return res.data;
}
