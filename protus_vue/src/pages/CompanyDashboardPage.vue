<template>
  <v-container v-show="!!companyName" class="user-info">
    <v-card elevation="8">
      <v-row class="ma-0 pa-0">
        <v-col class="bg-grey-lighten-3">
          <v-icon
              icon="mdi-briefcase-account"
          ></v-icon>
          {{ companyName }}
        </v-col>
        <v-col class="text-left">
          <v-row>
            <v-col>
              <v-icon
                  icon="mdi-pound-box"
              ></v-icon> {{ clientId }}<br>
              <v-icon
                  icon="mdi-shield-key"
              ></v-icon> {{ clientSecret }}
            </v-col>
            <v-col cols="3">
              <v-btn
                  class="text-none"
                  color="warning"
                  variant="flat"
                  rounded
              >+ Услуга</v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
    <v-card class="mt-3" elevation="6">
      <v-list density="compact">
        <v-list-subheader>Ваши услуги:</v-list-subheader>
        <v-list-item
            v-if="services.length"
            v-for="service in services"
            :key="service.service_id"
            :title="'Название: ' + service.name"
            class="bg-grey-lighten-3 mt-2"
        >
          <v-spacer class="mt-3"></v-spacer>
          <v-row>
            <v-col class="align-self-center text-left">
              <p>Идентификатор: {{ service.service_id }}</p>
            </v-col>
            <v-col cols="4" class="align-self-center">
              <p>Стоимость: {{ service.price }} руб.</p>
            </v-col>
            <v-col cols="4" class="align-self-center">
              <v-btn
                  class="text-none"
                  color="warning"
                  variant="flat"
                  width="140"
                  rounded
              >Редактировать</v-btn>
              <v-btn
                  class="text-none"
                  color="info"
                  variant="flat"
                  rounded
              >Инвойсы</v-btn>
              <v-btn
                  class="text-none"
                  color="success"
                  variant="flat"
                  rounded
              >Операции</v-btn>
            </v-col>
          </v-row>
        </v-list-item>
        <v-list-item v-else>
         Вы пока не добавили услуг для ваших пользователей.
        </v-list-item>
        <v-divider thickness="2"></v-divider>
      </v-list>
    </v-card>
  </v-container>
</template>

<script>
import axiosInstance from "@/services/AxiosTokenInstance";
import { mapActions, mapMutations } from "vuex";
import MyLoader from "@/components/MyLoader";
import {
  REFRESH_ACTION,
  LOADING_SPINNER_SHOW_MUTATION
} from "@/store/storeConstants";

export default {
  components: {
    MyLoader
  },
  data: () => ({
    companyName: '',
    clientId: '',
    clientSecret: '',
    services: [],
    isRefreshed: false,
  }),
  methods: {
    ...mapActions('auth', {
      getRefresh: REFRESH_ACTION
    }),
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async getCompanyDashboard() {
      try {
        await axiosInstance.get('http://127.0.0.1:7077/billing/dashboard/').then((response) => {
          this.showLoading(false);
          this.companyName = response.data.provider.name;
          this.clientId = response.data.provider.client_id;
          this.clientSecret = response.data.provider.client_secret;
          this.services = response.data.services
          this.isRefreshed = false
        });
      } catch (e) {
        if (typeof e.response !== "undefined" && e.response.status === 401 && !this.isRefreshed) {
          try {
            await this.getRefresh();
            this.isRefreshed = true;
          } catch (err) {
            this.$router.replace('/login');
            this.showLoading(false);
          }
        } else {
          this.$router.replace('/error');
          this.showLoading(false);
        }
      }
    },
    async runGetCompanyDashboard() {
      this.showLoading(true);
      do {
        await this.getCompanyDashboard();
      } while (this.isRefreshed)
    }
  },
  mounted() {
    this.runGetCompanyDashboard();
  }
}
</script>

<style scoped>
.user-info {
  text-align: center;
}
</style>