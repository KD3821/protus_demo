<template>
  <v-app>
    <Navbar />
    <router-view />
    <my-loader v-if="showLoading"></my-loader>
    <Footer />
  </v-app>
</template>

<script>
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import MyLoader from "@/components/MyLoader";
import { AUTO_AUTH_ACTION } from "@/store/storeConstants";
import { mapState } from "vuex";
export default {
  name: 'App',
  components: {
    Footer,
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

<style>

</style>
