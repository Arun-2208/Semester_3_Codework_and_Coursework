<template>
  <div class="w-screen min-h-screen bg-white flex flex-col font-['Calibri'] items-center overflow-x-hidden">
    <div class="w-[60%] max-w-[1440px] flex flex-col mt-6">
      
      <!-- Upload Section -->
      <div class="bg-[#F3F3F3] rounded-xl p-8 flex flex-col items-center shadow-md">
        <label
          for="file-upload"
          class="w-full max-w-xl h-40 bg-white rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center cursor-pointer"
        >
          <span class="text-gray-500 text-lg font-medium">
            {{ file ? file.name : '+ Upload file to be scanned' }}
          </span>
        </label>
        <input
          id="file-upload"
          type="file"
          accept=".csv"
          class="hidden"
          @change="onFileChange"
        />

        <div class="flex space-x-6 mt-6">
          <button
            @click="runScan"
            :disabled="!file"
            class="w-40 py-3 bg-[#4F378A] text-white rounded-full text-base font-semibold disabled:opacity-50"
          >
            Run Scan
          </button>
          <button
            @click="clearFile"
            class="w-40 py-3 bg-gray-200 text-black rounded-full text-base font-medium"
          >
            Clear
          </button>
        </div>
      </div>

      <!-- Results -->
      <div v-if="results.length" class="w-full max-w-5xl mt-10 mx-auto">
        <h3 class="text-xl font-semibold text-[#4F378A] mb-4">Scan Results</h3>

        <div
          v-for="(res, i) in results"
          :key="i"
          class="mb-6 p-6 rounded-lg shadow border border-gray-200 bg-white"
        >
          <p class="text-lg font-bold mb-2">File {{ i + 1 }}</p>
          <div
            class="grid grid-cols-2 gap-y-2 text-sm"
            :class="res.prediction.result === 'malware' ? 'text-red-700' : 'text-green-700'"
          >
            <p><strong>Result:</strong> <span class="font-semibold">{{ res.prediction.result }}</span></p>
            <p><strong>Type:</strong> <span class="font-semibold">{{ res.prediction.malware_type }}</span></p>
            <p>
              <strong>Anomaly Score:</strong>
              <span class="font-semibold">{{ formatPercent(res.prediction.anomaly_detection_score) }}</span>
            </p>
            <p>
              <strong>Prediction Accuracy:</strong>
              <span class="font-semibold">{{ formatPercent(res.prediction.prediction_accuracy) }}</span>
            </p>
            <p>
              <strong>Future Risk:</strong>
              <span class="font-semibold">{{ formatPercent(res.prediction.future_risk_rating) }}</span>
            </p>
          </div>

          <!-- Pie Chart -->
          <div class="mt-6 flex justify-center">
            <PieChartComponent
              :risk="res.prediction.future_risk_rating * 100"
              :result="res.prediction.result"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Papa from 'papaparse';
import PieChartComponent from '../components/PieChartComponent.vue';

export default {
  name: 'ScanFile',
  components: {
    PieChartComponent,
  },
  data() {
    return {
      file: null,
      results: [],
      userName: '',
    };
  },
  mounted() {
    const user = JSON.parse(sessionStorage.getItem('user'));
    this.userName = user?.username || 'User';
  },
  methods: {
    onFileChange(e) {
      this.file = e.target.files[0];
    },
    clearFile() {
      this.file = null;
      document.getElementById('file-upload').value = '';
      this.results = [];
    },
    formatPercent(val) {
      return isNaN(val) ? '--' : `${(parseFloat(val) * 100).toFixed(2)}%`;
    },
    async runScan() {
      if (!this.file) return;

      try {
        const csvText = await this.file.text();
        const parsed = Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true
        });

        if (!parsed.data || parsed.data.length < 1) {
          alert('CSV file is empty or invalid.');
          return;
        }

        const samples = parsed.data.map(row => {
          const converted = {};
          for (let key in row) {
            const val = row[key].trim();
            converted[key.trim()] = isNaN(val) ? val : parseFloat(val);
          }
          return converted;
        });

        const user = JSON.parse(sessionStorage.getItem('user'));

        const res = await axios.post('http://localhost:5000/predict', {
          user_id: user.user_id,
          samples: samples
        });

        this.results = res.data.predictions;
      } catch (err) {
        console.error('Scan failed:', err);
        alert('Scan failed. Please check the file and format.');
      }
    }
  }
};
</script>
