<template>
  <div v-if="singleStatsView">
    Статистика по данной рассылке:
    <my-date v-bind:date="stats.date"/>
    <table class="stats__table">
      <tr>
        <th style="color: blue">Cообщения</th>
        <th style="color: darkgreen">Отправлено</th>
        <th>В процессе</th>
        <th style="color: darkslategray">Отменено</th>
        <th style="color: darkred">Ошибка</th>
      </tr>
      <tr>
        <td>{{ stats.msg_total }}</td>
        <td>{{ stats.msg_ok }}</td>
        <td>{{ stats.msg_processing }}</td>
        <td>{{ stats.msg_canceled }}</td>
        <td>{{ stats.msg_failed }}</td>
      </tr>
    </table>
  </div>
  <div v-else>
    Статистика по всем рассылкам:
    <my-date v-bind:date="stats.date"/>
    <table class="stats__table">
      <tr>
        <th style="color: blue">Сообщения</th>
        <th style="color: darkgreen">Отправлено</th>
        <th>В процессе</th>
        <th style="color: darkslategray">Отменено</th>
        <th style="color: darkred">Ошибка</th>
        <th style="color: blue">Рассылки</th>
      </tr>
      <tr>
        <td>{{ stats.msg_total }}</td>
        <td>{{ stats.msg_ok }}</td>
        <td>{{ stats.msg_processing }}</td>
        <td>{{ stats.msg_canceled }}</td>
        <td>{{ stats.msg_failed }}</td>
        <td>{{ stats.campaign_total }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import { REFRESH_ACTION } from "@/store/storeConstants";
import axiosInstance from "@/services/AxiosTokenInstance";
export default {
  props: {
    singleStatsView: {
      type: Boolean,
      required: true,
    }
  },
  data() {
    return {
      campaignId: '',
      isRefreshed: false,
      stats: {},
      api_route: '',
    }
  },
  watch: {
    singleStatsView: async function(newValue, oldValue) {
      await this.runFetchStats();
    }
  },
  methods: {
    ...mapActions('auth', {
      getRefresh: REFRESH_ACTION
    }),
    async fetchStats() {
      if (this.singleStatsView) {
        this.api_route = `http://127.0.0.1:8000/api/reports/${this.campaignId}/`;
      } else {
        this.api_route = `http://127.0.0.1:8000/api/reports/`;
      }
      try {
        await axiosInstance.get(this.api_route).then((response) => {
          this.stats = response.data;
          this.isRefreshed = false;
        })
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
    async runFetchStats() {
      do {
        await this.fetchStats();
      } while (this.isRefreshed)
    }
  },
  created() {
    this.campaignId = this.$route.params.id
    this.runFetchStats();
  },
}
</script>

<style scoped>
.stats__table > th, tr, td {
  border: 1px groove grey;
  text-align: center;
}
</style>