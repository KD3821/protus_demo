import axios from "axios";
import router from "@/router/router";
import SignupValidations from "@/services/SignupValidations";
import LoginValidations from "@/services/LoginValidations";
import {
    SIGNUP_ACTION,
    LOGIN_ACTION,
    AUTH_ACTION,
    AUTO_AUTH_ACTION,
    LOGOUT_ACTION,
    AUTO_LOGOUT_ACTION,
    REFRESH_ACTION,
    SET_USER_TOKEN_DATA_MUTATION,
    GET_USER_REFRESH_TOKEN_GETTER,
    LOADING_SPINNER_SHOW_MUTATION,
    OAUTH_LOGIN_USER_ACTION,
} from "@/store/storeConstants";
import store from "@/store/store";

export default {
    async [SIGNUP_ACTION](context, payload) {
        let postData = {
            username: payload.username,
            email: payload.email,
            password: payload.password,
        };
        context.commit(LOADING_SPINNER_SHOW_MUTATION, true, { root: true })
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/accounts/register', postData);
            if (response.status === 201) {
                await router.push('/login');
            }
        } catch (e) {
            context.commit(LOADING_SPINNER_SHOW_MUTATION, false, { root: true })
            if (e.response !== undefined) {
                throw SignupValidations.getErrorMessageDetail(e.response.data.errors);
            } else {
                console.log(e.response);
            }
        }
        context.commit(LOADING_SPINNER_SHOW_MUTATION, false, { root: true })
    },
    async [REFRESH_ACTION](context) {
        let refreshData = {
            refresh: store.getters[`auth/${GET_USER_REFRESH_TOKEN_GETTER}`]
        };
        if (!refreshData) {
            await router.push('/logout');
        }
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/accounts/token/refresh', refreshData);
            if (response.status === 200) {
                let oldUserData = localStorage.getItem('userData');
                if (oldUserData) {
                    let userData = JSON.parse(oldUserData)
                    let newUserData = {
                        email: userData.email,
                        username: userData.username,
                        refreshToken: userData.refreshToken,
                        accessToken: response.data.access
                    }
                    localStorage.setItem('userData', JSON.stringify(newUserData));
                    context.commit(SET_USER_TOKEN_DATA_MUTATION, newUserData)
                }
            }
        } catch (e) {
            if (e.response !== undefined) {
                await context.dispatch(AUTO_LOGOUT_ACTION);
                throw e;
            }
        }
    },
    async [AUTO_AUTH_ACTION](context) {
        let userData = localStorage.getItem('userData');
        if (userData) {
            context.commit(
                SET_USER_TOKEN_DATA_MUTATION,
                JSON.parse(userData)
            );
        }
    },
    async [LOGIN_ACTION](context, payload) {
        return context.dispatch(AUTH_ACTION, {
            ...payload,
            url: 'http://127.0.0.1:8000/api/accounts/login'
        });
    },
    async [AUTH_ACTION](context, payload) {
        let postData = {
            email: payload.email,
            password: payload.password,
        };
        try {
            let response = await axios.post(payload.url, postData);
            if  (response.status === 200) {
                let tokenData = {
                    email: response.data.email,
                    username: response.data.username,
                    accessToken: response.data.tokens.access,
                    refreshToken: response.data.tokens.refresh
                }
                localStorage.setItem('userData', JSON.stringify(tokenData));
                context.commit(SET_USER_TOKEN_DATA_MUTATION, tokenData)
                await router.push('/campaigns');
            }
        } catch (e) {
            if (e.response !== undefined) {
                throw LoginValidations.getErrorMessageDetail(e.response.data);
            } else {
                await router.replace('/error');
            }
        }
    },
    async [LOGOUT_ACTION](context) {
        let logoutData = {
            refresh: store.getters[`auth/${GET_USER_REFRESH_TOKEN_GETTER}`]
        };
        context.commit(SET_USER_TOKEN_DATA_MUTATION, {
            email: null,
            username: null,
            accessToken: null,
            refreshToken: null
        });
        localStorage.removeItem('userData');
        try {
            await axios.post('http://127.0.0.1:8000/api/accounts/logout', logoutData);
        } catch (e) {
            await router.replace('/error');
        }
    },
    [AUTO_LOGOUT_ACTION](context) {
        context.commit(SET_USER_TOKEN_DATA_MUTATION, {
            email: null,
            username: null,
            accessToken: null,
            refreshToken: null
        })
        localStorage.removeItem('userData');
    },
    async [OAUTH_LOGIN_USER_ACTION](context, payload) {
        let postData = {
            confirmation_id: payload
        };
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/protus/confirm-session', postData);
            if  (response.status === 200) {
                let tokenData = {
                    email: response.data.email,
                    username: response.data.username,
                    accessToken: response.data.access,
                    refreshToken: response.data.refresh
                }
                localStorage.setItem('userData', JSON.stringify(tokenData));
                context.commit(SET_USER_TOKEN_DATA_MUTATION, tokenData)
            }
        } catch (e) {
            await router.replace('/error');
        }
    },
};