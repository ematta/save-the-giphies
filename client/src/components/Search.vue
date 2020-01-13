<template>
  <div clas="search">
    <input
      placeholder="Enter Text Here"
      v-model="searchRequest"
      @keyup.enter="submit"
    />
    <!-- <button variant="info">Search</button> -->
  </div>
</template>
<script>
export default {
  name: 'Search',
  data() {
    return {
      searchRequest: '',
    };
  },
  methods: {
    submit() {
      this.$emit('inputData', this.searchRequest);
      this.searchRequest = '';
    },
  },
};
</script>
