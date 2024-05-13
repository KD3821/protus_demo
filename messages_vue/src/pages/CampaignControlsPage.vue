<template>
  <div>
    <h2>Управление рассылкой c ID: {{ campaign.id }} ( {{ campaignStatuses[campaign.status] }} )</h2>
    <CampaignForm
        v-bind:campaign="campaign"
    />
  </div>
</template>

<script>
import CampaignForm from "@/components/CampaignForm";
import axiosInstance from "@/services/AxiosTokenInstance";
import MyButton from "@/components/UI/MyButton";
import CreateCampaignValidations from "@/services/CreateCampaignValidations";
import { mapActions, mapMutations } from "vuex";
import {
  LOADING_SPINNER_SHOW_MUTATION,
  REFRESH_ACTION
} from "@/store/storeConstants";
export default {
  components: {MyButton, CampaignForm },
  data() {
    return {
      campaign: {},
      campaignId: '',
      campaignStatuses: {
        scheduled: 'Запланирована',
        launched: 'В процессе',
        canceled: 'Отменена',
        finished: 'Завершена'
      }
    }
  },
  methods: {
    ...mapActions('auth', {
      getRefresh: REFRESH_ACTION
    }),
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async fetchCampaign() {
      try {
        await axiosInstance.get(`http://127.0.0.1:8000/api/campaigns/${this.campaignId}/`).then((response) => {
          this.showLoading(false);
          this.campaign = response.data;
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
        } else if (e.response.status === 400 || e.response.status === 404) {
          this.failure = CreateCampaignValidations.getErrorMessageDetail(e.response.data);
          this.showLoading(false);
          return false;
        } else {
          this.showLoading(false);
          this.$router.replace('/error');
        }
      }
    },
    async runFetchCampaign() {
      this.showLoading(true);
      do {
        await this.fetchCampaign();
      } while (this.isRefreshed);
    }
  },
  created() {
    this.campaignId = this.$route.params.id;
    this.runFetchCampaign();
  }
}
</script>

<style scoped>

</style>