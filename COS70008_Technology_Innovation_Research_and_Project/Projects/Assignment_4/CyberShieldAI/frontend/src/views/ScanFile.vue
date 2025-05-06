
<template>
  <div class="p-8">
    <label for="file-upload" class="w-full h-48 bg-gray-100 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center cursor-pointer">
      <span class="text-gray-500">+ Upload file to be scanned</span>
    </label>
    <input id="file-upload" type="file" class="hidden" @change="onFileChange" />
    <div class="mt-6 flex gap-4">
      <button @click="runScan" :disabled="!file" class="px-6 py-2 bg-[#4F378A] text-white rounded-full disabled:opacity-50">Run Scan</button>
      <button @click="clearFile" class="px-6 py-2 bg-gray-200 text-black rounded-full">Clear</button>
    </div>
    <div v-if="results.length" class="mt-8">
      <div v-for="(res,i) in results" :key="i" class="mb-4 p-4 border rounded-lg">
        <p><strong>Sample {{i+1}}</strong></p>
        <p>Result: {{res.prediction.result}}</p>
        <p>Type: {{res.prediction.malware_type}}</p>
        <p>Anomaly: {{res.prediction.anomaly_detection_score}}</p>
        <p>Accuracy: {{res.prediction.prediction_accuracy}}</p>
        <p>Risk: {{res.prediction.future_risk_rating}}</p>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
export default {
  name: 'ScanFile',
  data() { return { file: null, results: [] }; },
  methods: {
    onFileChange(e) { this.file = e.target.files[0]; },
    clearFile() { this.file = null; document.getElementById('file-upload').value = ''; this.results = []; },
    async runScan() {
      const content = await this.file.text();
      const samples = JSON.parse(content);
      const user = JSON.parse(localStorage.getItem('user'));
      const res = await axios.post('http://localhost:5000/predict', { user_id: user.user_id, samples });
      this.results = res.data.predictions;
    }
  }
};
</script>