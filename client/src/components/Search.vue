<template>
  <div clas="search">
    <input
      ref="queryToSearch"
      placeholder="Press enter to search"
      @keyup.enter="submit"
    />
  </div>
</template>
<script>
export default {
  name: 'Search',
  methods: {
    submit() {
      this.$store.commit('setQuery', this.$refs.queryToSearch.value);
      this.$root.$emit('updatingResults');
    },
  },
};
</script>
