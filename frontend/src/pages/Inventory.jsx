import React, { useEffect, useState } from "react";
import InventoryItem from "../components/InventoryItem";
import { getInventory, getOrders } from "../utils/api";

const Inventory = () => {
  const [inventory, setInventory] = useState([]);
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const inv = await getInventory("vendor1");  // <-- Pass vendorId here
        console.log("Fetched Inventory:", inv);
        setInventory(Array.isArray(inv) ? inv : inv.inventory || []);

        const orderRes = await getOrders();
        if (orderRes && Array.isArray(orderRes.orders)) {
          setOrders(orderRes.orders);
        } else {
          setOrders([]);
        }
      } catch (err) {
        console.error("❌ Error fetching data:", err.message);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="p-4 max-w-4xl mx-auto">
      {/* Inventory Section */}
      <h1 className="text-2xl font-bold text-yellow-600 mb-4">Your Inventory</h1>
      <div className="grid grid-cols-1 gap-4 mb-8">
        {inventory.length > 0 ? (
          inventory.map((item, index) => (
            <InventoryItem key={index} item={item} />
          ))
        ) : (
          <p className="text-gray-500">No inventory data available.</p>
        )}
      </div>

      {/* Orders Section */}
      <h2 className="text-xl font-semibold text-yellow-700 mb-4">Recent Orders</h2>
      {orders.length === 0 ? (
        <p className="text-gray-500">No orders yet.</p>
      ) : (
        <ul className="space-y-4">
          {orders.map((order, idx) => (
            <li
              key={idx}
              className="bg-white rounded-xl shadow p-4 border border-yellow-300"
            >
              <p className="text-sm text-gray-500 mb-2">
                🕓 Ordered on:{" "}
                {order.timestamp
                  ? new Date(order.timestamp).toLocaleString()
                  : "Unknown time"}
              </p>
              <ul className="pl-4 list-disc text-gray-800">
                {Array.isArray(order.items) && order.items.length > 0 ? (
                  order.items.map((item, i) => (
                    <li key={i}>
                      {item.name} × {item.quantity} @ ₹{item.price} each
                    </li>
                  ))
                ) : (
                  <li className="text-red-500">⚠️ No items found</li>
                )}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Inventory;
