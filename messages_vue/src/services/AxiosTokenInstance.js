import axios from "axios";
import store from "@/store/store";
import {GET_USER_ACCESS_TOKEN_GETTER} from "@/store/storeConstants";

const axiosInstance = axios.create({
    baseURL: process.env.BASE_URL,
});

axiosInstance.interceptors.request.use(
    (config) => {
        const accessToken = store.getters[`auth/${GET_USER_ACCESS_TOKEN_GETTER}`];
        config.headers['Authorization'] = accessToken ? `Bearer ${accessToken}` : '';
        return config;
    },
    (error) => Promise.reject(error)
)

export default axiosInstance;