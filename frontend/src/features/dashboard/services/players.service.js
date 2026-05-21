import { dashboard_api } from "./api";

export const getPlayer = async(playerID) => {
    const res = await dashboard_api.get(`/players?id=${playerID}`);
    return res.data;
};

export const submitEnName = async(playerID, EnName) => {
    const res = await dashboard_api.put(`/players/update_EN_name?id=${playerID}&EN_name=${EnName}`);
    return res.data;
};

export const submitTransfermarktURL = async(playerID, transfermarktURL) => {
    const res = await dashboard_api.put(`/players/update_transfermarkt_URL?id=${playerID}&URL=${transfermarktURL}`);
    return res.data;
};

export const submitOrdbID = async(playerID, ordbID) => {
    const res = await dashboard_api.patch(`/players/update_ordb_ID?id=${playerID}`, {
        "ordb_id": ordbID
    });
    return res.data;
};

export const submitWyscoutID = async(playerID, wyscoutID) => {
    const res = await dashboard_api.patch(`/players/update_ordb_ID?id=${playerID}`, {
        "wyscoutID": wyscoutID 
    });
    return res.data;
};

export const removeTask = async(taskID) => {
    const res = await dashboard_api.delete(`/tasks/delete?id=${taskID}`);
    return res.data;
}
