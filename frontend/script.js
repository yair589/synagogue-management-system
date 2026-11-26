const API_URL = 'http://localhost:8000/api';

async function checkHealth() {
  try {
    const res = await fetch(`${API_URL}/health`);
    if (res.ok) {
      document.getElementById('backend-status').className = 'mb-4 p-2 bg-emerald-100 text-emerald-800 rounded text-center text-sm';
      document.getElementById('backend-status').innerText = '✅ שרת ה-Backend מחובר ופעיל!';
    }
  } catch (err) {
    document.getElementById('backend-status').className = 'mb-4 p-2 bg-red-100 text-red-800 rounded text-center text-sm';
    document.getElementById('backend-status').innerText = '❌ שגיאת חיבור ל-Backend';
  }
}

async function loadDonations() {
  const list = document.getElementById('donations-list');
  try {
    const res = await fetch(`${API_URL}/donations`);
    const data = await res.json();
    
    list.innerHTML = '';
    if (Array.isArray(data) && data.length > 0) {
      data.forEach(item => {
        const li = document.createElement('li');
        li.className = 'p-2 bg-slate-50 border rounded flex justify-between items-center';
        li.innerHTML = `<span class="font-medium text-slate-800">${item.donor_name}</span><span class="font-bold text-emerald-600">₪${item.amount}</span>`;
        list.appendChild(li);
      });
    } else {
      list.innerHTML = '<li class="text-slate-400 text-center">אין תרומות להצגה</li>';
    }
  } catch (err) {
    list.innerHTML = '<li class="text-red-500 text-center">שגיאה בטעינת נתונים</li>';
    console.error(err);
  }
}

async function sendDonation() {
  const nameInput = document.getElementById('name');
  const amountInput = document.getElementById('amount');
  const name = nameInput.value.trim();
  const amount = amountInput.value.trim();

  if (!name || !amount) {
    alert('נא למלא שם וסכום תרומה');
    return;
  }

  try {
    const res = await fetch(`${API_URL}/donations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ donor_name: name, amount: parseFloat(amount) })
    });

    if (res.ok) {
      alert(' תודה רבה! התרומה נקלטה בהצלחה במסד הנתונים');
      nameInput.value = '';
      amountInput.value = '';
      await loadDonations(); // רענון הרשימה מיד
    } else {
      alert('אירעה שגיאה בשמירת התרומה בשרת');
    }
  } catch (err) {
    alert('שגיאת תקשורת עם השרת');
    console.error(err);
  }
}

// הרצה ראשונית
checkHealth();
loadDonations();
