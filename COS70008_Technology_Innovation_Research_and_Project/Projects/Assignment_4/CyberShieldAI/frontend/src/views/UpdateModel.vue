
<template>
  <div class="p-6">
    <h2 class="text-2xl mb-4">Update Dataset & Retrain Model</h2>
    <input type="file" @change="onFile" class="mb-4" />
    <button @click="train" class="px-6 py-2 bg-[#4F378A] text-white rounded">Train</button>
  </div>
</template>
<script>
import axios from 'axios';
export default {
  name: 'UpdateModel',
  data() { return { file: null }; },
  methods: {
    onFile(e) { this.file = e.target.files[0]; },
    async train() {
      const form = new FormData();
      form.append('datafile', this.file);
      await axios.post('http://localhost:5000/train-model', form);
      alert('Retraining started');
    }
  }
};
</script>