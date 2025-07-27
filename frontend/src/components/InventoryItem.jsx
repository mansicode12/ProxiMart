import React from "react";

const InventoryItem = ({ item }) => {
  return (
    <div className="bg-white shadow-md rounded-2xl p-4 border border-yellow-300">
      <h2 className="text-lg font-semibold text-gray-800">{item.name || "Unnamed Item"}</h2>
      <p className="text-gray-600">Quantity: {item.quantity ?? "N/A"}</p>
      <p className="text-gray-600">Price: {item.price ?? "N/A"}</p>
      <p
        className={`text-sm mt-2 ${
          typeof item.quantity === "number" && item.quantity < 10
            ? "text-red-500 font-semibold"
            : "text-green-600"
        }`}
      >
        {typeof item.quantity === "number" && item.quantity < 10
          ? "Low stock!"
          : "Sufficient stock"}
      </p>
    </div>
  );
};

export default InventoryItem;
