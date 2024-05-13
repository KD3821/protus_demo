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
          <v-icon
              icon="mdi-pound-box"
          ></v-icon> {{ userUuid }}<br>
          <v-icon
              icon="mdi-wallet"
          ></v-icon> {{ walletBalance }} руб.
        </v-col>
      </v-row>
    </v-card>
    <v-card class="mt-3" elevation="6">
      <v-list density="compact">
        <v-list-subheader>Операции:</v-list-subheader>
        <v-list-item
            v-if="operations.length"
            v-for="operation in operations"
            :key="operation.reference_code"
            :title="'Код операции: ' + operation.reference_code"
            class="bg-grey-lighten-3 mt-2"
        >
          <v-spacer class="mt-3"></v-spacer>
          <v-row>
            <v-col>
              <p>
                <v-icon
                  icon="mdi-briefcase-account"
                ></v-icon>{{ operation.provider_name }}: "{{ operation.service_name }}"
                | № инвойса: {{ operation.invoice_number }}
              </p>
              <p>Дата операции: {{ adapter.date(operation.date) }}</p>
            </v-col>
            <v-col cols="4">
              <p>Cумма: {{ operation.amount }} руб.</p>
              <p>Остаток: {{ operation.remaining_balance }}</p>
            </v-col>
          </v-row>
        </v-list-item>
        <v-list-item v-else>
          Вы пока не оплачивали услуги.
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
    operations: [],
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
    async getWalletInfo() {
      try {
        await axiosInstance.get('http://127.0.0.1:7077/billing/dashboard/').then((response) => {
          this.showLoading(false);
          this.userName = response.data.wallet.username;
          this.userUuid = response.data.wallet.customer_uuid;
          this.walletBalance = response.data.wallet.balance;
          this.operations = response.data.operations
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
    async runGetWalletInfo() {
      this.showLoading(true);
      do {
        await this.getWalletInfo();
      } while (this.isRefreshed)
    }
  },
  mounted() {
    this.runGetWalletInfo();
  }
}
</script>

<style scoped>
.user-info {
  text-align: center;
}
</style>