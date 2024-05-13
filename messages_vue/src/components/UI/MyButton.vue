<template>
  <button class="btn">
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: "my-button"
}
</script>

<style scoped>
.btn {
  background: lightgray;
  border: 1px solid darkslategrey;
  color: darkred;
  margin: 10px;
  cursor: pointer;
}
.btn:active {
  background: darkgrey;
}
</style>
