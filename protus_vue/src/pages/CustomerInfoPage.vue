<template>
  <v-container v-show="!!userName" class="user-info">
    <v-card elevation="8">
      <v-row class="ma-0 pa-0">
        <v-col class="bg-grey-lighten-3">
          <v-icon
            icon="mdi-account-circle-outline"
          ></v-icon>
         {{ userName }}
        </v-col>
        <v-col class="text-left">
          <v-row>
            <v-col>
              <v-icon
                  icon="mdi-pound-box"
              ></v-icon> {{ userUuid }}<br>
              <v-icon
                  icon="mdi-wallet"
              ></v-icon> {{ walletBalance }} руб.
            </v-col>
            <v-col cols="3">
              <router-link to="/customer-wallet">
                <v-btn
                    class="text-none"
                    color="info"
                    variant="flat"
                    width="90"
                    rounded
                >Выписка</v-btn>
              </router-link>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
    <v-card class="mt-3" elevation="6">
      <v-list density="compact">
        <v-list-subheader>Ваши счета:</v-list-subheader>
        <v-list-item
            v-for="account in accounts"
            :key="account.account_number"
            :title="'Cервис: ' + account.company_name"
            class="bg-grey-lighten-3"
        >
          <v-spacer class="mt-3"></v-spacer>
          <v-row>
            <v-col>
              <p>Cчет: {{ account.account_number }}</p>
              <p>Дата регистрации: {{ adapter.date(account.registered_at) }}</p>
            </v-col>
            <v-col cols="4">
              <p>Оплачено: {{ account.balance }} руб.
                <v-btn
                    class="text-none"
                    color="success"
                    variant="flat"
                    width="90"
                    rounded
                >Подробнее</v-btn>
              </p>
            </v-col>
          </v-row>
        </v-list-item>
        <v-divider thickness="2"></v-divider>
      </v-list>
    </v-card>
  </v-container>
</template>

<script>
import { useDate } from "vuetify";
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
    userName: '',
    userUuid: '',
    walletBalance: '',
    accounts: [],
    isRefreshed: false,
    adapter: useDate()
  }),
  methods: {
    ...mapActions('auth', {
      getRefresh: REFRESH_ACTION
    }),
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async getCustomerInfo() {
      try {
        await axiosInstance.get('http://127.0.0.1:7077/billing/info/').then((response) => {
          this.showLoading(false);
          this.userName = response.data.wallet.username;
          this.userUuid = response.data.wallet.customer_uuid;
          this.walletBalance = response.data.wallet.balance;
          this.accounts = response.data.accounts
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
    async runGetCustomerInfo() {
      this.showLoading(true);
      do {
        await this.getCustomerInfo();
      } while (this.isRefreshed)
    }
  },
  mounted() {
    this.runGetCustomerInfo();
  }
}
</script>

<style scoped>
.user-info {
  text-align: center;
}
</style>