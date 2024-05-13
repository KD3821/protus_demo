<template>
  <div>
    <form v-on:submit.prevent>
      <h4>Войти в ЛК</h4>
      <my-input
          v-bind:value="email"
          v-on:input="email = $event.target.value.trim()"
          type="text"
          placeholder="Email"
      ></my-input>
      <div v-if="errors.email" class="error">
        {{ errors.email }}
      </div>
      <my-input
          v-bind:value="password"
          v-on:input="password = $event.target.value.trim()"
          type="password"
          placeholder="Пароль"
      ></my-input>
      <div v-if="errors.password" class="error">
        {{ errors.password }}
      </div>
      <div>
        <my-button
            class="btn"
            v-on:click="onLogin"
        >
          Войти
        </my-button>
        <my-button
            class="btn-protus"
            v-on:click="onProtusLogin"
        >
          Войти с PROTUS
        </my-button>
      </div>
      <div
          v-if="error"
          class="error"
      >
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions, mapMutations } from "vuex";
import LoginValidations from "@/services/LoginValidations";
import {
  LOGIN_ACTION,
  LOADING_SPINNER_SHOW_MUTATION,
} from "@/store/storeConstants";
import MyButton from "@/components/UI/MyButton";
export default {
  components: {MyButton},
  data() {
    return {
      email: '',
      password: '',
      errors: {},
      error: '',
      login_url: ''
    }
  },
  methods: {
    ...mapActions('auth', {
      login: LOGIN_ACTION
    }),
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async onLogin() {
      // check the validations
      let validations = new LoginValidations(
          this.email,
          this.password
      );
      this.errors = validations.checkLoginValidations();
      if ('email' in this.errors || 'password' in this.errors) {
        return false;
      }
      this.showLoading(true);
      await this.login({
        email: this.email,
        password: this.password
      }).catch(error => {
        this.showLoading(false);
        this.error = error
      });
      this.showLoading(false);
    },
    async onProtusLogin() {
      this.showLoading(true);
      try {
        await axios.get('http://127.0.0.1:8000/api/protus/login-session').then((response) => {
          this.showLoading(false);
          window.location.href = response.data.login_url;
        })
      } catch (e) {
        this.showLoading(false);
        this.$router.replace('/error');
      }
    }
  },
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 25%;
}
form > input {
  margin-bottom: 10px;
}
.error {
  color: red;
  font-size: 10pt;
}
.btn-protus {
  background-color: dodgerblue;
  color: wheat;
}
</style>