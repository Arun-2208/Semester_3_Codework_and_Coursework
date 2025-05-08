<template>
    <div class="w-screen min-h-screen bg-white font-['Calibri'] flex flex-col items-center px-6 pt-12">
      <!-- Title -->
      <h2 class="text-2xl font-semibold text-[#4F378A] mb-6">Update Dataset & Retrain Model</h2>
  
      <!-- Content Card -->
      <div class="w-full max-w-3xl bg-[#F5F5F5] rounded-xl p-8 shadow-md flex flex-col items-center">
        <!-- File Upload -->
        <label
          for="file-upload"
          class="w-full max-w-xl h-40 bg-gray-200 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center cursor-pointer mb-6"
        >
          <span class="text-gray-600 text-lg">+ Upload new dataset file</span>
        </label>
        <input id="file-upload" type="file" class="hidden" @change="onFile" />
  
        <!-- Train Button -->
        <button
          @click="train"
          :disabled="!file"
          class="w-40 py-3 bg-[#4F378A] text-white rounded-full text-base font-medium disabled:opacity-50"
        >
          Train
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UpdateModel',
    data() {
      return {
        file: null,
      };
    },
    methods: {
      onFile(e) {
        this.file = e.target.files[0];
      },
      async train() {
        try {
          const form = new FormData();
          form.append('datafile', this.file);
          await axios.post('http://localhost:5000/train-model', form);
          alert('Retraining started');
        } catch (err) {
          alert('Failed to start training');
          console.error(err);
        }
      },
    },
  };
  </script>
  