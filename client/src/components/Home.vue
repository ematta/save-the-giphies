<template>
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Save the Giphies</h2>
        </div>
      </div>
    </section>
    <section class="search">
      <Search @inputData="updateSearch" />
    </section>
    <section class="results">
      <Results :msg="child" />
    </section>
  </div>
</template>

<script>
import Search from '@/components/Search.vue';
import Results from '@/components/Results.vue';

export default {
  name: 'Home',
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
