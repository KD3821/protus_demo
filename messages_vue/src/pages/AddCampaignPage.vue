<template>
  <div>
    <form v-on:submit.prevent class="add-item-form">
      <p>Время запуска:</p>
      <my-input
        v-bind:value="startTime"
        v-on:input="startTime = $event.target.value"
        type="time"
      ></my-input>
      <my-input
        v-bind:value="startDate"
        v-on:input="startDate = $event.target.value"
        type="date"
      ></my-input>
      <p>Время остановки:</p>
      <my-input
          v-bind:value="finishTime"
          v-on:input="finishTime = $event.target.value"
          type="time"
      ></my-input>
      <my-input
          v-bind:value="finishDate"
          v-on:input="finishDate = $event.target.value"
          type="date"
      ></my-input>
      <p>Фильтр:</p>
      <my-select
          v-bind:value="selectedCarrier"
          v-on:input="selectedCarrier = $event.target.value"
          v-bind:options="carrierOptions"
      />
      <my-input
          v-bind:value="tag"
          v-on:input="tag = $event.target.value"
          type="text"
          placeholder="Тэг"
      ></my-input>
      <my-input
          v-bind:value="text"
          v-on:input="text = $event.target.value"
          type="text"
          placeholder="Текст рассылки"
      ></my-input>
      <my-button
        v-on:click="runCreateCampaign"
      >
        Создать рассылку
      </my-button>
      <div v-if="success" class="success">{{ success }}</div>
      <div v-else class="failure">{{ failure }}</div>
    </form>
  </div>
</template>

<script>
import axiosInstance from "@/services/AxiosTokenInstance";
import {mapActions, mapMutations} from "vuex";
import CreateCampaignValidations from "@/services/CreateCampaignValidations";
import {
  LOADING_SPINNER_SHOW_MUTATION,
  REFRESH_ACTION
} from "@/store/storeConstants";
export default {
  data() {
    return {
      isRefreshed: false,
      startTime: '',
      startDate: '',
      finishTime: '',
      finishDate: '',
      selectedCarrier: '',
      tag: null,
      text: '',
      success: '',
      failure: '',
      errors: {},
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
    async createCampaign() {
      let campaignData = {
        start_at: `${this.startDate}T${this.startTime}:00+03:00`,
        finish_at: `${this.finishDate}T${this.finishTime}:00+03:00`,
        text: this.text,
        params: {
          'tag': this.tag === '' ? null : this.tag,
          'carrier': this.selectedCarrier,
        }
      };
      let validations = new CreateCampaignValidations(
          campaignData.start_at,
          campaignData.finish_at,
          campaignData.text,
          campaignData.params.carrier
      );
      this.errors = validations.checkCreateCampaignValidations()
      if ('start' in this.errors || 'finish' in this.errors || 'text' in this.errors || 'carrier' in this.errors) {
        this.failure = CreateCampaignValidations.getErrorMessageDetail(this.errors);
        return false;
      }
      try {
        await axiosInstance.post('http://127.0.0.1:8000/api/campaigns/', campaignData).then((response) => {
          if (response.status === 201) {
            this.isRefreshed = false;
            this.$router.replace('/campaigns');
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
          this.failure = CreateCampaignValidations.getErrorMessageDetail(e.response.data);
          return false;
        } else {
          this.$router.replace('/error');
        }
      }
    },
    async runCreateCampaign() {
      do {
        await this.createCampaign();
      } while (this.isRefreshed)
    }
  }
}
</script>

<style>
.add-item-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 50px;
}
.success {
  color: green;
  font-size: 10pt;
}
.failure {
  color: red;
  font-size: 10pt;
}
</style>