<template>
  <div class="oauth-notice">
    <h3 class="text-h7 font-weight-bold mb-4">
      Вы входите в приложение: <br>
      <span @click="toReturnUrl" class="return-link">{{ companyName }}</span><br>
      с помощью своего "PROTUS" аккаунта.
    </h3>
  <p>После входа приложению будут доступны следующие действия над вашим аккаунтом:</p>
  </div>
  <v-sheet class="mx-auto" width="300">
    <v-switch
        v-model="scope"
        color="success"
        label="Запрос баланса кошелька"
        value="check"
        hide-details
    ></v-switch>
    <v-switch
        v-model="scope"
        color="success"
        label="Резервирование средств"
        value="hold"
        hide-details
    ></v-switch>
    <v-switch
        v-model="scope"
        color="success"
        label="Списание средств"
        value="charge"
        hide-details
    ></v-switch>
    <v-form fast-fail @submit.prevent>
      <v-text-field
          v-model="email"
          :rules="emailRules"
          label="Email"
      ></v-text-field>
      <v-text-field
          v-model="password"
          :rules="passwordRules"
          label="Пароль"
          type="password"
      ></v-text-field>
      <v-btn
          @click="OAuthLoginUser"
          class="mt-2"
          type="submit"
          block
      >
        Войти
      </v-btn>
    </v-form>
    <div
        v-if="error"
        class="auth-error"
    >
      {{ error }}
    </div>
  </v-sheet>
</template>

<script>
import axios from "axios";
import Validations from "@/services/Validations";
import { mapActions, mapMutations } from "vuex";
import {
  LOADING_SPINNER_SHOW_MUTATION,
  LOGOUT_ACTION,
  OAUTH_LOGIN_USER_ACTION
} from "@/store/storeConstants";
import UserLoginValidations from "@/services/UserLoginValidations";
export default {
  data: () => ({
    sid: '',
    companyName: '',
    returnUrl: '',
    scope: ["check", "hold", "charge"],
    email: '',
    emailRules: [
      value => {
        if (Validations.checkEmail(value)) return true;
        return 'Некорректный email';
      },
      value => {
        if (Validations.checkUserEmail(value)) return true;
        return 'Недопустимый адрес электронной почты';
      }
    ],
    password: '',
    passwordRules: [
      value => {
        if (Validations.minLength(value, 6)) return true;
        return 'Пароль должен содержать минимум 6 символов';
      }
    ],
    errors: {},
    error: ''
  }),
  methods: {
    ...mapActions('auth', {
      oauthLogout: LOGOUT_ACTION,
      oauthLogin: OAUTH_LOGIN_USER_ACTION
    }),
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async OAuthLoginUser() {
      let validations = new UserLoginValidations(
          this.email,
          this.password
      );
      this.errors = validations.checkUserLoginValidations();
      if ('email' in this.errors || 'password' in this.errors) return false;
      try {
        await this.oauthLogin({
          email: this.email,
          password: this.password,
          sid: this.sid,
          scope: this.scope
        }).catch(error => {
          this.error = error;
        });
      } catch (err) {
        await this.toReturnUrl();
      }
    },
    async getCompanyInfo() {
      try {
        await axios.get(`http://127.0.0.1:7077/oauth/session-info/?sid=${this.sid}`).then((response) => {
          this.showLoading(false);
          this.companyName = response.data.company_name;
          this.returnUrl = response.data.return_url;
        })
      } catch (e) {
        this.$router.replace('/error');
        this.showLoading(false);
      }
    },
    async toReturnUrl() {
      window.location.href = this.returnUrl;
    }
  },
  mounted() {
    this.getCompanyInfo();
  },
  created() {
    this.sid = this.$route.query.sid;
    this.oauthLogout();
    this.showLoading(true);
  }
}
</script>

<style scoped>
.oauth-notice {
  width: 400px;
  text-align: center;
  margin: 0 auto;
}
.return-link {
  color: blue;
  cursor: pointer;
}
</style>