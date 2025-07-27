// src/components/SupplierCard.jsx
import React from "react";
import { useNavigate } from "react-router-dom";

const SupplierCard = ({ supplier }) => {
  const navigate = useNavigate();

  if (!supplier || !supplier.name) return null;

  return (
    <div
      className="bg-white shadow-md rounded-2xl p-4 border border-yellow-300 hover:shadow-lg cursor-pointer transition-all"
      onClick={() => navigate(`/supplier/${supplier.id}`)}
    >
      <h2 className="text-xl font-semibold text-gray-800">{supplier.name}</h2>
      <p className="text-gray-600">
        Location: {supplier.location?.lat ?? "?"}, {supplier.location?.lon ?? "?"}
      </p>

      <div className="mt-2">
        <h3 className="text-md font-medium text-yellow-700">Available Items:</h3>
        {Array.isArray(supplier.items) && supplier.items.length > 0 ? (
          <ul className="list-disc list-inside text-gray-700">
            {supplier.items.map((item, idx) =>
              item?.name ? (
                <li key={idx}>
                  {item.name} — ₹{item.price ?? "?"}
                </li>
              ) : null
            )}
          </ul>
        ) : (
          <p className="text-gray-500">None</p>
        )}
      </div>
    </div>
  );
};

export default SupplierCard;
