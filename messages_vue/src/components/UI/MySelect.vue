<template>
  <select
      v-bind:value="modelValue"
      v-on:input="modelValue = $event.target.value"
      v-on:change="changeOption"
      class="my-input"
  >
    <option disabled value="">Выберите из списка</option>
    <option
        v-for="option in options"
        v-bind:value="option.value"
        v-bind:key="option.value"
    >
      {{ option.name }}
    </option>
  </select>
</template>

<script>
export default {
  name: 'my-select',
  props: {
    modelValue: {
      type: String,
    },
    options: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    changeOption(event) {
      this.$emit('update:modelValue', event.target.value)
    }
  }
}
</script>

<style scoped>

</style>