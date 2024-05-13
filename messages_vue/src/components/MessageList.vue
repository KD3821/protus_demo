<template>
  <div v-if="messages.length > 0">
    <h2>Всего сообщений: {{ count }}</h2>
    <Message
        v-for="message in messages"
        v-bind:message="message"
        v-bind:key="message.id"
        campaignStatus="launched"
        customerDetailedView
    />
  </div>
  <div v-else>
    <h2>Нет сообщений...</h2>
  </div>
</template>

<script>
import Message from "@/components/Message";
export default {
  components: { Message },
  props: {
    messages: {
      type: Object,
      required: true
    },
    count: 0
  }
}
</script>

<style scoped>

</style>