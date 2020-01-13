<template>
  <div></div>
</template>

<script>
export default {
  name: 'Save',
  data: () => ({
    id: '',
  }),
  beforeMount() {
    this.id = this.$route.params.id
  },
};
</script>
