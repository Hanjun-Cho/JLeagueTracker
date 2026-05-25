import { dashboard_api } from "./api";

export const getTeams = async() => {
    const res = await dashboard_api.get(`/teams`);
    return res.data;
}
