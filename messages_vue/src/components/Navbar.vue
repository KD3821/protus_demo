<template>
  <div class="navbar">
    <div v-on:click="$router.push('/')" class="logo">MESSAGE SERVICE</div>
    <div v-if="isAuthenticated" class="navbar__bttns">
      <span id="user">Пользователь: {{ userName }}</span>
      <my-button v-on:click="$router.push('/campaigns')">Рассылки</my-button>
      <my-button v-on:click="$router.push('/customers')">Клиенты</my-button>
      <my-button v-on:click="onLogout">Выход</my-button>
    </div>
    <div v-else>
      <my-button v-on:click="$router.push('/login')">Вход</my-button>
      <my-button v-on:click="$router.push('/register')">Регистрация</my-button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import {
  IS_USER_AUTHENTICATED_GETTER,
  GET_USER_NAME,
  LOGOUT_ACTION
} from "@/store/storeConstants";
export default {
  computed: {
    ...mapGetters('auth', {
      isAuthenticated: IS_USER_AUTHENTICATED_GETTER
    }),
    ...mapGetters('auth', {
      userName: GET_USER_NAME
    })
  },
  methods: {
    ...mapActions('auth', {
      logout: LOGOUT_ACTION
    }),
    onLogout() {
      this.logout();
      this.$router.replace('/login');
    }
  }
}
</script>

<style scoped>
.navbar {
  min-height: 30px;
  background-color: dodgerblue;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo {
  margin-left: 20px;
  color: white;
  font-size: 1.2em;
  cursor: pointer;
}
#user {
  color: white;
  margin: 0 5px;
}
</style>