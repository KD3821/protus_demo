<template>
  <v-container class="navbar">
    <v-app-bar
        color="primary"
        density="compact"
    >
      <router-link to="/" class="ml-3">
        <b>PROTUS</b>ervice
      </router-link>
      <v-spacer />
      <div v-if="!isAuthenticated">
        <router-link to="/login" style="color:white">
          <v-btn variant="outlined" class="mr-3">
            Вход
          </v-btn>
        </router-link>
        <router-link to="/register" style="color:white">
          <v-btn variant="outlined" class="mr-3">
            Регистрация
          </v-btn>
        </router-link>
      </div>
      <div v-else>
        <v-icon
            :icon=iconType
        ></v-icon>
        {{ userEmail }}
        <router-link :to=infoRoute class="ml-3">
          <v-btn variant="outlined" class="mx-3">
            Информация
          </v-btn>
        </router-link>
        <v-btn variant="outlined" class="mx-3" @click="onLogout">
          Выход
        </v-btn>
      </div>
    </v-app-bar>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import {
  GET_USER_EMAIL,
  IS_USER_AUTHENTICATED_GETTER,
  LOGOUT_ACTION,
  GET_USER_TYPE,
} from "@/store/storeConstants";
export default {
  data: () => ({
    infoRoute: '',
    iconType: ''
  }),
  computed: {
    ...mapGetters('auth', {
      isAuthenticated: IS_USER_AUTHENTICATED_GETTER,
      userEmail: GET_USER_EMAIL,
      userType: GET_USER_TYPE
    }),
  },
  methods: {
    ...mapActions('auth', {
      logout: LOGOUT_ACTION
    }),
    onLogout() {
      this.logout();
      this.$router.replace('/');
    },
    setInfoRoute() {
      this.infoRoute = this.userType === 'companies' ? '/company-info' : '/customer-info';
      this.iconType = this.userType === 'companies' ? 'mdi-briefcase-account' : 'mdi-account-circle-outline';
    },
  },
  mounted() {
    this.setInfoRoute();
  },
  watch: {
    userType: function(newValue, oldValue) {
      this.setInfoRoute()
    }
  },
}
</script>

<style scoped>
a:link, a:visited {
  color: white;
  text-decoration: none;
}
.navbar {
  margin-bottom: 50px;
}
</style>