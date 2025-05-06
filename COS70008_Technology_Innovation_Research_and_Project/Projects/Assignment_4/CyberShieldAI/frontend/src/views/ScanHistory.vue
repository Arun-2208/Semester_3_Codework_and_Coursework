

<template>
  <div class="p-6">
    <h2 class="text-2xl mb-4">Scan History</h2>
    <table class="min-w-full bg-white">
      <thead><tr>
        <th class="border px-4 py-2">Scan ID</th>
        <th class="border px-4 py-2">Timestamp</th>
        <th class="border px-4 py-2">Result</th>
        <th class="border px-4 py-2">Download</th>
      </tr></thead>
      <tbody>
        <tr v-for="scan in scans" :key="scan.scan_id">
          <td class="border px-4 py-2">{{ scan.scan_id }}</td>
          <td class="border px-4 py-2">{{ scan.scan_timestamp }}</td>
          <td class="border px-4 py-2">{{ scan.result_1 }}</td>
          <td class="border px-4 py-2">
            <button @click="downloadPdf(scan)" class="bg-[#4F378A] text-white px-3 py-1 rounded">PDF</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import axios from 'axios';
import jsPDF from 'jspdf';
export default {
  name: 'ScanHistory',
  data() { return { scans: [] }; },
  async mounted() {
    const user = JSON.parse(localStorage.getItem('user'));
    const res = await axios.get(`http://localhost:5000/scan-history?user_id=${user.user_id}`);
    this.scans = res.data;
  },
  methods: {
    downloadPdf(scan) {
      const doc = new jsPDF();
      doc.text(`Scan ID: ${scan.scan_id}`, 10, 10);
      doc.text(`Result: ${scan.result_1}`, 10, 20);
      // ... add more details
      doc.save(`scan_${scan.scan_id}.pdf`);
    }
  }
};
</script>
