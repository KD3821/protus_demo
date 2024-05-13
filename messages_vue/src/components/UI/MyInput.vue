<template>
  <input
      v-bind:value="modelValue"
      v-on:input="updateInput"
      type="text"
      class="my-input"
  >
</template>

<script>
export default {
  name: 'my-input',
  props: {
    modelValue: [String, Number]
  },
  methods: {
    updateInput(event) {
      this.$emit('update:modelValue', event.target.value)
    }
  }
}
</script>

<style>
.my-input {
  width: 40%;
  border: 2px solid darkseagreen;
  margin-bottom: 5px;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}
</style>