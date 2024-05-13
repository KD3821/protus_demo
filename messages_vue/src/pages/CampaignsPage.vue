<template>
  <div>
    <div class="top__bttns">
      <h2>Рассылки</h2>
      <my-button v-on:click="$router.push('/campaigns/add')">
        Создать рассылку
      </my-button>
    </div>
    <div class="dock__bttns">
      <my-select
          v-bind:value="selectedSort"
          v-on:input="selectedSort = $event.target.value"
          v-bind:options="sortOptions"
      ></my-select>
      <my-input
          v-bind:value="searchQuery"
          v-on:input="searchQuery = $event.target.value"
          placeholder="Найти рассылку ..."
      ></my-input>
    </div>
    <campaign-list
        v-bind:count
        v-bind:campaigns="sortedAndSearchedCampaigns"
        v-bind:showNoCampaigns="showNoCampaigns"
    />
  </div>
</template>

<script>
import axiosInstance from "@/services/AxiosTokenInstance";
import CampaignList from "@/components/CampaignList";
import { mapActions, mapMutations } from "vuex";
import {
  REFRESH_ACTION,
  LOADING_SPINNER_SHOW_MUTATION,
} from "@/store/storeConstants";
export default {
  components: { CampaignList },
  data() {
    return {
      campaigns: [],
      count: 0,
      searchQuery: '',
      isRefreshed: false,
      selectedSort: '',
      showNoCampaigns: false,
      sortOptions: [
        {value: 'text', name: 'По тексту сообщения'},
        {value: 'params', name: 'По мобильному оператору'},
        {value: 'status', name: 'По статусу'}
      ],
      statuses: [
        ['Запланирована', 'scheduled'],
        ['В процессе', 'launched'],
        ['Отменена', 'canceled'],
        ['Завершена', 'finished']
      ]
    }
  },
  methods: {
    ...mapActions('auth', {
      getRefresh: REFRESH_ACTION
    }),
    ...mapMutations({
      showLoading: LOADING_SPINNER_SHOW_MUTATION
    }),
    async fetchCampaigns() {
      try {
        await axiosInstance.get('http://127.0.0.1:8000/api/campaigns/').then((response) => {
          this.showLoading(false);
          this.campaigns = response.data.results;
          this.count = response.data.count;
          this.isRefreshed = false;
          this.showNoCampaigns = this.campaigns.length <= 0; // same this.campaigns.length > 0 ? false : true
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
        } else {
          this.$router.replace('/error');
          this.showLoading(false);
        }
      }
    },
    async runFetchCampaigns() {
      this.showLoading(true);
      do {
        await this.fetchCampaigns();
      } while (this.isRefreshed)
    }
  },
  mounted() {
    this.runFetchCampaigns();
},
  computed: {
    sortedCampaigns() {
      return [...this.campaigns].sort((campaign1, campaign2) => {
        if (this.selectedSort === 'params') {
          return campaign1[this.selectedSort].carrier?.localeCompare(campaign2[this.selectedSort].carrier)
        } else {
          return campaign1[this.selectedSort]?.localeCompare(campaign2[this.selectedSort])
        }
      });
    },
    sortedAndSearchedCampaigns() {
      return this.sortedCampaigns.filter(campaign => {
        switch (this.selectedSort) {
          case 'params':
            return campaign[this.selectedSort].carrier.toLowerCase().includes(this.searchQuery.toLowerCase());
          case 'status':
            let filteredStatusesArr = this.statuses.filter( (status) => {
              return status[0].toLowerCase().includes(this.searchQuery.toLowerCase())
            });
            let filteredStatuses = [];
            for (let el of filteredStatusesArr) {
              filteredStatuses.push(el[1]);
            }
            return filteredStatuses.indexOf(campaign[this.selectedSort]) >= 0;
          default:
            return campaign['text'].toLowerCase().includes(this.searchQuery.toLowerCase());
        }
      });
    }
  }
}
</script>

<style>
.top__bttns {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.dock__bttns {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>