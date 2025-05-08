<template>
    <div class="w-screen min-h-screen bg-white font-['Calibri'] flex flex-col items-center px-6 pt-12">
      <!-- Title -->
      <h2 class="text-2xl font-semibold text-[#4F378A] mb-6">Scan History</h2>
  
      <!-- Table Wrapper -->
      <div class="w-full max-w-5xl bg-[#F5F5F5] rounded-xl p-6 shadow-md">
        <!-- Table -->
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
            <tr
              v-for="scan in scans"
              :key="scan.scan_id"
              class="bg-white border-b hover:bg-gray-50 transition"
            >
              <td class="px-6 py-4">{{ scan.scan_id }}</td>
              <td class="px-6 py-4">{{ formatDate(scan.scan_timestamp) }}</td>
              <td class="px-6 py-4">{{ scan.result_1 }}</td>
              <td class="px-6 py-4">
                <button
                  @click="downloadPdf(scan)"
                  class="bg-[#4F378A] hover:bg-[#3e2c6a] text-white px-4 py-2 rounded-full text-xs font-medium"
                >
                  PDF
                </button>
              </td>
            </tr>
          </tbody>
        </table>
  
        <!-- Empty Message -->
        <div v-if="!scans.length" class="text-gray-500 text-center mt-6">
          No scan history available.
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import jsPDF from 'jspdf';
  
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
        this.scans = res.data;
      } catch (err) {
        console.error('Error fetching scan history:', err);
      }
    },
    methods: {
      formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleString();
      },
      downloadPdf(scan) {
        const doc = new jsPDF();
        doc.setFontSize(14);
        doc.text(`Scan Report`, 10, 10);
        doc.setFontSize(11);
        doc.text(`Scan ID: ${scan.scan_id}`, 10, 20);
        doc.text(`Timestamp: ${this.formatDate(scan.scan_timestamp)}`, 10, 30);
        doc.text(`Result: ${scan.result_1}`, 10, 40);
        doc.save(`scan_${scan.scan_id}.pdf`);
      },
    },
  };
  </script>
  
  <style scoped>
  table {
    border-spacing: 0;
  }
  </style>
  