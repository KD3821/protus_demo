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
          v-on:click="runUpdateCustomer"
      >
        Сохранить изменения
      </my-button>
      <div v-if="success" class="success">{{ success }}</div>
      <div v-else class="failure">{{ failure }}</div>
    </form>
  </div>
</template>

<script>
import {mapActions, mapMutations} from "vuex";
import CreateCustomerValidations from "@/services/CreateCustomerValidations";
import axiosInstance from "@/services/AxiosTokenInstance";
import {
  LOADING_SPINNER_SHOW_MUTATION,
  REFRESH_ACTION
} from "@/store/storeConstants";
export default {
  props: {
    customer: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      isRefreshed: false,
      phone: '',
      selectedCarrier: {},
      tag: '',
      timeZone: '',
      oldPhone: '',
      oldSelectedCarrier: {},
      oldTag: '',
      oldTimeZone: '',
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
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async updateCustomer() {
      this.success = this.failure = '';
      this.showLoading(true);
      let customerData = {
        phone: this.phone,
        carrier: this.selectedCarrier,
        tag: this.tag,
        tz_name: this.timeZone
      };
      if (this.oldPhone === customerData.phone &&
          this.oldSelectedCarrier === customerData.carrier &&
          this.oldTag === customerData.tag &&
          this.oldTimeZone === customerData.tz_name
      ) {
        this.errors = {old: 'Данные не были изменены.'}
        this.failure = CreateCustomerValidations.getErrorMessageDetail(this.errors);
        this.showLoading(false);
        return false;
      }
      let validations = new CreateCustomerValidations(
          customerData.phone,
          customerData.carrier,
          customerData.tag,
          customerData.tz_name
      );
      this.errors = validations.checkCreateCustomerValidations()
      if ('phone' in this.errors || 'timezone' in this.errors || 'carrier' in this.errors) {
        this.failure = CreateCustomerValidations.getErrorMessageDetail(this.errors);
        this.showLoading(false);
        return false;
      }
      try {
        await axiosInstance.patch(`http://127.0.0.1:8000/api/customers/${this.$props.customer.id}/`, customerData).then((response) => {
          this.showLoading(false);
          if (response.status === 200) {
            this.success = 'Изменения успешно сохранены!';
            this.oldPhone = customerData.phone;
            this.oldSelectedCarrier = customerData.carrier;
            this.oldTag = customerData.tag;
            this.oldTimeZone = customerData.tz_name;
            this.$router.replace(`/customers/${this.$props.customer.id}`);
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
            this.showLoading(false);
          }
        } else if (e.response.status === 400) {
          this.failure = CreateCustomerValidations.getErrorMessageDetail(e.response.data);
          this.showLoading(false);
          return false;
        } else {
          this.$router.replace('/error');
          this.showLoading(false);
        }
      }
    },
    async runUpdateCustomer() {
      do {
        await this.updateCustomer();
      } while (this.isRefreshed);
    },
    async getCustomerProp() {
      let customer = this.$props.customer;
      if (customer.phone !== undefined) {
        this.phone = this.oldPhone = customer.phone;
        this.selectedCarrier = this.oldSelectedCarrier = customer.carrier;
        this.tag = this.oldTag = customer.tag;
        this.timeZone = this.oldTimeZone = customer.tz_name;
      } else {
        await this.watchCustomerProp();
      }
    },
    async watchCustomerProp() {
      if (this.$props.customer.phone === undefined) {
        if (this.phone !== 'загружаем...') {
          this.phone = 'загружаем...';
          this.tag = 'загружаем...';
          this.timeZone = 'загружаем...';
        }
        setTimeout(this.getCustomerProp, 50)
      } else {
        await this.getCustomerProp();
      }
    }
  },
  mounted() {
    this.watchCustomerProp();
  }
}
</script>

<style scoped>

</style>