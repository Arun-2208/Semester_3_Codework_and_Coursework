<template>
  <div class="w-screen min-h-screen bg-white font-['Calibri'] flex flex-col items-center py-8 px-4">
    <!-- Loading Bar -->
    <div v-if="loading" class="w-full max-w-4xl mb-4">
      <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div class="h-full bg-[#4F378A] animate-pulse w-full"></div>
      </div>
      <p class="text-xs text-gray-500 text-center mt-1">Training in progress… please wait</p>
    </div>

    <div class="w-full max-w-4xl bg-[#F4F0FF] rounded-2xl p-8 shadow-lg">
      <h2 class="text-2xl font-semibold text-[#4F378A] mb-6 text-center">Update & Retrain Model</h2>

      <!-- Hyperparameter Inputs -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="flex flex-col">
          <label class="text-sm text-gray-600 mb-1">Epochs</label>
          <input type="number" v-model="epochs" class="px-3 text-[#4F378A] bg-white py-2 border rounded-md text-[#4F378A]" />
        </div>
        <div class="flex flex-col">
          <label class="text-sm text-gray-600 mb-1">Batch Size</label>
          <input type="number" v-model="batch_size" class="px-3 text-[#4F378A] bg-white  py-2 border rounded-md text-[#4F378A]" />
        </div>
        <div class="flex flex-col">
          <label class="text-sm text-gray-600 mb-1">Learning Rate</label>
          <input type="number" step="0.0001" v-model="learning_rate" class="px-3 text-[#4F378A] bg-white  py-2 border rounded-md text-[#4F378A]" />
        </div>
      </div>

      <!-- Dataset Download + Upload -->
      <div class="flex flex-col md:flex-row justify-center items-center gap-4 mb-6">
        <button
          @click="downloadDataset"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md font-medium"
        >
          Download Dataset
        </button>
        <div>
  <input
    type="file"
    id="upload-dataset"
    accept=".csv"
    @change="handleFileUpload"
    class="hidden"
  />
  <label
    for="upload-dataset"
    class="cursor-pointer bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-md font-medium inline-block"
  >
    Upload Updated Dataset
  </label>
</div>
      </div>

      <!-- Status Message -->
      <div v-if="successMessage" class="text-green-700 bg-green-100 border border-green-300 px-4 py-2 rounded text-center mb-4">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="text-red-700 bg-red-100 border border-red-300 px-4 py-2 rounded text-center mb-4">
        {{ errorMessage }}
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col md:flex-row gap-4 justify-center mb-6">
        <button
          :disabled="loading"
          @click="retrainModel"
          class="bg-[#4F378A] hover:bg-[#3e2c6a] text-white px-6 py-2 rounded-md font-medium"
        >
          Retrain Model
        </button>
      </div>

      <!-- Plot + Logs -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white border rounded-lg p-4 shadow-inner">
          <h3 class="text-[#4F378A] font-medium mb-2">Training Plot</h3>
          <img v-if="trainingPlot" :src="'data:image/png;base64,' + trainingPlot" class="w-full rounded" />
          <p v-else class="text-sm text-gray-500 italic">No plot yet</p>
        </div>
        <div class="bg-white border rounded-lg p-4 shadow-inner">
          <h3 class="text-[#4F378A] font-medium mb-2">Logs</h3>
          <pre class="text-xs text-gray-700 whitespace-pre-wrap max-h-64 overflow-auto">{{ logs.join('\n') }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UpdateModel',
  data() {
    return {
      epochs: 100,
      batch_size: 32,
      learning_rate: 0.001,
      trainingPlot: null,
      logs: [],
      loading: false,
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    async downloadDataset() {
      try {
        const res = await axios.get('http://localhost:5000/get-dataset', {
          responseType: 'blob'
        });
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'RF_1_dataset.csv');
        document.body.appendChild(link);
        link.click();
        link.remove();
        this.successMessage = ' Dataset downloaded successfully!';
        this.errorMessage = '';
      } catch (err) {
        console.error('Download error:', err);
        this.errorMessage = 'Failed to download dataset.';
        this.successMessage = '';
      }
    },
    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file || !file.name.endsWith('.csv')) {
        this.errorMessage = ' Please upload a valid CSV file.';
        this.successMessage = '';
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      try {
        await axios.post('http://localhost:5000/upload-dataset', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        this.successMessage = ' Updated dataset uploaded successfully!';
        this.errorMessage = '';
      } catch (err) {
        console.error('Upload error:', err);
        this.errorMessage = ' Failed to upload updated dataset.';
        this.successMessage = '';
      }
    },
    async retrainModel() {
      this.loading = true;
      this.logs = [];
      this.trainingPlot = null;
      this.successMessage = '';
      this.errorMessage = '';
      try {
        const res = await axios.post('http://localhost:5000/retrain-model', {
          epochs: this.epochs,
          batch_size: this.batch_size,
          learning_rate: this.learning_rate
        });
        this.logs = res.data.logs;
        this.trainingPlot = res.data.training_plot;
        this.successMessage = ' Model retrained successfully!';
      } catch (err) {
        console.error('Retrain error:', err);
        this.errorMessage = ' Model retraining failed.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
input[type='number'],
input[type='text'] {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 4px;
}
</style>
