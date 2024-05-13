<template>
  <v-sheet class="mx-auto" width="300">
    <v-form fast-fail @submit.prevent>
      <div class="switch-toggle">
        <span id="switchLabel">Компания</span>
        <v-switch
            v-model="customer"
            label="Физическое лицо"
            hide-details
            indeterminate
        ></v-switch>
      </div>
      <v-text-field
          v-model="email"
          :rules="emailRules"
          label="Email"
          prepend-inner-icon="mdi-email"
      ></v-text-field>
      <v-text-field v-if="customer"
          v-model="username"
          label="Имя пользователя"
          prepend-inner-icon="mdi-account"
      ></v-text-field>
      <v-text-field v-else
          v-model="name"
          label="Название компании"
          prepend-inner-icon="mdi-account"
      ></v-text-field>
      <v-text-field
          v-model="password"
          :rules="passwordRules"
          label="Пароль"
          :type="showPassword ? 'text' : 'password'"
          prepend-inner-icon="mdi-lock"
          :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          @click:appendInner="showPassword = !showPassword"
      ></v-text-field>
      <v-btn
          @click="registerUser"
          class="mt-2"
          type="submit"
          block
      >
        Зарегистрироваться
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
import Validations from "@/services/Validations";
import { mapActions } from "vuex";
import { REGISTER_USER_ACTION } from "@/store/storeConstants";
import UserRegisterValidations from "@/services/UserRegisterValidations";
export default {
  data: () => ({
    showPassword: false,
    customer: true,
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
    username: '',
    name: '',
    errors: {},
    error: ''
  }),
  methods: {
    ...mapActions('auth', {
      register: REGISTER_USER_ACTION
    }),
    async registerUser() {
      let validations = new UserRegisterValidations(
          this.email,
          this.password
      );
      this.errors = validations.checkUserRegisterValidations();
      if ('email' in this.errors || 'password' in this.errors) return false;
      await this.register({
        email: this.email,
        password: this.password,
        isCustomer: this.customer,
        userName: this.customer === true ? this.username : this.name,
      }).catch(error => {
        this.error = error;
      });
    },
  }
}
</script>

<style>
.auth-error {
  color: red;
  font-size: 10pt;
  margin-top: 5px;
  text-align: center;
}
.switch-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
}
#switchLabel {
  color: grey;
  margin-right: 10px;
}
</style>