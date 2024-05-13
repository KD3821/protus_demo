<template>
  <v-footer class="bg-grey-lighten-1" app>
    <v-row justify="center" no-gutters>
      <v-btn
          v-for="link in links"
          :key="link"
          class="mx-2"
          color="black"
          rounded="xl"
          variant="text"
      >
        {{ link }}
      </v-btn>
      <v-col class="text-center mt-4" cols="12">
        {{ new Date().getFullYear() }} — <strong>PROTUS service</strong>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  data: () => ({
    links: [
        'О нас',
        'Документация',
        'Статьи'
    ]
  })
}
</script>

<style scoped>

</style>