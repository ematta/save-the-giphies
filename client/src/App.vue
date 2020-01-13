<template>
  <div id="app">
    <Search @inputData="updateSearch" />
    <Results :msg="child" />
  </div>
</template>

<script>
import Search from './components/Search.vue';
import Results from './components/Results.vue';

export default {
  name: 'App',
  components: {
    Search,
    Results,
  },
  data: () => ({
    child: '',
  }),
  methods: {
    updateSearch(req) {
      this.child = req;
    },
  },
};
</script>

<style>
#app {
  margin-top: 60px
}
</style>
