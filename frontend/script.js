const API_URL = 'http://localhost:8000/api';

async function checkHealth() {
  try {
    const res = await fetch(`${API_URL}/health`);
    const data = await res.json();
    document.getElementById('backend-status').className = 'mb-4 p-2 bg-emerald-100 text-emerald-800 rounded text-center text-sm';
    document.getElementById('backend-status').innerText = '✅ שרת ה-Backend מחובר ופעיל!';
  } catch (err) {
    document.getElementById('backend-status').className = 'mb-4 p-2 bg-red-100 text-red-800 rounded text-center text-sm';
    document.getElementById('backend-status').innerText = '❌ שגיאת חיבור ל-Backend';
  }
}

async function loadDonations() {
  try {
    const res = await fetch(`${API_URL}/donations`);
    const data = await res.json();
    const list = document.getElementById('donations-list');
    list.innerHTML = '';
    data.forEach(item => {
      const li = document.createElement('li');
      li.className = 'p-1.5 bg-slate-50 border rounded flex justify-between';
      li.innerHTML = `<span>${item.donor_name}</span><span class="font-bold text-emerald-600">₪${item.amount}</span>`;
      list.appendChild(li);
    });
  } catch (err) {
    console.error(err);
  }
}

async function sendDonation() {
  const name = document.getElementById('name').value;
  const amount = document.getElementById('amount').value;
  if (!name || !amount) return alert('נא למלא שם וסכום');

  await fetch(`${API_URL}/donations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ donor_name: name, amount: parseFloat(amount) })
  });

  document.getElementById('name').value = '';
  document.getElementById('amount').value = '';
  loadDonations();
}

// הרצה בטעינת המסך
checkHealth();
loadDonations();
