import {
    GET_USER_EMAIL,
    IS_USER_AUTHENTICATED_GETTER,
    GET_USER_ACCESS_TOKEN_GETTER,
    GET_USER_REFRESH_TOKEN_GETTER,
    GET_USER_TYPE,
} from "@/store/storeConstants";

export default {
    [GET_USER_EMAIL]: (state) => {
        return state.email;
    },
    [IS_USER_AUTHENTICATED_GETTER](state) {
        return !!state.accessToken;
    },
    [GET_USER_ACCESS_TOKEN_GETTER]: (state) => {
        return state.accessToken;
    },
    [GET_USER_REFRESH_TOKEN_GETTER]: (state) => {
        return state.refreshToken;
    },
    [GET_USER_TYPE]: (state) => {
        return state.userType;
    },
};