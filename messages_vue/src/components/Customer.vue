<template>
  <div v-if="customerInfoView" class="customer message__view ">
    <table>
      <tr>
        <td>ID клиента: {{ customer.id }}</td>
        <td>Телефон: {{ customer.phone }}</td>
        <td>Оператор: {{ customer.carrier }}</td>
        <td>Тэг: {{ customer.tag }}</td>
      </tr>
    </table>
    <my-button
        v-if="customerInfoView && !showDeleted"
        v-on:click="deleteCustomer"
    >
      Удалить
    </my-button>
    <div v-if="failure" class="failure">{{ failure }}</div>
    <div v-show="showDeleted" class="deleted">
      Клиент удален!
    </div>
  </div>
  <div v-else class="customer list__view">
    <div class="detailed__view">
      <div>
        <div>ID: {{ customer.id }}</div>
        <div>Телефон: {{ customer.phone }}</div>
        <div>Оператор: {{ customer.carrier }}</div>
        <div>Тэг: {{ customer.tag }}</div>
        <div>Часовой пояс: {{ customer.tz_name }}</div>
      </div>
      <my-button
          v-on:click="$router.push({ name: 'customerDetails', params: { id: customer.id }})"
      >
        Информация
      </my-button>
      <my-button
          v-on:click="$router.push({ name: 'customerEdit', params: { id: customer.id, action: 'edit' }})"
      >
        Редактировать
      </my-button>

    </div>
  </div>
</template>

<script>
import MessageList from "@/components/MessageList";
import {mapActions, mapMutations} from "vuex";
import axiosInstance from "@/services/AxiosTokenInstance";
import CreateCustomerValidations from "@/services/CreateCustomerValidations";
import {
  REFRESH_ACTION,
  LOADING_SPINNER_SHOW_MUTATION
} from "@/store/storeConstants";
export default {
  components: { MessageList },
  props: {
    customer: {
      type: Object,
      required: true
    },
    customerMessageView: {
      type: Boolean
    },
    customerInfoView: {
      type: Boolean
    }
  },
  data() {
    return {
      customerId: '',
      isRefreshed: false,
      showDeleted: false,
      messages: [],
      count: 0,
      campaignStatus: 'launched',
      showNoMessages: false,
      failure: ''
    }
  },
  methods: {
    ...mapActions('auth', {
      getRefresh: REFRESH_ACTION
    }),
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async deleteCustomer() {
      if (confirm("Удалить клиента?")) {
        try {
          this.showLoading(true);
          await axiosInstance.delete(`http://127.0.0.1:8000/api/customers/${this.customer.id}/`).then((response) => {
            this.showDeleted = response.status === 204;
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
            if (e.response.status === 400) {
              this.failure = CreateCustomerValidations.getErrorMessageDetail(e.response.data);
              return false;
            }
            this.$router.replace('/error');
          }
        }
      }
    },
  },
}
</script>

<style scoped>
.customer {
  border: 3px solid lightseagreen;
  margin: 15px;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: lightcyan;
  color: black;
}
.list__view {
  display: flex;
  align-items: center;
  margin-left: 50px;
}
.message__view {
  display: flex;
  justify-content: center;
}
.deleted {
  color: darkred;
  border: 1px solid black;
}
.detailed__view {
  display: flex;
  align-items: center;
  max-width: 350px;
  margin: auto;
}
</style>