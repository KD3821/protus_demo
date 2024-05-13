<template>
  <div v-if="editView">
    <h2>Данные клиента c ID:{{ customer.id }}</h2>
    <CustomerForm
        v-bind:customer="customer"
    />
  </div>
  <div v-else>
    <h2>Информация о клиенте:</h2>
    <Customer
        v-bind:customer="customer"
        customerInfoView
    />
    <MessageList
        v-if="messages.length > 0"
        v-bind:messages="messages"
        v-bind:count
    />
  </div>
</template>

<script>
import Customer from "@/components/Customer";
import MessageList from "@/components/MessageList";
import CustomerForm from "@/components/CustomerForm";
import { mapActions, mapMutations } from "vuex";
import axiosInstance from "@/services/AxiosTokenInstance";
import {
  LOADING_SPINNER_SHOW_MUTATION,
  REFRESH_ACTION
} from "@/store/storeConstants";
export default {
  components: {
    Customer,
    CustomerForm,
    MessageList
  },
  data() {
    return {
      customer: {},
      messages: [],
      customerId: '',
      isRefreshed: false,
      editView: false
    }
  },
  methods: {
    ...mapActions('auth', {
      getRefresh: REFRESH_ACTION
    }),
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async fetchCustomer() {
      try {
        await axiosInstance.get(`http://127.0.0.1:8000/api/customers/${this.customerId}/`).then((response) => {
          this.showLoading(false);
          this.customer = response.data;
          this.isRefreshed = false;
        })
      } catch (e) {
        if (typeof e.response !== "undefined" && e.response.status === 401 && !this.isRefreshed) {
          try {
            await this.getRefresh();
            this.isRefreshed = true;
          } catch (err) {
            this.showLoading(false);
            this.$router.replace('/login');
          }
        } else {
          this.showLoading(false);
          this.$router.replace('/error');
        }
      }
    },
    async runFetchCustomer() {
      this.showLoading(true);
      do {
        await this.fetchCustomer();
      } while (this.isRefreshed);
    },
    async fetchCustomerMessages() {
      try {
        await axiosInstance.get(`http://127.0.0.1:8000/api/customers/${this.customerId}/customer-messages/`).then((response) => {
          this.showLoading(false);
          this.messages = response.data.results;
          this.count = response.data.count;
          this.isRefreshed = false;
          this.showNoMessages = this.messages.length <= 0;
        })
      } catch (e) {
        if (typeof e.response !== "undefined" && e.response.status === 401 && !this.isRefreshed) {
          try {
            await this.getRefresh();
            this.isRefreshed = true;
          } catch (err) {
            this.showLoading(false);
            this.$router.replace('/login');
          }
        } else {
          this.showLoading(false);
          this.$router.replace('/error');
        }
      }
    },
    async runFetchCustomerMessages() {
      this.showLoading(true);
      do {
        await this.fetchCustomerMessages()
      } while (this.isRefreshed)
    },
  },
  created() {
    this.customerId = this.$route.params.id;
    this.editView = this.$route.params.action === 'edit';
    this.runFetchCustomer();
    if (this.editView !== 'edit') {
      this.runFetchCustomerMessages();
    }
  }
}
</script>

<style scoped>

</style>