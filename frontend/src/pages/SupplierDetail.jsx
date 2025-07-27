// src/pages/SupplierDetail.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getSuppliers, placeOrder } from "../utils/api";

const SupplierDetail = () => {
  const { id } = useParams();
  const [supplier, setSupplier] = useState(null);
  const [orders, setOrders] = useState([]); // { itemName, quantity }
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchSupplier = async () => {
      try {
        const data = await getSuppliers();
        const found = data.find((s) => s.id === id);
        setSupplier(found);
      } catch (error) {
        console.error("Failed to fetch supplier:", error.message);
      }
    };
    fetchSupplier();
  }, [id]);

  const handleOrderChange = (itemName, quantity) => {
    setOrders((prev) => {
      const existing = prev.find((o) => o.itemName === itemName);
      if (existing) {
        return prev.map((o) =>
          o.itemName === itemName ? { ...o, quantity } : o
        );
      } else {
        return [...prev, { itemName, quantity }];
      }
    });
  };

  const handleSubmit = async () => {
    if (!supplier || orders.length === 0) {
      alert("Please select at least one item.");
      return;
    }

    const selectedItems = supplier.items.filter((item) =>
      orders.some((o) => o.itemName === item.name && o.quantity > 0)
    );

    const items = selectedItems.map((item) => {
      const orderItem = orders.find((o) => o.itemName === item.name);
      return {
        name: item.name,
        price: item.price,
        quantity: orderItem.quantity,
        supplier_id: supplier.id,
      };
    });

    const orderData = {
      vendor_id: "vendor1", // ✅ hardcoded vendor for now
      items,
    };

    console.log("📦 Submitting order:", orderData);

    try {
      const response = await placeOrder(orderData);
      alert("Order placed successfully!");
      setOrders([]);
      setMessage("Order placed successfully.");
    } catch (err) {
      console.error("❌ Order failed:", err.message);
      alert("Order failed. Please try again.");
    }
  };

  if (!supplier) {
    return <p className="p-4 text-gray-500">Loading supplier details...</p>;
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold text-yellow-600 mb-4">{supplier.name}</h1>

      <div className="bg-white shadow-lg rounded-2xl p-6 border border-yellow-300">
        <p className="text-gray-700 mb-2">
          <strong>Location:</strong> {supplier.location?.lat ?? "?"}, {supplier.location?.lon ?? "?"}
        </p>
        <h2 className="text-lg font-semibold text-yellow-700 mb-1">Available Items:</h2>
        <ul className="list-disc list-inside text-gray-700 mb-4">
          {supplier.items?.map((item, idx) => (
            <li key={idx} className="flex items-center justify-between mb-2">
              <span>{item.name} – ₹{item.price ?? "?"}</span>
              <input
                type="number"
                placeholder="Qty"
                min="0"
                className="w-20 p-1 border rounded ml-4"
                onChange={(e) =>
                  handleOrderChange(item.name, parseInt(e.target.value, 10) || 0)
                }
              />
            </li>
          ))}
        </ul>

        <button
          className="mt-4 bg-yellow-500 text-white px-4 py-2 rounded-xl hover:bg-yellow-600 transition"
          onClick={handleSubmit}
        >
          Place Order
        </button>

        {message && <p className="mt-3 text-sm text-blue-600">{message}</p>}
      </div>
    </div>
  );
};

export default SupplierDetail;
