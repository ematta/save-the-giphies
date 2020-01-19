<template>
  <div>
    <img :src="giphy.images.original.url" />
    <div v-if="isAuthenticated">
      <div>
        <a class="button is-large is-primary" @click.stop="deleteGiphy">Delete</a>
      </div>
      <div v-if="!inAccount">
        <a class="button is-large is-primary" @click.stop="saveGiphy">Save</a>
      </div>
      <div v-if="inAccount">
        Tag:
        <input
          ref="addTagInput"
          placeholder="Press enter to tag"
          @keyup.enter="addTag"
        />
      </div>
      <div v-if="tags.length > 0" :key="tags.legnth">
        Tags set for this giphy (click to remove):
        <br />
        <div v-for="tag in tags" :key="tag.id">
          <a @click.stop="removeTag(tag.id)"> {{ tag.tag }} </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'Giphy',
  computed: mapState([
    'isAuthenticated',
    'giphy',
    'tags',
  ]),
  data() {
    return {
      inAccount: false,
    };
  },
  beforeMount() {
    if (this.isAuthenticated) {
      this.$store.dispatch('getUserGiphies').then(() => {
        this.$store.getters.giphies.forEach((giphy) => {
          if (this.giphy.id === giphy.id) {
            this.inAccount = true;
          }
        });
      });
      this.getTags();
    }
  },
  methods: {
    async addTag() {
      await this.$store.dispatch(
        'addTagToGiphy',
        {
          tag: this.$refs.addTagInput.value,
          giphyId: this.giphy.id,
        },
      ).then(this.$refs.addTagInput.value = '');
    },
    async deleteGiphy() {
      await this.$store.dispatch('deleteUserGiphy', this.giphy.id);
    },
    async saveGiphy() {
      await this.$store.dispatch('saveUserGiphy', this.giphy.id);
    },
    async getTags() {
      await this.$store.dispatch('getTagsToGiphy', this.giphy.id);
    },
    async removeTag(tagId) {
      await this.$store.dispatch('removeTagFromGiphy', { giphyId: this.giphy.id, tag: tagId });
    },
  },
};
</script>
