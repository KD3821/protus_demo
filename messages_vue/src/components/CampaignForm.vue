<template>
  <div>
    <form v-on:submit.prevent class="add-item-form">
      <p>Время запуска:</p>
      <my-input
          v-bind:value="startTime"
          v-on:input="startTime = $event.target.value"
          type="time"
          v-bind:disabled="!campaignScheduled"
      ></my-input>
      <my-input
          v-bind:value="startDate"
          v-on:input="startDate = $event.target.value"
          type="date"
          v-bind:disabled="!campaignScheduled"
      ></my-input>
      <p>Время остановки:</p>
      <my-input
          v-bind:value="finishTime"
          v-on:input="finishTime = $event.target.value"
          type="time"
          v-bind:disabled="!campaignScheduled"
      ></my-input>
      <my-input
          v-bind:value="finishDate"
          v-on:input="finishDate = $event.target.value"
          type="date"
          v-bind:disabled="!campaignScheduled"
      ></my-input>
      <p>Фильтр:</p>
      <my-select
          v-bind:value="selectedCarrier"
          v-on:input="selectedCarrier = $event.target.value"
          v-bind:options="carrierOptions"
          v-bind:disabled="!campaignScheduled"
      />
      <my-input
          v-bind:value="tag"
          v-on:input="tag = $event.target.value"
          type="text"
          placeholder="Тэг"
          v-bind:disabled="!campaignScheduled"
      ></my-input>
      <my-input
          v-bind:value="text"
          v-on:input="text = $event.target.value"
          type="text"
          placeholder="Текст рассылки"
          v-bind:disabled="!campaignScheduled"
      ></my-input>
      <div v-if="campaignScheduled" class="result">
        <my-button
            v-on:click="runUpdateCampaign"
        >
          Сохранить изменения
        </my-button>
        <my-button
            v-on:click="runLaunchCampaign"
        >
          Оплатить и запустить рассылку
        </my-button>
        <my-button
            v-on:click="runDeleteCampaign"
        >
          Удалить рассылку
        </my-button>
        <div v-if="success" class="success">{{ success }}</div>
        <div v-else class="failure">{{ failure }}</div>
      </div>
      <div v-else>
        <div v-show="showDeleted" class="deleted">
          Рассылка удалена!
        </div>
        <div v-show="showCanceled" class="deleted">
          {{ deleteMessage }}
        </div>
        <my-button
            v-show="showCancelBttn"
            v-on:click="runCancelCampaign"
        >
          Отменить рассылку
        </my-button>
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions, mapMutations } from "vuex";
import axiosInstance from "@/services/AxiosTokenInstance";
import CreateCampaignValidations from "@/services/CreateCampaignValidations";
import {
  LOADING_SPINNER_SHOW_MUTATION,
  REFRESH_ACTION,
} from "@/store/storeConstants";
import MyButton from "@/components/UI/MyButton";
export default {
  components: { MyButton },
  props: {
    campaign: {
      type: Object,
      required: true
    }
  },
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
      oldStartTime: '',
      oldStartDate: '',
      oldFinishTime: '',
      oldFinishDate: '',
      oldSelectedCarrier: '',
      oldTag: null,
      oldText: '',
      campaignScheduled: true,
      showDeleted: false,
      showCancelBttn: false,
      showCanceled: false,
      deleteMessage: '',
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
    async launchCampaign() {
      this.success = this.failure = '';
      if (confirm("Подтвердите оплату услуги по рассылке сообщений. Стоимость: 10.00 руб.")) {
        this.showLoading(true);
        try {
          await axiosInstance.post(`http://127.0.0.1:8000/api/campaigns/${this.$props.campaign.id}/launch/`).then((response) => {
            this.showLoading(false);
            this.isRefreshed = false;
            this.$router.replace(`/campaigns/${this.$props.campaign.id}`)
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
          } else if (e.response.status === 400) {
            this.failure = CreateCampaignValidations.getErrorMessageDetail(e.response.data);
            this.showLoading(false);
            return false;
          } else if (e.response.status === 426) {
            this.showLoading(false);
            this.$router.replace('/forbidden');
          } else {
            this.showLoading(false);
            this.$router.replace('/error');
          }
        }
      }
    },
    async runLaunchCampaign() {
      do {
        await this.launchCampaign();
      } while (this.isRefreshed);
    },
    async cancelCampaign() {
      this.success = this.failure = '';
      if (confirm("Отменить рассылку?")) {
        try {
          this.showLoading(true);
          await axiosInstance.post(`http://127.0.0.1:8000/api/campaigns/${this.$props.campaign.id}/cancel/`).then((response) => {
            this.showLoading(false);
            this.campaignScheduled = false;
            this.showCancelBttn = false;
            this.showCanceled = response.status === 200;
            this.deleteMessage = response.data.cancel_data;
            this.isRefreshed = false;
          });
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
            if (e.response.status === 400) {
              this.failure = CreateCampaignValidations.getErrorMessageDetail(e.response.data);
              this.showLoading(false);
              return false;
            }
            this.showLoading(false);
            this.$router.replace('/error');
          }
        }
      }
    },
    async runCancelCampaign() {
      do {
        await this.cancelCampaign();
      } while (this.isRefreshed);
    },
    async deleteCampaign() {
      this.success = this.failure = '';
      if (confirm("Удалить рассылку?")) {
        try {
          this.showLoading(true);
          await axiosInstance.delete(`http://127.0.0.1:8000/api/campaigns/${this.$props.campaign.id}/`).then((response) => {
            this.showLoading(false);
            this.campaignScheduled = false;
            this.showDeleted = response.status === 204;
            this.isRefreshed = false;
          });
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
            if (e.response.status === 400) {
              this.failure = CreateCampaignValidations.getErrorMessageDetail(e.response.data);
              this.showLoading(false);
              return false;
            }
            this.showLoading(false);
            this.$router.replace('/error');
          }
        }
      }
    },
    async runDeleteCampaign() {
      do {
        await this.deleteCampaign();
      } while (this.isRefreshed);
    },
    async updateCampaign() {
      this.success = this.failure = '';
      this.showLoading(true);
      let campaignData = {
        start_at: `${this.startDate}T${this.startTime}:00+03:00`,
        finish_at: `${this.finishDate}T${this.finishTime}:00+03:00`,
        text: this.text,
        params: {
          'tag': this.tag === '' ? null : this.tag,
          'carrier': this.selectedCarrier,
        }
      };
      if (this.startTime === this.oldStartTime &&
          this.startDate === this.oldStartDate &&
          this.finishTime === this.oldFinishTime &&
          this.finishDate === this.oldFinishDate &&
          this.text === this.oldText &&
          this.selectedCarrier === this.oldSelectedCarrier &&
          (this.tag === this.oldTag || (this.tag === '' && this.oldTag === null))
      ) {
        this.errors = {old: 'Данные не были изменены.'}
        this.failure = CreateCampaignValidations.getErrorMessageDetail(this.errors);
        this.showLoading(false);
        return false;
      }
      let validations = new CreateCampaignValidations(
          campaignData.start_at,
          campaignData.finish_at,
          campaignData.text,
          campaignData.params.carrier
      );
      this.errors = validations.checkCreateCampaignValidations()
      if ('start' in this.errors || 'finish' in this.errors || 'text' in this.errors || 'carrier' in this.errors) {
        this.failure = CreateCampaignValidations.getErrorMessageDetail(this.errors);
        this.showLoading(false);
        return false;
      }
      try {
        await axiosInstance.patch(`http://127.0.0.1:8000/api/campaigns/${this.$props.campaign.id}/`, campaignData).then((response) => {
          this.showLoading(false);
          if (response.status === 200) {
            this.success = 'Данные успешно сохранены.';
            this.oldStartTime = this.startTime;
            this.oldStartDate = this.startDate;
            this.oldFinishTime = this.finishTime;
            this.oldFinishDate = this.finishDate;
            this.oldText = this.text;
            this.oldTag = this.tag;
            this.oldSelectedCarrier = this.selectedCarrier;
            this.$router.replace(`/campaigns/${this.$props.campaign.id}/controls`);
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
        } else if (e.response.status === 400 || e.response.status === 404) {
          this.failure = CreateCampaignValidations.getErrorMessageDetail(e.response.data);
          this.showLoading(false);
          return false;
        } else {
          this.$router.replace('/error');
          this.showLoading(false);
        }
      }
    },
    async runUpdateCampaign() {
      do {
        await this.updateCampaign();
      } while (this.isRefreshed);
    },
    async getCampaignProp() {
      let campaign = this.$props.campaign;
      if (campaign.start_at !== undefined) {
        let tmpStart = campaign.start_at.split('T');
        let tmpStartTime = tmpStart[1].split('+');
        this.startDate = this.oldStartDate = tmpStart[0];
        this.startTime = this.oldStartTime = tmpStartTime[0].substring(0, 5);
        let tmpFinish = campaign.finish_at.split('T');
        let tmpFinishTime = tmpFinish[1].split('+');
        this.finishDate = this.oldFinishDate = tmpFinish[0];
        this.finishTime = this.oldFinishTime = tmpFinishTime[0].substring(0, 5);
        this.text = this.oldText = campaign.text;
        this.selectedCarrier = this.oldSelectedCarrier = campaign.params.carrier;
        this.tag = this.oldTag = campaign.params.tag;
        this.campaignScheduled = campaign.status === 'scheduled' && campaign.confirmed_at === null;
        this.showCancelBttn = (
            (campaign.status === 'scheduled' && campaign.confirmed_at !== null) || campaign.status === 'launched'
        );
      } else {
        await this.watchCampaignProp();
      }
    },
    async watchCampaignProp() {
      if (this.$props.campaign.start_at === undefined) {
        if (this.startTime !== 'загружаем...') {
          this.startTime = 'загружаем...'
          this.startDate = 'загружаем...';
          this.finishTime = 'загружаем...';
          this.finishDate = 'загружаем...';
          this.selectedCarrier = 'загружаем...';
          this.tag = 'загружаем...';
        }
        setTimeout(this.getCampaignProp, 50)
      } else {
        await this.getCustomerProp();
      }
    }
  },
  mounted() {
    this.watchCampaignProp();
  }
}
</script>

<style scoped>
.result {
  text-align: center;
}
.deleted {
  color: darkred;
  border: 1px solid black;
  max-width: 200px;
  margin: auto;
}
</style>