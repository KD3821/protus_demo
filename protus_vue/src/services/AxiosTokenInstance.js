import axios from "axios";
import store from "@/store/store";
import {
    GET_USER_ACCESS_TOKEN_GETTER,
    GET_USER_TYPE
} from "@/store/storeConstants";

const axiosInstance = axios.create({
    baseURL: process.env.BASE_URL,
});

axiosInstance.interceptors.request.use(
    (config) => {
        const accessToken = store.getters[`auth/${GET_USER_ACCESS_TOKEN_GETTER}`];
        const userType = store.getters[`auth/${GET_USER_TYPE}`];
        config.headers['Authorization'] = accessToken ? `Bearer ${accessToken}` : '';
        config.headers['User-Type'] = userType || '';
        return config;
    },
    (error) => Promise.reject(error)
)

export default axiosInstance;