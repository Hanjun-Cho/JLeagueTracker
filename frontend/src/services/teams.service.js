import { dashboard_api } from "./api";

export const getTeams = async() => {
    const res = await dashboard_api.get(`/teams`);
    return res.data;
}

export const getTeamSquad = async(teamID) => {
    const res = await dashboard_api.get(`/teams/squad?id=${teamID}`);
    return res.data;
}
