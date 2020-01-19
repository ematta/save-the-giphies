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
import { EventBus } from '@/utility';

export default {
  name: 'Search',
  methods: {
    async submit() {
      await this.$store.commit('setQuery', this.$refs.queryToSearch.value);
      await EventBus.$emit('updatingResults');
    },
  },
};
</script>
