import { SET_USER_TOKEN_DATA_MUTATION } from "@/store/storeConstants";

export default {
    [SET_USER_TOKEN_DATA_MUTATION](state, payload) {
        state.email = payload.email;
        state.username = payload.username;
        state.accessToken = payload.accessToken;
        state.refreshToken = payload.refreshToken;
    }
};