<template>
  <div v-if="campaign && campaign.id" class="campaign">
    <div>
      <div>ID: {{ campaign.id }}</div>
      <div>
        Начало:
        <my-date v-bind:date="campaign.start_at"/>
      </div>
      <div>
        Завершение:
        <my-date v-bind:date="campaign.finish_at"/>
      </div>
      <div>Текст: {{ campaign.text }}</div>
      <div>Фильтр: {{ campaign.params.tag }} {{ campaign.params.carrier }}</div>
      <div>Статус: {{ campaignStatuses[campaign.status] }}</div>
    </div>
    <div v-if="campaignDetailedView" class="detailed__view">
      <div class="stats__bttns">
        <my-button
            v-on:click="fetchSingleStats"
        >
          Статистика рассылки
        </my-button>
        <my-button
            v-on:click="fetchAllStats"
        >
          Статистика всех рассылок
        </my-button>
      </div>
      <div class="stats">
        <Stats v-bind:singleStatsView="showSingleStats" />
      </div>
    </div>
    <div v-else class="campaign__view">
      <my-button
          v-on:click="$router.push({ name: 'campaignDetails', params: { id: campaign.id }})"
      >
        Информация
      </my-button>
      <my-button
          v-on:click="$router.push({ name: 'campaignControls', params: { id: campaign.id }})"
      >
        Управление
      </my-button>
    </div>
  </div>
  <div v-if="messages.length > 0">
    <h2>Всего сообщений: {{ count }}</h2>
    <Message
      v-for="message in messages"
      v-bind:message="message"
      v-bind:key="message.id"
      v-bind:campaignStatus="campaign.status"
    />
  </div>
  <div v-show="showNoMessages">
    <h2>Нет сообщений ...</h2>
  </div>
</template>

<script>
import Message from "@/components/Message";
import Stats from "@/components/Stats";
import { mapActions, mapMutations } from "vuex";
import axiosInstance from "@/services/AxiosTokenInstance";
import {
  LOADING_SPINNER_SHOW_MUTATION,
  REFRESH_ACTION
} from "@/store/storeConstants";
export default {
  components: {
    Stats,
    Message
  },
  props: {
    campaign: {
      type: Object,
      required: true
    },
    campaignDetailedView: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      messages: [],
      count: 0,
      campaignId: '',
      isRefreshed: false,
      showNoMessages: false,
      showSingleStats: true,
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
    async fetchCampaignMessages() {
      try {
        await axiosInstance.get(`http://127.0.0.1:8000/api/campaigns/${this.campaignId}/campaign-messages/`).then((response) => {
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
    async runFetchCampaignMessages() {
      this.showLoading(true);
      do {
        await this.fetchCampaignMessages()
      } while (this.isRefreshed)
    },
    fetchSingleStats() {
      this.showSingleStats = true;
    },
    fetchAllStats() {
      this.showSingleStats = false;
    }
  },
  mounted() {
    if (this.campaignDetailedView) {
      this.campaignId = this.$route.params.id;
      this.runFetchCampaignMessages();
    }
  }
}
</script>

<style scoped>
.campaign {
  border: 3px solid dodgerblue;
  margin: 15px;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: seashell;
}
.campaign__view {
  display: flex;
  flex-direction: column;
  margin-left: 50px;
}
.detailed__view {
  display: flex;
  flex-direction: column;
}
.stats__bttns {
  display: flex;
  justify-content: space-evenly;
  padding: 10px;
  background-color: paleturquoise;
  border: 1px solid grey;
}
.stats {
  text-align: center;
  border: 1px solid grey;
  border-top: none;
  background-color: ghostwhite;
  width: 485px;
}
.stats__bttns > button:focus {
  outline: 2px groove darkred;
  outline-offset: 1px;
}
</style>