import { dashboard_api } from "./api";

export const getTasks = async (page, teamFiltersFlat, taskFiltersFlat, signal) => {
    const res = await dashboard_api.get(`/tasks?page=${page}&team_filters=${teamFiltersFlat}&task_type_filters=${taskFiltersFlat}`, signal);
    return res.data;
};

export const getTask = async (taskID, signal) => {
    const res = await dashboard_api.get(`/task?id=${taskID}`, signal);
    return res.data;
}

export const getTaskFilters = async() => {
    const res = await dashboard_api.get('/tasks/filters');
    return res.data;
}

export const getTasksMaxPageCount = async(teamFiltersFlat, taskFiltersFlat, signal) => {
    const res = await dashboard_api.get(`/tasks/max_page_count?team_filters=${teamFiltersFlat}&task_type_filters=${taskFiltersFlat}`, signal);
    return res.data;
}

export const removeTask = async(taskID) => {
    const res = await dashboard_api.delete(`/tasks/delete?id=${taskID}`);
    return res.data;
}
