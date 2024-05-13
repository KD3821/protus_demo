<template>
  <div>
    <h2>Детали рассылки:</h2>
    <Campaign
        v-bind:campaign="campaign"
        campaignDetailedView
    />
  </div>
</template>

<script>
import Campaign from "@/components/Campaign";
import { mapActions, mapMutations } from "vuex";
import axiosInstance from "@/services/AxiosTokenInstance";
import {
  LOADING_SPINNER_SHOW_MUTATION,
  REFRESH_ACTION
} from "@/store/storeConstants";
export default {
  components: { Campaign },
  data() {
    return {
      campaign: {},
      campaignId: '',
      isRefreshed: false,
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
        });
      } catch (e) {
        if (typeof e.response !== "undefined" && e.response.status === 401 && !this.isRefreshed) {
          try {
            await this.getRefresh();
            this.isRefreshed = true;
          } catch (err) {
            this.$router.replace('/login');
          }
        } else {
          this.$router.replace('/error');
        }
      }
    },
    async runFetchCampaign() {
      this.showLoading(true);
      do {
        await this.fetchCampaign();
      } while (this.isRefreshed)
    }
  },
  mounted() {
    this.campaignId = this.$route.params.id
    this.runFetchCampaign();
  },
}
</script>

<style scoped>

</style>