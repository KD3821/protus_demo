<template>
  <div>
    <form v-on:submit.prevent class="add-item-form">
      <p>Номер телефона и мобильный оператор:</p>
      <my-input
          v-bind:value="phone"
          v-on:input="phone = $event.target.value"
          type="text"
      ></my-input>
      <my-select
          v-bind:value="selectedCarrier"
          v-on:input="selectedCarrier = $event.target.value"
          v-bind:options="carrierOptions"
      />
      <p>Тэг (опционально):</p>
      <my-input
          v-bind:value="tag"
          v-on:input="tag = $event.target.value"
          type="text"
      ></my-input>
      <p>Часовой пояс:</p>
      <my-input
          v-bind:value="timeZone"
          v-on:input="timeZone = $event.target.value"
          type="text"
      ></my-input>
      <my-button
          v-on:click="runCreateCustomer"
      >
        Создать клиента
      </my-button>
      <div v-if="success" class="success">{{ success }}</div>
      <div v-else class="failure">{{ failure }}</div>
    </form>
  </div>
</template>

<script>
import axiosInstance from "@/services/AxiosTokenInstance";
import { REFRESH_ACTION } from "@/store/storeConstants";
import { mapActions } from "vuex";
import CreateCustomerValidations from "@/services/CreateCustomerValidations";
import CreateCampaignValidations from "@/services/CreateCampaignValidations";
export default {
  data() {
    return {
      isRefreshed: false,
      phone: '',
      selectedCarrier: '',
      tag: '',
      timeZone: '',
      errors: {},
      success: '',
      failure: '',
      carrierOptions: [
        {value: 'mts', name: 'МТС'},
        {value: 'megafon', name: 'Мегафон'},
        {value: 'beeline', name: 'Билайн'},
        {value: 'tele2', name: 'Теле2'},
        {value: 'yota', name: 'Йота'}
      ],
    }
  },
  methods: {
    ...mapActions('auth', {
      getRefresh: REFRESH_ACTION
    }),
    async createCustomer() {
      let customerData = {
        phone: this.phone,
        carrier: this.selectedCarrier,
        tag: this.tag,
        tz_name: this.timeZone
      };
      let validations = new CreateCustomerValidations(
          customerData.phone,
          customerData.carrier,
          customerData.tag,
          customerData.tz_name
      );
      this.errors = validations.checkCreateCustomerValidations()
      if ('phone' in this.errors || 'timezone' in this.errors || 'carrier' in this.errors) {
        this.failure = CreateCampaignValidations.getErrorMessageDetail(this.errors);
        return false;
      }
      if (confirm("Подтвердите оплату услуги по добавлению клиента. Стоимость: 2.00 руб.")) {
        try {
          await axiosInstance.post('http://127.0.0.1:8000/api/customers/', customerData).then((response) => {
            if (response.status === 201) {
              this.isRefreshed = false;
              this.$router.replace('/customers');
            } else {
              this.failure = 'ОШИБКА. Проверьте правильность заполнения формы.'
            }
          });
        } catch (e) {
          if (typeof e.response !== "undefined" && e.response.status === 401 && !this.isRefreshed) {
            try {
              await this.getRefresh();
              this.isRefreshed = true;
            } catch (err) {
              this.$router.replace('/login');
            }
          } else if (e.response.status === 400) {
            this.failure = CreateCustomerValidations.getErrorMessageDetail(e.response.data);
            return false;
          } else if (e.response.status === 426) {
            this.$router.replace('/forbidden');
          } else {
            this.$router.replace('/error');
          }
        }
      }
    },
    async runCreateCustomer() {
      do {
        await this.createCustomer();
      } while (this.isRefreshed);
    }
  }
}
</script>

<style scoped>

</style>