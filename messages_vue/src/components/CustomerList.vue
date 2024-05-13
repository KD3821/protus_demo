<template>
  <div v-if="customers.length > 0">
    <h2>Всего клиентов: {{ count }}</h2>
    <div class="customer-list">
      <Customer
        v-for="customer in customers"
        v-bind:customer="customer"
        v-bind:key="customer.id"
      />
    </div>
  </div>
  <div v-else>
    <h2>Нет данных ...</h2>
  </div>
</template>

<script>
import Customer from "@/components/Customer";
export default {
  components: { Customer },
  props: {
    customers: {
      type: Array,
      required: true
    },
    count: 0
  }
}
</script>

<style scoped>
.customer-list {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>