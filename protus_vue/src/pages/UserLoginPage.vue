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
          @click="loginUser"
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
import UserLoginValidations from "@/services/UserLoginValidations";
import Validations from "@/services/Validations";
import { mapActions } from "vuex";
import { LOGIN_USER_ACTION } from "@/store/storeConstants";
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
    errors: {},
    error: ''
  }),
  methods: {
    ...mapActions('auth', {
      login: LOGIN_USER_ACTION
    }),
    async loginUser() {
      let validations = new UserLoginValidations(
          this.email,
          this.password
      );
      this.errors = validations.checkUserLoginValidations();
      if ('email' in this.errors || 'password' in this.errors) return false;
      await this.login({
        email: this.email,
        password: this.password,
        isCustomer: this.customer
      }).catch(error => {
        this.error = error
      });
    }
  }
}
</script>

<style>

</style>