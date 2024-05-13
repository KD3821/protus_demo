import axios from "axios";
import router from "@/router";
import {
    REGISTER_USER_ACTION,
    LOGIN_USER_ACTION,
    AUTH_ACTION,
    AUTO_AUTH_ACTION,
    LOGOUT_ACTION,
    AUTO_LOGOUT_ACTION,
    SET_USER_TOKEN_DATA_MUTATION,
    REFRESH_ACTION,
    GET_USER_REFRESH_TOKEN_GETTER,
    GET_USER_TYPE,
    OAUTH_LOGIN_USER_ACTION,
} from "@/store/storeConstants";
import UserRegisterValidations from "@/services/UserRegisterValidations";
import UserLoginValidations from "@/services/UserLoginValidations";
import store from "@/store/store";

export default {
    async [REGISTER_USER_ACTION](context, payload) {
        let postData = {
            email: payload.email,
            password: payload.password
        }
        if (payload.isCustomer) {
            postData.username = payload.userName;
        } else {
            postData.name = payload.userName;
        }
        let headers = {
            'User-Type': payload.isCustomer === true ? 'customers' : 'companies'
        }
        try {
            let response = await axios.post('http://127.0.0.1:7077/auth/register/', postData, {headers: headers});
            if (response.status === 200) {
                await router.push('/confirm');
            }
        } catch (e) {
            if (e.response !== undefined) {
                throw UserRegisterValidations.getErrorMessageDetail(e.response.data);
            } else {
                await router.replace('/error');
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
    async [LOGIN_USER_ACTION](context, payload) {
        return context.dispatch(AUTH_ACTION, {
            ...payload,
            url: 'http://127.0.0.1:7077/auth/login/'
        });
    },
    async [AUTH_ACTION](context, payload) {
        let postData = {
            email: payload.email,
            password: payload.password,
        };
        let userType = payload.isCustomer === true ? 'customers' : 'companies'
        let headers = {'User-Type': userType}
        try {
            let response = await axios.post(payload.url, postData, {headers: headers});
            if  (response.status === 200) {
                let tokenData = {
                    email: payload.email,
                    accessToken: response.data.access,
                    refreshToken: response.data.refresh,
                    userType: userType
                }
                localStorage.setItem('userData', JSON.stringify(tokenData));
                context.commit(SET_USER_TOKEN_DATA_MUTATION, tokenData)
                let infoRoute = payload.isCustomer === true ? '/customer-info' : '/company-info'
                await router.push(infoRoute);
            }
        } catch (e) {
            if (e.response !== undefined) {
                throw UserLoginValidations.getErrorMessageDetail(e.response.data);
            } else {
                await router.replace('/error');
            }
        }
    },
    async [REFRESH_ACTION](context) {
        let refresh = store.getters[`auth/${GET_USER_REFRESH_TOKEN_GETTER}`]
        let userType = store.getters[`auth/${GET_USER_TYPE}`]
        if (refresh === '' || userType === '') {
            throw {'detail': 'Credentials not provided'}
        } else {
            let refreshData = {refresh: refresh};
            let headers = {'User-Type': userType}
            try {
                let response = await axios.post('http://127.0.0.1:7077/auth/refresh/', refreshData, {headers: headers});
                if (response.status === 200) {
                    let oldUserData = localStorage.getItem('userData');
                    if (oldUserData) {
                        let userData = JSON.parse(oldUserData)
                        let newUserData = {
                            email: userData.email,
                            accessToken: response.data.access,
                            refreshToken: userData.refreshToken,
                            userType: userData.userType
                        }
                        localStorage.setItem('userData', JSON.stringify(newUserData));
                        context.commit(SET_USER_TOKEN_DATA_MUTATION, newUserData);
                    }
                }
            } catch (e) {
                if (e.response !== undefined) {
                    await context.dispatch(AUTO_LOGOUT_ACTION);
                    throw e;
                }
            }
        }
    },
    [LOGOUT_ACTION](context) {
        context.commit(SET_USER_TOKEN_DATA_MUTATION, {
            email: null,
            accessToken: null,
            refreshToken: null,
            userType: null
        })
        localStorage.removeItem('userData');
    },
    [AUTO_LOGOUT_ACTION](context) {
        context.dispatch(LOGOUT_ACTION);
    },
    async [OAUTH_LOGIN_USER_ACTION](context, payload) {
        let postData = {
            email: payload.email,
            password: payload.password,
            session_id: payload.sid,
            scope: payload.scope
        };
        try {
            let response = await axios.post('http://127.0.0.1:7077/oauth/login/', postData);
            if  (response.status === 200) {
                window.location.href = response.data.return_url;
            }
        } catch (e) {
            if (e.response !== undefined) {
                throw UserLoginValidations.getErrorMessageDetail(e.response.data);
            } else {
                await router.replace('/error');
            }
        }
    },
}