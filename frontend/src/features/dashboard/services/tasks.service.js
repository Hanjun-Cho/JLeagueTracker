import { dashboard_api } from "./api";

export const getTasks = async (page) => {
    const res = await dashboard_api.get(`/tasks?page=${page}`);
    return res.data;
};

export const getTasksMaxPageCount = async() => {
    const res = await dashboard_api.get("/tasks/max_page_count");
    return res.data;
}
