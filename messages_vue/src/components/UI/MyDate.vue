<template>
  <span>
    {{ formattedDate }}
  </span>
</template>

<script>
export default {
  name: 'my-date',
  props: {
    date: {
      type: String
    }
  },
  data() {
    return {
      formattedDate: '',
    }
  },
  methods: {
    formatDate() {
      let formatter = new Intl.DateTimeFormat('ru', {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      });
      let dateToFormat = new Date(this.date);
      this.formattedDate = formatter.format(dateToFormat);
    },
    async getDateProp() {
      let date = this.$props.date;
      if (date !== undefined) {
        this.formatDate();
      } else {
        await this.watchDateProp();
      }
    },
    async watchDateProp() {
      if (this.$props.date === undefined) {
        setTimeout(this.getDateProp, 50)
      } else {
        await this.getDateProp();
      }
    }
  },
  mounted() {
    this.watchDateProp();
  }
}
</script>

<style scoped>

</style>