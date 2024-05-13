<template>
  <div>
    <div class="top__bttns">
      <h2>Клиенты</h2>
      <my-button v-on:click="this.$router.push('/customers/add')">
        Добавить клиента
      </my-button>
    </div>
    <div class="dock__bttns">
      <my-input
        v-bind:value="searchQuery"
        v-on:input="searchQuery = $event.target.value"
        placeholder="Найти клиента по номеру телефона..."
      ></my-input>
    </div>
    <customer-list
        v-bind:count
        v-bind:customers="searchedCustomers"
    />
  </div>
</template>

<script>
import CustomerList from "@/components/CustomerList";
import {
  mapActions,
  mapMutations,
  mapGetters,
} from "vuex";
import axiosInstance from "@/services/AxiosTokenInstance";
import {
  OAUTH_LOGIN_USER_ACTION,
  IS_USER_AUTHENTICATED_GETTER,
  LOADING_SPINNER_SHOW_MUTATION,
  REFRESH_ACTION
} from "@/store/storeConstants";
export default {
  components: { CustomerList },
  data() {
    return {
      customers:[],
      count: 0,
      searchQuery: '',
      isRefreshed: false,
      cid: ''
    }
  },
  methods: {
    ...mapActions('auth', {
      oauthLogin: OAUTH_LOGIN_USER_ACTION,
      getRefresh: REFRESH_ACTION
    }),
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async fetchCustomers() {
      try {
        await axiosInstance.get('http://127.0.0.1:8000/api/customers/').then((response) => {
          this.showLoading(false);
          this.customers = response.data.results;
          this.count = response.data.count;
          this.isRefreshed = false;
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
    async runFetchCustomers() {
      this.showLoading(true);
      do {
        await this.fetchCustomers();
      } while (this.isRefreshed);
    },
    async checkOAuth() {
      await this.checkOAuthRunFetch();
    },
    async checkOAuthRunFetch() {
      if (!this.isOAuthenticated) {
        setTimeout(this.checkOAuth, 50);
      } else {
        await this.runFetchCustomers();
      }
    }
  },
  mounted() {
    if (!!this.cid) {
      this.checkOAuthRunFetch();
    } else {
      this.runFetchCustomers();
    }
  },
  created() {
    this.cid = this.$route.query.cid;
    if (!!this.cid) {
      this.oauthLogin(this.cid);
    }
  },
  computed: {
    ...mapGetters('auth', {
      isOAuthenticated: IS_USER_AUTHENTICATED_GETTER
    }),
    searchedCustomers() {
      return this.customers.filter((customer) => {
        return customer.phone.includes(this.searchQuery)
      });
    }
  }
}
</script>

<style scoped>

</style>