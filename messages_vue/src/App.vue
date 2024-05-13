<template>
  <navbar></navbar>
  <div class="app">
    <router-view></router-view>
  </div>
  <my-loader v-if="showLoading"></my-loader>
</template>

<script>
import Navbar from "@/components/Navbar";
import MyLoader from "@/components/UI/MyLoader";
import { AUTO_AUTH_ACTION } from "@/store/storeConstants";
import { mapState } from "vuex";
export default {
  components: {
    Navbar,
    MyLoader
  },
  created() {
    this.$store.dispatch(`auth/${AUTO_AUTH_ACTION}`);
  },
  computed: {
    ...mapState({
      showLoading: state => state.showLoading
    })
  }
}

</script>

<style scoped>

</style>