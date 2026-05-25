import { dashboard_api } from "./api";

export const getTasks = async (page, teamFiltersFlat) => {
    const res = await dashboard_api.get(`/tasks?page=${page}&filters=${teamFiltersFlat}`);
    return res.data;
};

export const getTasksMaxPageCount = async(teamFiltersFlat) => {
    const res = await dashboard_api.get(`/tasks/max_page_count?filters=${teamFiltersFlat}`);
    return res.data;
}
