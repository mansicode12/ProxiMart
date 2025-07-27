const API_BASE_URL = "http://localhost:5000/api";

// Helper function to handle fetch errors
const handleResponse = async (res) => {
  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: "Unknown error" }));
    throw new Error(error.error || "API request failed");
  }
  return res.json();
};

// Suppliers
export const getSuppliers = async () => {
  const res = await fetch(`${API_BASE_URL}/suppliers/all`);
  return handleResponse(res).then(data => data.suppliers);
};

// Orders
export const getOrders = async (vendorId = "vendor1") => {
  const res = await fetch(`${API_BASE_URL}/orders/history?vendor_id=${vendorId}`);
  return handleResponse(res);
};

// Inventory (updated to accept vendorId)
export const getInventory = async (vendorId = "vendor1") => {
  const url = `${API_BASE_URL}/inventory/vendor/${vendorId}`;
  console.log("Fetching inventory from:", url);

  const res = await fetch(url);
  return handleResponse(res);
};




// FAQs
export const getFAQs = async () => {
  const res = await fetch(`${API_BASE_URL}/help/faqs`);
  return handleResponse(res);
};

// ✅ FIXED: Place Order
export const placeOrder = async (orderData) => {
  const res = await fetch(`${API_BASE_URL}/orders/place`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(orderData),
  });

  return handleResponse(res);
};

