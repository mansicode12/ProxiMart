import React, { useEffect, useState } from "react";
import OrderCard from "../components/OrderCard";
import { getOrders } from "../utils/api";

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const vendorId = "vendor1"; // Change to your vendor ID
        const data = await getOrders(vendorId);
        console.log("Fetched orders:", data);

        // ✅ Make sure to access correct property from API response
        const orderList = Array.isArray(data.orders)
          ? data.orders
          : data.order_history || [];

        setOrders(orderList);
      } catch (error) {
        console.error("Failed to fetch orders:", error.message);
        setOrders([]);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold text-yellow-600 mb-4">Your Orders</h1>
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : orders.length > 0 ? (
        <div className="grid grid-cols-1 gap-4">
          {orders.map((order, index) => (
            <OrderCard key={index} order={order} />
          ))}
        </div>
      ) : (
        <p className="text-gray-500">No orders found.</p>
      )}
    </div>
  );
};

export default Orders;
