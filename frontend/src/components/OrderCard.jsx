import React from "react";

const OrderCard = ({ order }) => {
  const formattedDate = order.timestamp
    ? new Date(order.timestamp).toLocaleString("en-IN", {
        dateStyle: "medium",
        timeStyle: "short",
      })
    : "Unknown time";

  return (
    <div className="bg-white shadow-md rounded-2xl p-4 border border-yellow-300">
      <h2 className="text-lg font-semibold text-gray-800">
        Order ID: {order.order_id || "N/A"}
      </h2>

      <p className="text-gray-600">Supplier ID: {order.supplier_id || "N/A"}</p>

      <p className="text-gray-600">
        Items:{" "}
        {Array.isArray(order.items) && order.items.length > 0
          ? order.items
              .map((item) => `${item.name} × ${item.quantity} @ ₹${item.price}`)
              .join(", ")
          : "None"}
      </p>

      <p className="text-gray-600">
        Status:{" "}
        <span
          className={`ml-2 font-medium ${
            order.status === "pending"
              ? "text-yellow-500"
              : order.status === "delivered"
              ? "text-green-600"
              : "text-gray-500"
          }`}
        >
          {order.status || "unknown"}
        </span>
      </p>

      <p className="text-gray-600">Placed On: {formattedDate}</p>
    </div>
  );
};

export default OrderCard;
