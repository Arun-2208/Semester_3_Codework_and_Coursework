<template>
  <div class="w-screen min-h-screen bg-white font-['Calibri'] flex flex-col items-center px-6 pt-12">
    <h2 class="text-2xl font-semibold text-[#4F378A] mb-6">Scan History</h2>

    <div class="w-full max-w-5xl bg-[#F5F5F5] rounded-xl p-6 shadow-md">
      <table class="w-full text-sm text-left border-collapse">
        <thead>
          <tr class="bg-[#EDE4FF] text-[#4F378A] uppercase text-xs">
            <th class="px-6 py-4">Scan ID</th>
            <th class="px-6 py-4">Timestamp</th>
            <th class="px-6 py-4">Result</th>
            <th class="px-6 py-4">Download</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="scan in scans" :key="scan.scan_id" class="bg-white border-b text-[#4F378A] hover:bg-gray-50 transition">
            <td class="px-6 py-4">{{ scan.scan_id }}</td>
            <td class="px-6 py-4">{{ formatDate(scan.scan_timestamp) }}</td>
            <td class="px-6 py-4">{{ scan.result_1 }}</td>
            <td class="px-6 py-4">
              <button
                @click="downloadPdf(scan.scan_id)"
                class="bg-[#4F378A] hover:bg-[#3e2c6a] text-white px-4 py-2 rounded-full text-xs font-medium"
              >
                PDF
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!scans.length" class="text-gray-500 text-center mt-6">
        No scan history available.
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import jsPDF from 'jspdf';
import { base64Logo } from '../assets/logo_base64.js';

export default {
  name: 'ScanHistory',
  data() {
    return {
      scans: [],
    };
  },
  async mounted() {
  const user = JSON.parse(sessionStorage.getItem('user'));
  try {
    const res = await axios.get(`http://localhost:5000/scan-history?user_id=${user.user_id}`);
    // Sort the scans by scan_id in ascending order
    this.scans = res.data.sort((a, b) => a.scan_id - b.scan_id);
  } catch (err) {
    console.error('Error fetching scan history:', err);
  }
},
  methods: {
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleString();
    },
    async downloadPdf(scan_id) {
  try {
    const res = await axios.get(`http://localhost:5000/scan-details/${scan_id}`);
    const scan = res.data;
    const user = JSON.parse(sessionStorage.getItem('user'));

    const formatPercent = (value) => {
      return (value && value !== '--' && !isNaN(value)) ? `${Math.round(parseFloat(value) * 100)}%` : '--';
    };

    const results = [
      ['1', scan.malware_type_1, formatPercent(scan.anomaly_score_1), formatPercent(scan.accuracy_1), formatPercent(scan.risk_1), scan.result_1],
      ['2', scan.malware_type_2, formatPercent(scan.anomaly_score_2), formatPercent(scan.accuracy_2), formatPercent(scan.risk_2), scan.result_2],
      ['3', scan.malware_type_3, formatPercent(scan.anomaly_score_3), formatPercent(scan.accuracy_3), formatPercent(scan.risk_3), scan.result_3],
    ];

    const doc = new jsPDF();
    doc.addImage(base64Logo, 'JPEG', 150, 10, 40, 12);

    doc.setFontSize(16);
    doc.setTextColor(40);
    doc.text('CyberShieldAI - Malware Scan Report', 10, 20);

    doc.setFontSize(11);
    doc.setTextColor(0);
    doc.text(`Scan ID: ${scan.scan_id}`, 10, 30);
    doc.text(`Timestamp: ${this.formatDate(scan.scan_timestamp)}`, 10, 37);
    doc.text(`User Name: ${user.username}`, 10, 47);
    doc.text(`Email: ${user.email}`, 10, 54);
    doc.text(`User Type: ${user.user_type}`, 10, 61);

    doc.setFontSize(10);
    doc.setTextColor(60);
    doc.text('This report summarises the malware detection results from the AI-based analysis.', 10, 69);

    const headers = ['#', 'Malware Type', 'Anomaly Score', 'Accuracy', 'Risk'];
    const colWidths = [10, 60, 35, 35, 30];
    const startX = 10;
    let startY = 80;

    doc.setFillColor(240);
    doc.rect(startX, startY, colWidths.reduce((a, b) => a + b), 10, 'F');
    doc.setTextColor(50);
    headers.forEach((header, i) => {
      doc.text(header, startX + colWidths.slice(0, i).reduce((a, b) => a + b, 0) + 2, startY + 7);
    });

    results.forEach((row, rowIndex) => {
      let rowY = startY + 10 + rowIndex * 10;
      row.slice(0, 5).forEach((cell, colIndex) => {
        const cellX = startX + colWidths.slice(0, colIndex).reduce((a, b) => a + b, 0);
        doc.rect(cellX, rowY, colWidths[colIndex], 10);
        const isRiskCol = headers[colIndex] === 'Risk';
        doc.setTextColor(isRiskCol && cell === '100%' ? 200 : 30, 0, 0);
        doc.text(String(cell), cellX + 2, rowY + 7);
      });
    });

    const summaryY = startY + 10 + results.length * 10 + 10;
    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text(`Historical Average Error: ${scan.historical_avg_error}`, 10, summaryY);

    const isAllMalware = results.some(r => (r[5] || '').toLowerCase() === 'malware');
    doc.setFontSize(11);
    doc.setTextColor(isAllMalware ? 200 : 0, isAllMalware ? 0 : 150, 0);
    doc.text(
      isAllMalware ? 'Verdict: Malware detected in this scan.' : ' Verdict: Safe – No threats detected in this scan.',
      10,
      summaryY + 10
    );

    doc.setFontSize(9);
    doc.setTextColor(60);
    doc.text('For more information, contact CyberShieldAI support.', 10, summaryY + 18);

    doc.save(`scan_${scan.scan_id}.pdf`);
  } catch (err) {
    console.error('Error downloading report:', err);
  }
}



  }
};
</script>

<style scoped>
table {
  border-spacing: 0;
}
</style>
