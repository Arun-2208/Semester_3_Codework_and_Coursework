<template>
  <div class="w-screen min-h-screen bg-white flex flex-col font-['Calibri'] items-center overflow-x-hidden px-4 py-8">
    <div class="w-full max-w-5xl">
      <!-- Upload Section -->
      <div class="bg-[#F3F3F3] rounded-xl p-8 flex flex-col items-center shadow-md">
        <label for="file-upload" class="w-full max-w-xl h-40 bg-white rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center cursor-pointer">
          <span class="text-gray-500 text-lg font-medium">
            {{ file ? file.name : '+ Upload file to be scanned' }}
          </span>
        </label>
        <input id="file-upload" type="file" accept=".csv" class="hidden" @change="onFileChange" />
        <div class="flex justify-center gap-4 mt-6">
          <button
            @click="runScan"
            :disabled="!file"
            class="w-40 py-3 bg-[#4F378A] text-white rounded-full text-base font-semibold disabled:opacity-50"
          >Run Scan</button>
          <button
            @click="clearFile"
            class="w-40 py-3 bg-gray-300 text-black rounded-full text-base font-medium"
          >Clear</button>
        </div>
      </div>

      <!-- Results -->
      <div v-if="results.length" class="mt-10">
        <h3 class="text-xl font-semibold text-[#4F378A] mb-6 text-center">Scan Results</h3>

        <div
          v-for="(res, i) in results"
          :key="i"
          class="mb-8 p-6 rounded-lg shadow border border-gray-200 bg-white"
        >
          <div class="flex justify-between items-center mb-4">
            <p class="text-lg font-bold text-[#4F378A]">Classification {{ i + 1 }} – {{ fileName || 'Unnamed.csv' }}</p>
            <button
              @click="downloadPdf(res.scan_id)"
              class="bg-[#4F378A] text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-[#3e2c6a]"
            >Download Report</button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
            <p><strong>Filename:</strong> {{ fileName }}</p>
            <p><strong>Result:</strong> {{ res.prediction.result }}</p>
            <p><strong>Type:</strong> {{ res.prediction.malware_type }}</p>
            <p><strong>Anomaly Score:</strong> {{ formatPercent(res.prediction.anomaly_detection_score) }}</p>
            <p><strong>Prediction Accuracy:</strong> {{ formatPercent(res.prediction.prediction_accuracy) }}</p>
            <p><strong>Future Risk:</strong> {{ formatPercent(res.prediction.future_risk_rating) }}</p>
            <p class="col-span-2">
              <strong>Severity:</strong>
              <span :class="getSeverityBadge(res.prediction.future_risk_rating)" class="ml-2 px-3 py-1 rounded-full text-xs font-medium">
                {{ getSeverityLabel(res.prediction.future_risk_rating) }}
              </span>
            </p>
          </div>

          <!-- Pie Charts -->
          <div class="mt-8 flex flex-col md:flex-row justify-center items-center gap-8">
            <div class="text-center">
              <h5 class="font-medium text-[#4F378A] mb-2">Detection Accuracy</h5>
              <PieChartComponent
                :risk="res.prediction.prediction_accuracy * 100"
                :result="res.prediction.result"
                :label="'Detection Accuracy'"
                :malwareType="res.prediction.malware_type"
              />
            </div>
            <div v-if="res.prediction.result === 'malware'" class="text-center">
              <h5 class="font-medium text-[#4F378A] mb-2">Future Risk Rating</h5>
              <PieChartComponent
                :risk="res.prediction.future_risk_rating * 100"
                :result="res.prediction.result"
                :label="'Future Risk'"
                :malwareType="res.prediction.malware_type"
              />
            </div>
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
import jsPDF from 'jspdf'; // ✅ Added jsPDF import

// Optional placeholder logo (if needed)
const base64Logo = ''; // or add your actual base64 string here

export default {
  name: 'ScanFile',
  components: { PieChartComponent },
  data() {
    return {
      file: null,
      fileName: '',
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
      this.fileName = this.file ? this.file.name : '';
    },
    clearFile() {
      this.file = null;
      this.fileName = '';
      document.getElementById('file-upload').value = '';
      this.results = [];
    },
    formatPercent(val) {
      return isNaN(val) ? '--' : `${(parseFloat(val) * 100).toFixed(2)}%`;
    },
    getSeverityBadge(risk) {
      if (risk === '--' || isNaN(risk)) return 'bg-gray-300 text-gray-700';
      if (risk < 0.6) return 'bg-green-100 text-green-700';
      if (risk < 0.72) return 'bg-yellow-100 text-yellow-700';
      return 'bg-red-100 text-red-700';
    },
    getSeverityLabel(risk) {
      if (risk === '--' || isNaN(risk)) return 'N/A';
      if (risk < 0.6) return 'Low';
      if (risk < 0.72) return 'Medium';
      return 'High';
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
        const scanId = res.data.scan_id || 1;
        this.results = res.data.predictions.map(p => ({ ...p, scan_id: scanId }));
      } catch (err) {
        console.error('Scan failed:', err);
        alert('Scan failed. Please check the file and format.');
      }
    },
           async downloadPdf() {
      try {
        const user = JSON.parse(sessionStorage.getItem('user'));
        
        // Step 1: Fetch scan history and get the latest scan_id
        const historyRes = await axios.get(`http://localhost:5000/scan-history?user_id=${user.user_id}`);
        const scans = historyRes.data;
        if (!scans.length) {
          alert("No scans found for this user.");
          return;
        }

        const latestScanId = scans[0].scan_id;

        // Step 2: Fetch scan details using latest scan_id
        const res = await axios.get(`http://localhost:5000/scan-details/${latestScanId}`);
        const scan = res.data;

        const formatPercent = (value) => (value && value !== '--' && !isNaN(value)) ? `${Math.round(parseFloat(value) * 100)}%` : '--';

        const results = [
          ['1', scan.result_1, scan.malware_type_1, formatPercent(scan.anomaly_score_1), formatPercent(scan.accuracy_1), formatPercent(scan.risk_1)],
          ['2', scan.result_2, scan.malware_type_2, formatPercent(scan.anomaly_score_2), formatPercent(scan.accuracy_2), formatPercent(scan.risk_2)],
          ['3', scan.result_3, scan.malware_type_3, formatPercent(scan.anomaly_score_3), formatPercent(scan.accuracy_3), formatPercent(scan.risk_3)],
        ];

        const doc = new jsPDF();
        if (base64Logo) {
          doc.addImage(base64Logo, 'JPEG', 150, 10, 40, 12);
        }

        doc.setFontSize(16);
        doc.text('CyberShieldAI - Malware Scan Report', 10, 20);
        doc.setFontSize(11);
        doc.text(`Scan ID: ${scan.scan_id}`, 10, 30);
        doc.text(`Timestamp: ${scan.scan_timestamp}`, 10, 37);
        doc.text(`User Name: ${user.username}`, 10, 47);
        doc.text(`Email: ${user.email}`, 10, 54);
        doc.text(`User Type: ${user.user_type}`, 10, 61);

        doc.setFontSize(10);
        doc.text('This report summarises the malware detection results from the AI-based analysis.', 10, 69);

        const headers = ['#', 'Result', 'Malware Type', 'Anomaly Score', 'Accuracy', 'Risk'];
        const colWidths = [10, 25, 40, 35, 35, 30];
        const startX = 10;
        let y = 80;

        doc.setFillColor(240);
        doc.rect(startX, y, colWidths.reduce((a, b) => a + b), 10, 'F');
        doc.setTextColor(50);
        headers.forEach((h, i) => {
          doc.text(h, startX + colWidths.slice(0, i).reduce((a, b) => a + b, 0) + 2, y + 7);
        });

        results.forEach((row, rowIndex) => {
          let rowY = y + 10 + rowIndex * 10;
          row.forEach((cell, colIndex) => {
            const cellX = startX + colWidths.slice(0, colIndex).reduce((a, b) => a + b, 0);
            doc.rect(cellX, rowY, colWidths[colIndex], 10);
            doc.setTextColor(30);
            doc.text(String(cell), cellX + 2, rowY + 7);
          });
        });

        const summaryY = y + 10 + results.length * 10 + 5;
        doc.setFontSize(10);
        doc.setTextColor(100);
        doc.text(`Historical Average Error: ${scan.historical_avg_error}`, 10, summaryY);

        const isAllMalware = results.some(r => (r[1] || '').toLowerCase() === 'malware');
        doc.setFontSize(11);
        doc.setTextColor(isAllMalware ? 200 : 0, isAllMalware ? 0 : 150, 0);
        doc.text(
          isAllMalware ? 'Verdict: Malware detected in this scan.' : 'Verdict: Safe – No threats detected in this scan.',
          10,
          summaryY + 10
        );

        doc.setFontSize(9);
        doc.setTextColor(60);
        doc.text('For more information, contact CyberShieldAI support.', 10, summaryY + 18);

        doc.save(`scan_${scan.scan_id}.pdf`);
      } catch (err) {
        console.error('Error downloading report:', err);
        alert("Failed to download report. Please try again.");
      }
    }


  }
};
</script>
