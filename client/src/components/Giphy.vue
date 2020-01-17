<template>
  <div>
    <img :src="this.giphy.images.original.url" />
    <div v-if="this.authenticated">
      <div>
        <a class="button is-large is-primary" @click.stop="deleteGiphy">Delete</a>
      </div>
      <div v-if="!this.inAccount">
        <a class="button is-large is-primary" @click.stop="saveGiphy">Save</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Giphy',
  computed: {
    giphy() {
      return this.$store.getters.giphy;
    },
    authenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  data() {
    return {
      inAccount: false,
    };
  },
  beforeMount() {
    if (this.authenticated) {
      this.$store.dispatch('getUserGiphies').then(() => {
        this.$store.getters.giphies.forEach((giphy) => {
          if (this.giphy.id === giphy.id) {
            this.inAccount = true;
          }
        });
      });
    }
  },
  methods: {
    async deleteGiphy() {
      await this.$store.dispatch('deleteUserGiphy', this.giphy.id)
        .then(() => {
          this.$root.$emit('changeView', 'profile');
        });
    },
    async saveGiphy() {
      await this.$store.dispatch('saveUserGiphy', this.giphy.id)
        .then(() => {
          this.$store.dispatch('getUserGiphies')
            .then(() => {
              this.$root.$emit('changeView', 'profile');
            });
        });
    },
  },
};
</script>
